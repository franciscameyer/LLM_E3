"""Verificación MCP externa y consultas exploratorias en una base temporal propia."""

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


async def check(generation):
    from mira.agent import answer, model_info
    from mira.bridge import call, connection
    from mira.validation import digest
    from mira.config import ROOT

    report = {"fecha": datetime.now(timezone.utc).isoformat(),
        "base": "Temporal aislada, importada desde el Excel original; no se usa la base de la demo.",
        "codigo_sha256": {p.name: digest(p) for p in sorted((ROOT / "mira").glob("*.py"))},
        "modelo": await model_info(), "consultas": [], "revision_semantica": "Pendiente; las respuestas se conservan sin atribuirles aprobación automática."}
    async with connection("U-01", "verificacion-externa-" + uuid.uuid4().hex) as client:
        report["mcp"] = {"tools": [t.model_dump(mode="json") for t in await client.list_tools()],
            "resources": [r.model_dump(mode="json") for r in await client.list_resources()],
            "prompts": [p.model_dump(mode="json") for p in await client.list_prompts()]}
        report["denegacion_organizacion"] = await call(client, "consultar_caso", {"caso_id": "C-020"})
        report["limite_solicitudes"] = await call(client, "preparar_solicitud", {
            "caso_id": "C-016", "documentos": "Boleta original legible", "motivo": "No se distingue el total del documento."})
        proposal = await call(client, "preparar_solicitud", {
            "caso_id": "C-011", "documentos": "Boleta original legible", "motivo": "No se distingue el total del documento."})
        report["preparacion_sin_confirmacion"] = proposal
        assert proposal["ok"] and proposal["datos"]["requiere_confirmacion"]
        report["cancelacion"] = await call(client, "cancelar_propuesta", {"accion_id": proposal["datos"]["accion_id"]})
        assert not report["denegacion_organizacion"]["ok"]
        assert not report["limite_solicitudes"]["ok"]
    if generation and report["modelo"]["disponible"]:
        source = ROOT / "evaluation/parafrasis.json"
        report["parafrasis_sha256"] = digest(source)
        for q in json.loads(source.read_text(encoding="utf-8"))["preguntas"]:
            print(q["id"], flush=True)
            report["consultas"].append({**q, "resultado": await answer(q["usuario"], "exploracion-" + q["id"], q["pregunta"])})
    report["generacion_ejecutada"] = bool(report["consultas"])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, required=True)
    parser.add_argument("--generacion", action="store_true")
    args = parser.parse_args()
    if args.salida.exists():
        parser.error("La salida ya existe; usa un nombre nuevo.")
    root = Path(__file__).resolve().parent.parent
    cache = root / ".cache"
    cache.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="verificacion-", dir=cache) as directory:
        os.environ["MIRA_DATA_DIR"] = directory
        subprocess.run([sys.executable, "-m", "mira.cli", "preparar"], cwd=root, check=True)
        # Importar después de fijar el directorio; los módulos capturan DATA al cargarse.
        report = asyncio.run(check(args.generacion))
        from mira.validation import write_json
        write_json(args.salida, report)
    print(args.salida)


if __name__ == "__main__":
    main()
