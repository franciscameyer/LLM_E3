"""Métricas reproducibles; fidelidad y respaldo semántico requieren revisión humana."""

import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import time

from mira.config import ROOT
from mira.rag import build_chunks, buscar


async def evaluate(generation=False, output_dir=None):
    destination = Path(output_dir) if output_dir else ROOT / "evaluation"
    destination.mkdir(parents=True, exist_ok=True)
    if output_dir and any((destination / name).exists() for name in (
        "resultados_recuperacion.json", "resultados_generacion.json", "revision_manual.csv")):
        raise ValueError("La carpeta de salida ya contiene evidencia. Usa una carpeta nueva.")
    golden_path = ROOT / "evaluation" / "golden.json"
    golden_bytes = golden_path.read_bytes()
    golden = json.loads(golden_bytes)
    code_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT / "mira").glob("*.py"))}
    report = {"fecha": datetime.now(timezone.utc).isoformat(), "golden_sha256": hashlib.sha256(golden_bytes).hexdigest(),
        "codigo_sha256": code_hashes,
        "k": golden["k"], "estado_validacion_cliente": golden["estado"], "experimentos": [],
        "metodo": "Recall@k por fragmento esperado; se excluyen del denominador las preguntas sin respuesta. No se atribuye fidelidad a un simple ID válido."}
    for size in (900, 1800):
        chunks, _ = build_chunks(size)
        results, expected, found = [], 0, 0
        for item in golden["preguntas"]:
            retrieved = [d["id"] for d in buscar(item["pregunta"], golden["k"], chunks=chunks)["fragmentos"]]
            hits = [x for x in item["fragmentos"] if x in retrieved]
            found += len(hits)
            expected += len(item["fragmentos"])
            results.append({"id": item["id"], "tipo": item["tipo"], "esperados": item["fragmentos"],
                "recuperados": retrieved, "fallo": "recuperacion" if len(hits) < len(item["fragmentos"]) else None})
        report["experimentos"].append({"max_caracteres": size, "fragmentos": len(chunks),
            "recall_at_k": found / expected if expected else None, "aciertos_fragmento": found,
            "total_fragmentos_esperados": expected, "preguntas": results})
    path = destination / "resultados_recuperacion.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    for exp in report["experimentos"]:
        print(f"Tamaño {exp['max_caracteres']}: Recall@{golden['k']} = {exp['recall_at_k']:.3f} ({exp['aciertos_fragmento']}/{exp['total_fragmentos_esperados']})")
    if generation:
        from mira.agent import answer, model_info
        info = await model_info()
        configured = os.getenv("LLM_MODEL", "auto")
        output = destination / "resultados_generacion.json"
        run = {"fecha": datetime.now(timezone.utc).isoformat(), "codigo_sha256": code_hashes,
            "golden_sha256": report["golden_sha256"], "modelo_configurado": configured,
            "modelo": info["modelos"][0] if configured == "auto" and len(info["modelos"]) == 1 else configured,
            "estado_modelo_al_inicio": info,
            "base_url": os.getenv("LLM_BASE_URL", "http://127.0.0.1:8080/v1"),
            "modo_herramientas": os.getenv("LLM_TOOL_MODE", "native"), "preguntas": [],
            "revision_humana": "Pendiente: precisión de cita, fidelidad y semántica de conflicto/vigencia; no inferidas automáticamente."}
        for item in golden["preguntas"]:
            start = time.monotonic()
            result = await answer("U-01", "evaluacion-" + item["id"], item["pregunta"])
            retrieved = {c["id"] for t in result["trazas"] if t["herramienta"] == "buscar_reglas" and t["ok"]
                for c in t["resultado"]["datos"]["fragmentos"]}
            missing = set(item["fragmentos"]) - retrieved
            failure = "recuperacion" if missing else (
                ("generacion" if result.get("tipo_error") == "validacion" else "servicio") if result["estado"] == "error" else
                "generacion" if (item["tipo"] == "sin_respuesta" and result["estado"] != "abstencion") or
                    (item["tipo"] != "sin_respuesta" and result["estado"] == "abstencion") or
                    (item["tipo"] == "conflicto" and result["estado"] != "conflicto") else "pendiente_revision_semantica")
            run["preguntas"].append({**item, "resultado": result, "segundos": round(time.monotonic() - start, 2), "clasificacion_inicial": failure})
            # Guardar tras cada pregunta permite recuperar una ejecución interrumpida.
            output.write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")
            print(item["id"], result["estado"], failure, flush=True)
        no_answer = [q for q in run["preguntas"] if not q["debe_responder"]]
        with_answer = [q for q in run["preguntas"] if q["debe_responder"]]
        run["metricas_automaticas"] = {
            "abstencion_en_sin_respuesta": sum(q["resultado"]["estado"] == "abstencion" for q in no_answer) / len(no_answer),
            "abstencion_en_con_respuesta": sum(q["resultado"]["estado"] == "abstencion" for q in with_answer) / len(with_answer),
            "precision_cita": None, "fidelidad": None,
            "nota": "Precisión y fidelidad pendientes de juicio sobre el contenido, no sobre el formato."}
        output.write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")
        with (destination / "revision_manual.csv").open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "citas_emitidas", "citas_respaldan", "respuesta_totalmente_fiel_0_1", "conflicto_o_vigencia_correcto_0_1", "fallo_recuperacion_generacion", "observacion", "revisor"])
            for q in run["preguntas"]:
                writer.writerow([q["id"], len(q["resultado"]["citas"]), "", "", "", q["clasificacion_inicial"], "", ""])
    print(f"Resultados de recuperación: {path}")
