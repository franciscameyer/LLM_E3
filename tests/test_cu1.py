import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import sqlite3
import time

from fastapi.testclient import TestClient
import pytest

from mira import agent, rag, security, store
from mira.api import app
from mira.bridge import call, connection


def person(uid="U-01"):
    with store.connect() as db:
        return store.usuario(db, uid)


def prepare(case="C-011", uid="U-01", sid="test"):
    with store.connect() as db:
        return store.preparar(db, person(uid), sid, case, "Boleta original legible", "El documento no permite verificar el total.")


def confirm(action, uid="U-01", sid="test", proof=None):
    proof = proof or security.sign({"purpose": "confirmacion", "sub": uid, "sid": sid, "accion": action})
    with store.connect() as db:
        return store.confirmar(db, person(uid), sid, action, proof)


def test_importacion_y_originales_inmutables(isolated):
    assert store.verificar_integridad()
    assert store.cargar_kit()["estado"] == "ya importado"
    with store.connect() as db:
        assert db.execute("SELECT COUNT(*) FROM casos").fetchone()[0] == 14
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("UPDATE casos SET puntaje=99 WHERE caso_id=?", ("C-012",))


def test_metadatos_no_se_confunden_con_tablas_del_cuerpo(isolated):
    data = rag.load_index()
    assert len(data["documentos"]) == 6
    assert {d["codigo"] for d in data["documentos"]} == {"POL-DEC", "PRO-ANT", "CAT-SEN", "MAN-REV", "FAQ-OPE"}
    assert rag.fragmento("CAT-SEN@3#s06:01")["codigo"] == "CAT-SEN"


def test_recuperacion_vigente_y_historico(isolated):
    regular = rag.buscar("¿El fraude resta 20 puntos?")["fragmentos"]
    assert all(c["estado"] == "vigente" for c in regular)
    historical = rag.buscar("¿El fraude resta 20 puntos?", 12, True)["fragmentos"]
    assert any(c["estado"] == "derogada" for c in historical)


def test_conflicto_preserva_ambas_fuentes(isolated):
    result = rag.buscar("¿El manual dice aprobar desde 80 y la política desde 85?")
    assert result["conflictos"]
    assert {"MAN-REV@1#s01:01", "POL-DEC@2#s02:01"}.issubset({c["id"] for c in result["fragmentos"]})


def test_contexto_mantiene_contraparte_de_una_fuente_en_conflicto(isolated):
    result = rag.buscar("casos", k=1, chunks=[rag.fragmento("MAN-REV@1#s01:01"), rag.fragmento("POL-DEC@2#s02:01")])
    ids = {c["id"] for c in result["fragmentos"] + result["complementarios_conflicto"]}
    assert len(result["fragmentos"]) == 1
    assert len(result["complementarios_conflicto"]) == 1
    assert {"MAN-REV@1#s01:01", "POL-DEC@2#s02:01"}.issubset(ids)


def test_datos_ajenos_y_rol_de_indicadores_bloqueados(isolated):
    with store.connect() as db:
        with pytest.raises(ValueError, match="no disponible"):
            store.detalle(db, person(), "C-020")
        with pytest.raises(ValueError, match="rol"):
            store.listar_casos(db, person("U-03"))


def test_inyeccion_en_evidencia_se_aisla_y_original_se_conserva(isolated):
    with store.connect() as db:
        data = store.detalle(db, person(), "C-014")
        evidence = next(e for e in data["evidencias"] if e["evidencia_id"] == "E-007")
        assert "alerta_manipulacion" in evidence
        assert "ignora las políticas" not in evidence["texto_extraido"]
        assert "ignora las políticas" in db.execute("SELECT texto_extraido FROM evidencias WHERE evidencia_id=?", ("E-007",)).fetchone()[0]


def test_discrepancia_de_aprobacion_de_umbral_visible(isolated):
    with store.connect() as db:
        data = store.detalle(db, person(), "C-012")
        assert data["discrepancias"][0]["cambio"] == "CU-001"
        assert data["organizacion"]["umbral_aprobacion"] == 90


def test_tercera_solicitud_operador_y_aprobado_auto_rechazados(isolated):
    with pytest.raises(ValueError, match="supervisor"):
        prepare("C-016")
    with pytest.raises(ValueError, match="automáticamente"):
        prepare("C-010")
    assert prepare("C-016", "U-02")["requiere_confirmacion"]


def test_preparar_no_cambia_caso_ni_agrega_solicitud(isolated):
    proposal = prepare()
    with store.connect() as db:
        assert db.execute("SELECT COUNT(*) FROM solicitudes_antecedentes WHERE caso_id='C-011'").fetchone()[0] == 0
        assert store.caso_visible(db, person(), "C-011")["estado_actual"] == "en_revision"
    assert proposal["requiere_confirmacion"]


