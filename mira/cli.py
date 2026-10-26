import argparse
import asyncio
import json
import os
import sys
import uuid

from mira.config import DATA


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="MIRA CU-1 · herramientas de desarrollo")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("preparar", help="Importar Excel e indexar documentos sin alterar el kit")
    sub.add_parser("servir", help="Iniciar la aplicación web en localhost")
    sub.add_parser("estado", help="Comprobar el servidor del modelo local")
    search = sub.add_parser("buscar", help="Recuperar fragmentos sin llamar al modelo")
    search.add_argument("pregunta")
    ask = sub.add_parser("preguntar", help="Consultar al modelo con el servidor MCP real")
    ask.add_argument("pregunta")
    ask.add_argument("--usuario", default="U-01")
    mcp = sub.add_parser("mcp", help="Iniciar servidor para un cliente MCP externo local de prueba")
    mcp.add_argument("--usuario", required=True)
    mcp.add_argument("--sesion", default="cliente-externo")
    evaluate = sub.add_parser("evaluar", help="Medir Recall@k y comparar fragmentación")
    evaluate.add_argument("--generacion", action="store_true", help="Ejecutar también las 20 preguntas con el modelo; puede tardar")
    args = parser.parse_args()
    try:
        if args.command == "preparar":
            from mira.rag import indexar
            from mira.security import secret
            from mira.store import cargar_kit
            secret()
            print(json.dumps({"datos": cargar_kit(), "rag": indexar()}, ensure_ascii=False, indent=2))
        elif args.command == "servir":
            import uvicorn
            uvicorn.run("mira.api:app", host=os.getenv("MIRA_HOST", "127.0.0.1"), port=int(os.getenv("MIRA_PORT", "8000")))
        elif args.command == "estado":
            from mira.agent import model_info
            print(json.dumps(asyncio.run(model_info()), ensure_ascii=False, indent=2))
        elif args.command == "buscar":
            from mira.rag import buscar
            print(json.dumps(buscar(args.pregunta), ensure_ascii=False, indent=2))
        elif args.command == "preguntar":
            from mira.agent import answer
            print(json.dumps(asyncio.run(answer(args.usuario, "terminal-" + uuid.uuid4().hex, args.pregunta)), ensure_ascii=False, indent=2))
        elif args.command == "mcp":
            from mira.mcp_server import mcp
            from mira.security import sign
            available = json.loads((DATA / "usuarios_demo.json").read_text(encoding="utf-8"))
            if args.usuario not in {u["usuario_id"] for u in available}:
                raise ValueError("Usuario del kit no disponible.")
            os.environ["MIRA_PRINCIPAL_TOKEN"] = sign({"purpose": "mcp", "sub": args.usuario, "sid": args.sesion})
            mcp.run(transport="stdio", show_banner=False)
        elif args.command == "evaluar":
            from mira.evaluate import evaluate
            asyncio.run(evaluate(args.generacion))
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
