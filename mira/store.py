"""Persistencia de negocio. Solo el servidor MCP y la carga administrativa la usan."""

from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import re
import sqlite3
import time
import uuid

from mira.config import DATA, DB, KIT, ensure_data
from mira.security import verify


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def connect():
    db = sqlite3.connect(DB, timeout=15)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    try:
        with db:
            yield db
    finally:
        db.close()


def rows(db, sql, args=()):
    return [dict(r) for r in db.execute(sql, args)]


def cargar_kit():
    from openpyxl import load_workbook

    ensure_data()
    excel = KIT / "datos" / "CU-1_datos.xlsx"
    digest = hashlib.sha256(excel.read_bytes()).hexdigest()
    manifest_path = DATA / "importacion.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest["excel_sha256"] != digest:
            raise ValueError("El Excel cambió. No se sobrescribirá la base existente.")
        verificar_integridad()
        return {"estado": "ya importado", "tablas": manifest["tablas"]}
    workbook = load_workbook(excel, read_only=True, data_only=True)
    counts, fingerprints, users = {}, {}, []
    with connect() as db:
        db.execute("PRAGMA journal_mode=WAL")
        for sheet in workbook:
            if sheet.title == "LEEME":
                continue
            values = list(sheet.values)
            headers = list(values[0])
            if not all(re.fullmatch(r"[a-z_][a-z0-9_]*", n or "") for n in [sheet.title, *headers]):
                raise ValueError("Nombre de tabla o columna inválido en el Excel.")
            declarations = []
            for i, name in enumerate(headers):
                column = [r[i] for r in values[1:] if r[i] is not None]
                kind = "REAL" if column and all(isinstance(x, (int, float)) for x in column) else "TEXT"
                declarations.append(f'"{name}" {kind}' + (" PRIMARY KEY" if i == 0 else ""))
            table = sheet.title
            db.execute(f'CREATE TABLE "{table}" ({", ".join(declarations)})')
            placeholders = ",".join("?" for _ in headers)
            db.executemany(f'INSERT INTO "{table}" VALUES ({placeholders})', values[1:])
            for operation in ("UPDATE", "DELETE"):
                db.execute(f'''CREATE TRIGGER "preservar_{table}_{operation}"
                    BEFORE {operation} ON "{table}" BEGIN
                    SELECT RAISE(ABORT, 'Los registros importados son inmutables'); END''')
            counts[table] = len(values) - 1
            fingerprints[table] = {
                str(row[0]): hashlib.sha256(json.dumps(dict(zip(headers, row)), ensure_ascii=False,
                    sort_keys=True, default=str).encode()).hexdigest()
                for row in values[1:]
            }
            if table == "usuarios":
                users = [dict(zip(headers, row)) for row in values[1:]]
        db.executescript('''
            CREATE TABLE acciones_pendientes (
                accion_id TEXT PRIMARY KEY, usuario_id TEXT NOT NULL, sesion_id TEXT NOT NULL,
                caso_id TEXT NOT NULL, contenido TEXT NOT NULL, creado TEXT NOT NULL,
                vence REAL NOT NULL, estado TEXT NOT NULL DEFAULT 'pendiente', resultado TEXT
            );
            CREATE TABLE eventos_caso (
                evento_id TEXT PRIMARY KEY, caso_id TEXT NOT NULL, estado TEXT NOT NULL,
                usuario_id TEXT NOT NULL, fecha TEXT NOT NULL, accion_id TEXT UNIQUE NOT NULL
            );
            CREATE TABLE avisos_origen (
                aviso_id TEXT PRIMARY KEY, caso_id TEXT NOT NULL, solicitud_id TEXT NOT NULL,
                estado TEXT NOT NULL, fecha TEXT NOT NULL
            );
            CREATE TABLE auditoria (
                traza_id TEXT PRIMARY KEY, fecha TEXT NOT NULL, usuario_id TEXT NOT NULL,
                sesion_id TEXT NOT NULL, herramienta TEXT NOT NULL, argumentos TEXT NOT NULL,
                resultado TEXT NOT NULL, ok INTEGER NOT NULL
            );
        ''')
    workbook.close()
    # JSON numérico normalizado según SQLite (85.0 == 85) al verificar integridad.
    manifest_path.write_text(json.dumps({"excel_sha256": digest, "tablas": counts,
        "filas": fingerprints, "fecha": now()}, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "usuarios_demo.json").write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"estado": "importado", "tablas": counts}


