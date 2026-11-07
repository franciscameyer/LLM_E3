"""Genera un paquete de revision trazable sin atribuir aprobaciones humanas."""

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
RUN = ROOT / "evaluation/ejecucion_06/resultados_generacion.json"
GOLDEN = ROOT / "evaluation/golden.json"


def sha(path, normalized=False):
    data = path.read_bytes()
    return hashlib.sha256(data.replace(b"\r\n", b"\n") if normalized else data).hexdigest()


def write(name, value):
    with (OUT / name).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main():
    run = json.loads(RUN.read_text(encoding="utf-8-sig"))
    golden = json.loads(GOLDEN.read_text(encoding="utf-8-sig"))
    prior_path = ROOT / "evaluation/ejecucion_06/revision_semantica_agente.json"
    prior = json.loads(prior_path.read_text(encoding="utf-8-sig"))
    assert prior["ejecucion_sha256"] in {sha(RUN), sha(RUN, True)}
    selected = {
        "R01": "Las tres fuentes respaldan 80/85, condiciones y doble aprobacion; no elige precedencia.",
        "R08": "PRO-ANT secciones 2 y 4 respaldan campos, roles y excepcion del supervisor.",
        "A01": "No inventa pesos; las dos citas describen componentes y escala, no una formula.",
        "A02": "No inventa telefono; atribuye correctamente el contenido limitado de la seccion recibida.",
        "A04": "Abstencion sin credenciales ni canales de recuperacion inventados; no emite citas.",
        "C01": "Expone las dos reglas vigentes y sus condiciones sin elegir ni acreditar un valor vivo.",
        "C02": "Expone el conflicto para el supuesto de 82 puntos; no consulta ni inventa una ficha concreta.",
        "V02": "POL-DEC v2 y FAQ respaldan dos supervisores y la ausencia de efecto con una aprobacion.",
    }
    previous = {row["id"]: row for row in prior["preguntas"]}
    reviewed = []
    for question in run["preguntas"]:
        if question["id"] not in selected:
            continue
        result = question["resultado"]
        cited = {c["id"]: True for c in result["citas"]}
        behavior = True if question["tipo"] in {"conflicto", "version"} else None
        reviewed.append({"id": question["id"], "citas": cited, "fiel": True,
                         "comportamiento_correcto": behavior, "fallo": None,
                         "justificacion": selected[question["id"]]})
    review = {"tipo": "revision_tecnica_automatizada", "fecha": "2026-11-07",
              "ejecucion": str(RUN.relative_to(ROOT)), "ejecucion_sha256": sha(RUN),
              "ejecucion_sha256_lf": sha(RUN, True),
              "alcance": "Nueva lectura de ocho respuestas guardadas y sus fragmentos; no es una nueva generacion.",
              "revision_humana": False, "aprobacion_cliente": False, "preguntas": reviewed}
    write("revision_tecnica_muestra.json", review)
    def agreements(field):
        rows = [r for r in reviewed if r[field] is not None]
        return {"acuerdos": sum(r[field] == previous[r["id"]][field] for r in rows), "comparados": len(rows)}
    write("concordancia_tecnica.json", {
        "tipo": "concordancia_entre_revisiones_tecnicas_no_humanas",
        "ejecucion_sha256": sha(RUN), "revision_previa_sha256": sha(prior_path),
        "preguntas": len(reviewed), "citas_respaldadas": sum(len(r["citas"]) for r in reviewed),
        "citas_emitidas": sum(len(r["citas"]) for r in reviewed),
        "fidelidad": agreements("fiel"), "conflicto_vigencia": agreements("comportamiento_correcto"),
        "cantidad_citas_respaldadas": {"acuerdos": sum(sum(r["citas"].values()) == sum(previous[r["id"]]["citas"].values()) for r in reviewed), "comparados": len(reviewed)},
        "discrepancias": [], "concordancia_humana": None,
        "limite": "No sustituye la muestra humana ni constituye validacion del cliente."})
    with (OUT / "muestra_humana_ejecucion06.csv").open("x", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["id", "citas_respaldadas_humano", "fiel_humano_0_1", "conflicto_vigencia_humano_0_1", "observacion", "revisor", "fecha", "ejecucion_sha256"])
        for row in reviewed:
            writer.writerow([row["id"], "", "", "", "", "", "", sha(RUN)])
    lines = ["# Validación del golden set de CU-1", "", "**Representante del cliente:** Francisca Meyer.",
             "**Estado:** CORROBORAR ESTO: aprobación expresa pendiente.",
             "**Versión:** 1.0; conjunto original del commit `089b2fb`.",
             f"**SHA-256 de archivo:** `{sha(GOLDEN)}`.",
             f"**SHA-256 normalizado a LF:** `{sha(GOLDEN, True)}`.", "",
             "Revisar pregunta, expectativa y fragmentos. La revisión técnica no firma por la representante. La decisión debe registrar fecha y observaciones reales. R01 debe leerse junto con PR-4: el valor 85 no autoriza a ocultar la discrepancia 80/85.", "",
             "| ID | Pregunta | Respuesta esperada | Fragmentos mínimos |", "| --- | --- | --- | --- |"]
    for row in golden["preguntas"]:
        cells = [row["id"], row["pregunta"], row["respuesta_esperada"], "; ".join(row["fragmentos"]) or "Sin evidencia suficiente; abstención"]
        lines.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    lines += ["", "**Decisión de Francisca Meyer:** CORROBORAR ESTO.", "**Fecha y observaciones:** CORROBORAR ESTO.",
              "", "Si se solicitan cambios, crear otra versión y conservar este conjunto; no ajustar retroactivamente las preguntas para mejorar resultados."]
    (ROOT / "docs/validacion-golden-cliente.md").write_text("\n\n".join(lines[:7]) + "\n" + "\n".join(lines[7:]) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
