"""Repite los dos fallos históricos en una base temporal y conserva cada salida."""

import argparse
import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid


async def check(destination, repetitions):
    from mira.agent import answer, model_info
    from mira.config import ROOT
    from mira.validation import digest

    golden_path = ROOT / "evaluation/golden.json"
    extra_path = ROOT / "evaluation/parafrasis.json"
    golden = json.loads(golden_path.read_text(encoding="utf-8"))
    extra = json.loads(extra_path.read_text(encoding="utf-8"))
    questions = [next(q for q in extra["preguntas"] if q["id"] == "P07"),
        {**next(q for q in golden["preguntas"] if q["id"] == "A04"), "usuario": "U-01"}]
    report = {"fecha": datetime.now(timezone.utc).isoformat(), "modelo": await model_info(),
        "codigo_sha256": {p.name: digest(p) for p in sorted((ROOT / "mira").glob("*.py"))},
        "golden_sha256": digest(golden_path), "parafrasis_sha256": digest(extra_path),
        "metodo": "Repetición dirigida de fallos históricos, no muestra independiente ni aprobación del cliente. Revisión semántica separada.",
        "base": "Temporal aislada importada desde el kit original", "consultas": []}
    if not report["modelo"]["disponible"]:
        raise ValueError("Inicia Bonsai antes de ejecutar la regresión real.")
    for number in range(1, repetitions + 1):
        for question in questions:
            result = await answer(question["usuario"], "regresion-" + uuid.uuid4().hex, question["pregunta"])
            if question["id"] == "P07":
                passed = result["estado"] == "evidencia" and any(c["id"] == "POL-DEC@2#s06:01" for c in result["citas"])
            else:
                passed = result["estado"] == "abstencion" and result.get("motivo_abstencion") == "credenciales_no_disponibles" and not result["citas"]
            report["consultas"].append({"id": question["id"], "repeticion": number,
                "pregunta": question["pregunta"], "comprobacion_estructural": passed, "resultado": result})
            (destination / "resultados.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(question["id"], number, result["estado"], "estructura", passed, flush=True)
    return all(q["comprobacion_estructural"] for q in report["consultas"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, required=True)
    parser.add_argument("--repeticiones", type=int, default=3)
    args = parser.parse_args()
    if args.repeticiones < 1:
        parser.error("Indica al menos una repetición.")
    args.salida.mkdir(parents=True, exist_ok=False)
    root = Path(__file__).resolve().parent.parent
    cache = root / ".cache"
    cache.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="regresion-", dir=cache) as directory:
        os.environ["MIRA_DATA_DIR"] = directory
        subprocess.run([sys.executable, "-m", "mira.cli", "preparar"], cwd=root, check=True)
        if not asyncio.run(check(args.salida, args.repeticiones)):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