def verificar_integridad():
    """Compara cada fila original con el Excel, permitiendo solo filas nuevas."""
    from openpyxl import load_workbook
    workbook = load_workbook(KIT / "datos" / "CU-1_datos.xlsx", read_only=True, data_only=True)
    with connect() as db:
        for sheet in workbook:
            if sheet.title == "LEEME":
                continue
            all_rows = list(sheet.values)
            headers = list(all_rows[0])
            for original in all_rows[1:]:
                stored = db.execute(f'SELECT * FROM "{sheet.title}" WHERE "{headers[0]}"=?', (original[0],)).fetchone()
                if stored is None or any(stored[k] != v for k, v in zip(headers, original)):
                    raise ValueError(f"La fila original {sheet.title}/{original[0]} fue alterada.")
    workbook.close()
    return True


def usuario(db, uid):
    user = db.execute("SELECT * FROM usuarios WHERE usuario_id=?", (uid,)).fetchone()
    if not user:
        raise ValueError("Usuario no autorizado.")
    return dict(user)


def can_review(user):
    if user["rol"] not in {"operador", "supervisor"}:
        raise ValueError("Este rol no tiene permiso para consultar ni modificar casos individuales.")


def caso_visible(db, user, case):
    can_review(user)
    found = db.execute("""SELECT c.*, COALESCE((SELECT e.estado FROM eventos_caso e
        WHERE e.caso_id=c.caso_id ORDER BY rowid DESC LIMIT 1), c.estado) estado_actual
        FROM casos c WHERE c.caso_id=? AND c.org_id=?""", (case, user["org_id"])).fetchone()
    if found is None:
        raise ValueError("Caso no disponible para el usuario conectado.")
    return dict(found)


def listar_casos(db, user):
    can_review(user)
    return rows(db, """SELECT c.caso_id,c.tipo_proceso,c.puntaje,c.motivo_derivacion,c.vence_el,
        COALESCE((SELECT e.estado FROM eventos_caso e WHERE e.caso_id=c.caso_id
        ORDER BY rowid DESC LIMIT 1),c.estado) estado FROM casos c WHERE c.org_id=? ORDER BY c.caso_id""", (user["org_id"],))


def detalle(db, user, case):
    record = caso_visible(db, user, case)
    org = dict(db.execute("SELECT * FROM organizaciones WHERE org_id=?", (user["org_id"],)).fetchone())
    changes = rows(db, "SELECT * FROM cambios_umbral WHERE org_id=?", (user["org_id"],))
    warnings = []
    for change in changes:
        if not change["aprobador_2"] or change["aprobador_1"] == change["aprobador_2"]:
            warnings.append({"tipo": "dato_vs_politica", "cambio": change["cambio_id"],
                "valor_reportado": change["valor_nuevo"],
                "descripcion": "El historial no acredita dos aprobaciones distintas. No asumir que el valor de la plataforma acredita vigencia normativa.",
                "regla": "POL-DEC@2#s05:01"})
    evidence = rows(db, "SELECT * FROM evidencias WHERE caso_id=?", (case,))
    for item in evidence:
        original = item.get("texto_extraido") or ""
        if re.search(r"ignora las pol[ií]ticas|instrucci[oó]n.*sistema|NOTA PARA EL ASISTENTE", original, re.I):
            item["texto_extraido"] = re.split(r"Texto en el margen|NOTA PARA EL ASISTENTE", original, flags=re.I)[0].strip()
            item["alerta_manipulacion"] = "Se aisló una instrucción dirigida al asistente. No constituye evidencia para aprobar. El original se conserva en la base."
    return {"caso": record, "organizacion": org, "cambios_umbral": changes,
        "senales": rows(db, "SELECT * FROM senales WHERE caso_id=? ORDER BY senal_id", (case,)),
        "evidencias": evidence,
        "solicitudes": rows(db, "SELECT * FROM solicitudes_antecedentes WHERE caso_id=? ORDER BY fecha", (case,)),
        "discrepancias": warnings}


def validar_solicitud(db, user, case):
    record = caso_visible(db, user, case)
    if record["estado_actual"] == "aprobado_automatico":
        raise ValueError("No se permite solicitar antecedentes de un caso aprobado automáticamente (PRO-ANT §4 v1).")
    count = db.execute("SELECT COUNT(*) FROM solicitudes_antecedentes WHERE caso_id=?", (case,)).fetchone()[0]
    if count >= 2 and user["rol"] != "supervisor":
        raise ValueError(f"{case} ya tiene {count} solicitudes; una tercera debe registrarla un supervisor (PRO-ANT §4 v1).")