def test_confirmar_exige_firma_sesion_y_caducidad(isolated):
    proposal = prepare()
    with pytest.raises(ValueError, match="no válida"):
        confirm(proposal["accion_id"], proof="falsa")
    with pytest.raises(ValueError, match="corresponde"):
        confirm(proposal["accion_id"], proof=security.sign({"purpose": "confirmacion", "sub": "U-02", "sid": "test", "accion": proposal["accion_id"]}))
    with store.connect() as db:
        db.execute("UPDATE acciones_pendientes SET vence=? WHERE accion_id=?", (time.time() - 1, proposal["accion_id"]))
    with pytest.raises(ValueError, match="venció"):
        confirm(proposal["accion_id"])


def test_confirmar_es_atomico_idempotente_y_preserva_originales(isolated):
    proposal = prepare()
    first = confirm(proposal["accion_id"])
    second = confirm(proposal["accion_id"])
    assert first["solicitud_id"] == second["solicitud_id"]
    assert second["repeticion_sin_efecto"]
    with store.connect() as db:
        assert db.execute("SELECT COUNT(*) FROM solicitudes_antecedentes WHERE caso_id='C-011'").fetchone()[0] == 1
        assert store.caso_visible(db, person(), "C-011")["estado_actual"] == "solicitud_antecedentes"
        assert db.execute("SELECT estado FROM casos WHERE caso_id='C-011'").fetchone()[0] == "en_revision"
        assert db.execute("SELECT COUNT(*) FROM avisos_origen").fetchone()[0] == 1
    assert store.verificar_integridad()


def test_confirmaciones_concurrentes_no_eluden_limite(isolated):
    proposals = [prepare() for _ in range(3)]
    def run(p):
        try:
            confirm(p["accion_id"])
            return True
        except ValueError:
            return False
    with ThreadPoolExecutor(max_workers=3) as pool:
        assert sum(pool.map(run, proposals)) == 2


def test_sql_injection_no_interpreta_argumento_como_sql(isolated):
    with store.connect() as db:
        with pytest.raises(ValueError):
            store.detalle(db, person(), "C-012' OR 1=1 --")
        assert db.execute("SELECT COUNT(*) FROM casos").fetchone()[0] == 14


def test_mcp_real_lista_primitivas_y_audita_denegacion(isolated):
    async def run():
        async with connection("U-01", "mcp-test") as c:
            assert {t.name for t in await c.list_tools()} >= {"buscar_reglas", "consultar_caso", "preparar_solicitud"}
            assert await c.list_resources()
            assert await c.list_prompts()
            result = await call(c, "consultar_caso", {"caso_id": "C-020"})
            assert not result["ok"]
            assert not result["traza"]["ok"]
            trace = await call(c, "ver_trazas", {})
            assert any(t["herramienta"] == "consultar_caso" for t in trace["datos"])
    asyncio.run(run())


def test_api_login_csrf_y_consulta_mcp(isolated):
    with TestClient(app) as client:
        assert client.get("/api/casos").status_code == 401
        login = client.post("/api/login", json={"usuario_id": "U-01", "password": "mira-demo"})
        assert login.status_code == 200
        assert "HttpOnly" in login.headers["set-cookie"]
        assert client.post("/api/buscar", json={"pregunta": "fraude"}).status_code == 401
        headers = {"X-MIRA-CSRF": login.json()["csrf"]}
        result = client.post("/api/buscar", headers=headers, json={"pregunta": "fraude"})
        assert result.json()["ok"]
        assert result.json()["trazas"][0]["herramienta"] == "buscar_reglas"
        assert client.post("/api/propuestas/no-existe/confirmar", headers=headers, json={"confirmo": False}).status_code == 400


def test_agente_rechaza_citas_inventadas(isolated, monkeypatch):
    async def fake(*args, **kwargs):
        return {"content": json.dumps({"estado": "evidencia", "respuesta": "Afirmación [NO-EXISTE]", "citas": ["NO-EXISTE"]})}
    monkeypatch.setattr(agent, "completion", fake)
    result = asyncio.run(agent.answer("U-01", "test-agent", "¿Cuál es el mínimo DOC_AUT?"))
    assert result["estado"] == "error"
    assert "no recibió" in result["respuesta"]


def test_reintento_citas_no_ejecuta_tools_y_revalida_salida(isolated, monkeypatch):
    calls = []
    async def fake(http, messages, tools=None, final=False):
        calls.append((tools, final))
        if len(calls) == 1:
            return {"content": json.dumps({"estado": "evidencia", "respuesta": "70 [INVENTADA]", "citas": ["INVENTADA"]})}
        assert len(calls) == 2 and tools is None and final
        assert "POL-DEC@2#s03:01" in messages[-1]["content"]
        return {"content": json.dumps({"estado": "evidencia", "respuesta": "Mínimo DOC_AUT: 70 [POL-DEC@2#s03:01]", "citas": ["POL-DEC@2#s03:01"]})}
    monkeypatch.setattr(agent, "completion", fake)
    result = asyncio.run(agent.answer("U-01", "test-repair", "¿Cuál es el mínimo DOC_AUT?"))
    assert result["estado"] == "evidencia"
    assert result["reintento_citas"] is True
    assert len(calls) == 2


