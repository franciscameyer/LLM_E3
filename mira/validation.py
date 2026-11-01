"""Comprobaciones de entrega sin cambiar el golden set ni la base de la demo."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from mira.config import ROOT
from mira.rag import build_chunks, buscar


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path = Path(path)
    if path.exists():
        raise ValueError(f"La salida ya existe: {path}. Usa otro nombre para conservar la evidencia.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as file:
        json.dump(value, file, ensure_ascii=False, indent=2)
        file.write("\n")


def expected_parts(reference, candidates):
    """Compara contenido, no IDs :01 que cambian de significado al fragmentar.

    Los objetivos originales son secciones completas. Se exige conservar todo
    su texto, incluyendo tablas; no se redefine el golden tras ver resultados.
    """
    section = reference["id"].rsplit(":", 1)[0]
    parts = [c for c in candidates if c["id"].rsplit(":", 1)[0] == section]
    normalize = lambda text: "".join(text.split())
    if not parts or normalize("".join(c["texto"] for c in parts)) != normalize(reference["texto"]):
        raise ValueError(f"El objetivo {reference['id']} no equivale a una sección completa conservada.")
    return [c["id"] for c in parts]


def compare_chunks(golden, sizes=(300, 600, 900, 1800)):
    baseline, inventory = build_chunks(1800)
    references = {c["id"]: c for c in baseline}
    report = {
        "fecha": datetime.now(timezone.utc).isoformat(), "k": golden["k"],
        "metodo": "Mismas preguntas y texto esperado del golden original. Cada objetivo es una sección completa; cuenta como encontrado solo si se recuperan TODAS sus partes dentro de k. También se informa recall por subfragmento, cuyo denominador varía con la fragmentación.",
        "busqueda": "BM25 con las reglas de conflicto existentes; no es BM25 puro. Los complementos fuera de k no se cuentan.",
        "corpus_sha256": {d["fuente"]: d["sha256"] for d in inventory},
        "experimentos": [],
    }
    for size in sizes:
        chunks, _ = build_chunks(size)
        rows = []
        found = total = complete = targets = complete_questions = answerable = 0
        for question in golden["preguntas"]:
            retrieved = buscar(question["pregunta"], golden["k"], chunks=chunks)["fragmentos"]
            ids = {c["id"] for c in retrieved}
            objectives = []
            for identifier in question["fragmentos"]:
                needed = expected_parts(references[identifier], chunks)
                hits = [i for i in needed if i in ids]
                full = len(hits) == len(needed)
                found += len(hits)
                total += len(needed)
                targets += 1
                complete += full
                objectives.append({"referencia_original": identifier, "partes_necesarias": needed,
                    "partes_recuperadas": hits, "contenido_completo": full})
            if objectives:
                answerable += 1
                complete_questions += all(o["contenido_completo"] for o in objectives)
            rows.append({"id": question["id"], "tipo": question["tipo"],
                "objetivos": objectives, "recuperados": [c["id"] for c in retrieved],
                "caracteres_contexto_base": sum(len(c["texto"]) for c in retrieved),
                "fallo": "recuperacion" if any(not o["contenido_completo"] for o in objectives) else None})
        signature = hashlib.sha256(json.dumps([(c["id"], c["texto"]) for c in chunks], ensure_ascii=False).encode()).hexdigest()
        report["experimentos"].append({"max_caracteres": size, "fragmentos": len(chunks),
            "firma_fragmentacion": signature, "objetivos_completos": complete, "objetivos_totales": targets,
            "recall_contenido_completo_at_k": complete / targets if targets else None,
            "recall_subfragmentos_at_k": found / total if total else None,
            "subfragmentos_encontrados": found, "subfragmentos_esperados": total,
            "preguntas_completas": complete_questions, "preguntas_con_respuesta": answerable,
            "caracteres_contexto_promedio": round(sum(q["caracteres_contexto_base"] for q in rows) / len(rows), 2),
            "preguntas": rows})
    return report


def summarize_review(run, review, source_sha):
    if review["ejecucion_sha256"] != source_sha:
        raise ValueError("La revisión corresponde a otra ejecución.")
    questions = {q["id"]: q for q in run["preguntas"]}
    judgments = review["preguntas"]
    if len(judgments) != len(questions) or {r["id"] for r in judgments} != set(questions):
        raise ValueError("La revisión debe cubrir todas las preguntas exactamente una vez.")
    supported = emitted = faithful = behavior = behavior_total = 0
    for row in judgments:
        q = questions[row["id"]]
        cited = {c["id"] for c in q["resultado"]["citas"]}
        if set(row["citas"]) != cited:
            raise ValueError(f"Citas incompletas o ajenas en {row['id']}.")
        if any(type(v) is not bool for v in row["citas"].values()) or type(row["fiel"]) is not bool:
            raise ValueError("Los juicios deben ser booleanos.")
        if not row["justificacion"].strip():
            raise ValueError("Falta justificación semántica.")
        if row["fallo"] not in (None, "recuperacion", "generacion", "servicio"):
            raise ValueError("Clasificación de fallo no reconocida.")
        if row["fiel"] and not all(row["citas"].values()):
            raise ValueError("Una respuesta fiel no puede tener una cita sin respaldo.")
        emitted += len(cited)
        supported += sum(row["citas"].values())
        faithful += row["fiel"]
        if q["tipo"] in ("conflicto", "version"):
            if type(row["comportamiento_correcto"]) is not bool:
                raise ValueError("Falta el juicio de conflicto o vigencia.")
            behavior_total += 1
            behavior += row["comportamiento_correcto"]
    return {"tipo": "evaluacion_semantica_por_agente", "revisor": review["revisor"],
        "ejecucion_sha256": source_sha, "preguntas": len(questions),
        "citas_respaldadas": supported, "citas_emitidas": emitted,
        "precision_cita": supported / emitted if emitted else None,
        "respuestas_fieles": faithful, "fidelidad": faithful / len(questions) if questions else None,
        "conflicto_vigencia_correctos": behavior, "conflicto_vigencia_total": behavior_total,
        "manejo_conflicto_vigencia": behavior / behavior_total if behavior_total else None,
        "revision_humana": "Pendiente de muestra independiente y concordancia; esto no es aprobación del cliente.",
        "unidad_cita": "Par (respuesta, ID de fragmento) único; las repeticiones del mismo ID dentro de una respuesta no se cuentan de nuevo.",
        "fallos": [{"id": r["id"], "tipo": r["fallo"]} for r in judgments if r["fallo"]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    compare = commands.add_parser("comparar")
    compare.add_argument("--salida", type=Path, required=True)
    review = commands.add_parser("revision")
    review.add_argument("--ejecucion", type=Path, required=True)
    review.add_argument("--juicios", type=Path, required=True)
    review.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "comparar":
        golden_path = ROOT / "evaluation/golden.json"
        result = compare_chunks(json.loads(golden_path.read_text(encoding="utf-8")))
        result["golden_sha256"] = digest(golden_path)
        result["evaluador_sha256"] = digest(__file__)
    else:
        result = summarize_review(json.loads(args.ejecucion.read_text(encoding="utf-8")),
            json.loads(args.juicios.read_text(encoding="utf-8")), digest(args.ejecucion))
        result["juicios_sha256"] = digest(args.juicios)
    write_json(args.salida, result)
    print(args.salida)


if __name__ == "__main__":
    main()
