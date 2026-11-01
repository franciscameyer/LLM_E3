import copy

import pytest

from mira.validation import compare_chunks, expected_parts, summarize_review, write_json


def test_comparacion_no_confunde_id_con_contenido():
    reference = {"id": "DOC@1#s01:01", "texto": "primera segunda"}
    parts = [{"id": "DOC@1#s01:01", "texto": "primera"},
             {"id": "DOC@1#s01:02", "texto": "segunda"}]
    assert expected_parts(reference, parts) == [p["id"] for p in parts]
    with pytest.raises(ValueError, match="conservada"):
        expected_parts(reference, parts[:1])


def test_comparacion_cuenta_objetivo_incompleto_aunque_recupere_primera_parte():
    golden = {"k": 1, "preguntas": [{"id": "T", "tipo": "respuesta",
        "pregunta": "mínimos DOC_AUT BIO_ROSTRO CRUCE_MONTO", "fragmentos": ["POL-DEC@2#s03:01"]}]}
    report = compare_chunks(golden, sizes=(100, 1800))
    small, full = report["experimentos"]
    assert small["fragmentos"] > full["fragmentos"]
    assert small["objetivos_completos"] == 0
    assert full["objetivos_completos"] == 1
    assert small["firma_fragmentacion"] != full["firma_fragmentacion"]


def sample_review():
    run = {"preguntas": [{"id": "T", "tipo": "version", "resultado": {"citas": [{"id": "F"}]}}]}
    review = {"ejecucion_sha256": "hash", "revisor": "agente",
        "preguntas": [{"id": "T", "citas": {"F": True}, "fiel": True,
            "comportamiento_correcto": True, "justificacion": "La regla está en F.", "fallo": None}]}
    return run, review


def test_revision_exige_ejecucion_cobertura_y_respaldo_consistentes():
    run, review = sample_review()
    assert summarize_review(run, review, "hash")["precision_cita"] == 1
    with pytest.raises(ValueError, match="otra ejecución"):
        summarize_review(run, review, "otra")
    duplicate = copy.deepcopy(review)
    duplicate["preguntas"] *= 2
    with pytest.raises(ValueError, match="exactamente una"):
        summarize_review(run, duplicate, "hash")
    review["preguntas"][0]["citas"]["F"] = False
    with pytest.raises(ValueError, match="sin respaldo"):
        summarize_review(run, review, "hash")


def test_evidencia_no_se_sobrescribe(tmp_path):
    output = tmp_path / "evidencia.json"
    write_json(output, {"original": True})
    with pytest.raises(ValueError, match="ya existe"):
        write_json(output, {"original": False})
    assert 'true' in output.read_text(encoding="utf-8")