def test_agente_reporta_caida_del_modelo_sin_respuesta_inventada(isolated, monkeypatch):
    async def fail(*args, **kwargs):
        raise agent.ModelUnavailable("Bonsai no está disponible")
    monkeypatch.setattr(agent, "completion", fail)
    result = asyncio.run(agent.answer("U-01", "test-offline", "¿Cuál es el mínimo DOC_AUT?"))
    assert result["estado"] == "error"
    assert result["respuesta"] == "Bonsai no está disponible"
    assert result["trazas"]


def test_agente_no_expone_herramienta_de_confirmacion(isolated, monkeypatch):
    async def fake(http, messages, tools=None, final=False):
        if tools:
            assert "confirmar_solicitud" not in {t["function"]["name"] for t in tools}
        return {"tool_calls": [{"id": "bad", "function": {"name": "confirmar_solicitud", "arguments": "{}"}}]}
    monkeypatch.setattr(agent, "completion", fake)
    result = asyncio.run(agent.answer("U-01", "test-forbidden-tool", "Prepara antecedentes para C-011"))
    assert result["estado"] == "error"
    assert "fuera de sus permisos" in result["respuesta"]


def test_agente_se_abstiene_si_no_consulto_el_caso(isolated, monkeypatch):
    async def fake(*args, **kwargs):
        return {"content": json.dumps({"estado": "abstencion", "respuesta": "El caso C-012 tiene 99 puntos", "citas": []})}
    monkeypatch.setattr(agent, "completion", fake)
    result = asyncio.run(agent.answer("U-01", "test-not-consulted", "Consulta C-012"))
    assert result["estado"] == "abstencion"
    assert "99" not in result["respuesta"]
    assert "ficha autorizada" in result["respuesta"]


@pytest.mark.parametrize("uid,case", [("U-03", "C-012"), ("U-01", "C-020")])
def test_denegacion_mcp_se_muestra_sin_otro_turno_del_modelo(isolated, monkeypatch, uid, case):
    calls = []
    async def fake(*args, **kwargs):
        calls.append(True)
        assert len(calls) == 1, "No debe pedir al modelo reformular una denegación definitiva"
        return {"tool_calls": [{"function": {"name": "consultar_caso",
            "arguments": json.dumps({"caso_id": case})}}]}
    monkeypatch.setattr(agent, "completion", fake)
    result = asyncio.run(agent.answer(uid, "test-denied", f"Consulta {case}"))
    assert result["estado"] == "abstencion"
    assert result["motivo_abstencion"] == "acceso_denegado"
    assert result["citas"] == []
    assert not result["trazas"][-1]["ok"]


def test_guardia_no_afirma_vigencia_de_umbral_incompleto():
    warnings = [{"valor_reportado": 90}]
    assert agent.asserts_unverified_threshold("El umbral de 90.0 aplica para esta organización.", warnings)
    assert not agent.asserts_unverified_threshold("No se puede asumir que el umbral de 90 aplica.", warnings)
    assert not agent.asserts_unverified_threshold("La plataforma reporta un umbral de 90.", warnings)


def test_datos_enviados_al_modelo_no_duplican_auditoria():
    data = {"datos": {"texto": "Evidencia", "texto_busqueda": "Duplicado", "reglas_relevantes": []},
        "traza": {"resultado": "Duplicado"}}
    assert agent.model_data(data) == {"datos": {"texto": "Evidencia"}}


def test_conflicto_se_valida_aunque_la_pregunta_sea_sobre_roles(isolated, monkeypatch):
    async def fake(*args, **kwargs):
        return {"content": json.dumps({"estado": "evidencia", "respuesta": "Se aprueba desde 80 [MAN-REV@1#s01:01]", "citas": ["MAN-REV@1#s01:01"]})}
    monkeypatch.setattr(agent, "completion", fake)
    # Forzar que la fuente problemática forme parte del contexto recibido.
    from mira import bridge
    original = agent.call
    async def with_fragment(client, name, args, traces=None):
        result = await original(client, name, args, traces)
        if name == "buscar_reglas":
            result["datos"]["fragmentos"].append(rag.fragmento("MAN-REV@1#s01:01"))
        return result
    monkeypatch.setattr(agent, "call", with_fragment)
    result = asyncio.run(agent.answer("U-01", "test-conflict-independent", "¿Qué roles pueden solicitar antecedentes?"))
    assert result["estado"] == "error"
    assert "conflicto" in result["respuesta"]