def preparar(db, user, sid, case, documents, reason):
    validar_solicitud(db, user, case)
    if not 5 <= len(documents.strip()) <= 1000 or not 10 <= len(reason.strip()) <= 1500:
        raise ValueError("Especifica los documentos (5–1000 caracteres) y un motivo comprensible (10–1500 caracteres), PRO-ANT §2.")
    content = {"caso_id": case, "documentos_solicitados": documents.strip(), "motivo": reason.strip(),
        "regla": "PRO-ANT@1#s02:01", "regla_limites": "PRO-ANT@1#s04:01"}
    action = "AC-" + uuid.uuid4().hex
    db.execute("INSERT INTO acciones_pendientes VALUES (?,?,?,?,?,?,?,?,?)",
        (action, user["usuario_id"], sid, case, json.dumps(content, ensure_ascii=False), now(), time.time() + 600, "pendiente", None))
    return {"accion_id": action, **content, "requiere_confirmacion": True,
        "vence_en_segundos": 600, "efecto": "Registrar solicitud y añadir evento de estado; el aviso al origen queda en cola simulada."}


def confirmar(db, user, sid, action, proof):
    authorization = verify(proof, "confirmacion")
    if (authorization.get("sub"), authorization.get("sid"), authorization.get("accion")) != (user["usuario_id"], sid, action):
        raise ValueError("La confirmación no corresponde a esta sesión, usuario y acción.")
    # Serializar contar+insertar impide que dos confirmaciones eludan el límite.
    db.execute("BEGIN IMMEDIATE")
    pending = db.execute("SELECT * FROM acciones_pendientes WHERE accion_id=? AND usuario_id=? AND sesion_id=?",
        (action, user["usuario_id"], sid)).fetchone()
    if not pending:
        raise ValueError("No existe una propuesta de esta sesión.")
    if pending["estado"] == "ejecutada":
        return {**json.loads(pending["resultado"]), "repeticion_sin_efecto": True}
    if pending["estado"] != "pendiente" or pending["vence"] <= time.time():
        raise ValueError("La propuesta venció o fue cancelada; prepara una nueva.")
    validar_solicitud(db, user, pending["caso_id"])
    content = json.loads(pending["contenido"])
    solicitud = "SA-MIRA-" + uuid.uuid4().hex[:12]
    stamp = now()
    db.execute("INSERT INTO solicitudes_antecedentes VALUES (?,?,?,?,?,?,?)", (
        solicitud, pending["caso_id"], user["usuario_id"], stamp,
        content["documentos_solicitados"], content["motivo"], "pendiente"))
    db.execute("INSERT INTO eventos_caso VALUES (?,?,?,?,?,?)", (
        "EV-" + uuid.uuid4().hex, pending["caso_id"], "solicitud_antecedentes", user["usuario_id"], stamp, action))
    db.execute("INSERT INTO avisos_origen VALUES (?,?,?,?,?)", (
        "AV-" + uuid.uuid4().hex, pending["caso_id"], solicitud, "simulado_sin_callback_configurado", stamp))
    result = {"solicitud_id": solicitud, "caso_id": pending["caso_id"], "estado": "solicitud_antecedentes",
        "registrada_por": user["usuario_id"], "fecha": stamp, "aviso_origen": "Simulado: no hay un callback real configurado."}
    db.execute("UPDATE acciones_pendientes SET estado='ejecutada',resultado=? WHERE accion_id=?", (json.dumps(result), action))
    return result


def audit(user, sid, tool, args, result, ok, transaction=None):
    trace = {"id": "TR-" + uuid.uuid4().hex, "fecha": now(), "usuario": user["usuario_id"],
        "herramienta": tool, "argumentos": args, "ok": ok, "resultado": result}
    def write(db):
        db.execute("INSERT INTO auditoria VALUES (?,?,?,?,?,?,?,?)", (
            trace["id"], trace["fecha"], user["usuario_id"], sid, tool,
            json.dumps(args, ensure_ascii=False), json.dumps(result, ensure_ascii=False), int(ok)))
    if transaction is not None:
        write(transaction)
    else:
        with connect() as db:
            write(db)
    return trace
