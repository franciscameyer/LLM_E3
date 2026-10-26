"""Cliente MCP real por STDIO; la API web nunca consulta SQLite directamente."""

from contextlib import asynccontextmanager
import os
import sys

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from mira.config import DATA, ROOT
from mira.security import sign

MODEL_TOOLS = {"buscar_reglas", "listar_casos", "consultar_caso", "listar_senales", "preparar_solicitud"}


@asynccontextmanager
async def connection(uid: str, sid: str):
    transport = StdioTransport(
        command=sys.executable, args=["-m", "mira.mcp_server"], cwd=str(ROOT),
        env={"MIRA_PRINCIPAL_TOKEN": sign({"purpose": "mcp", "sub": uid, "sid": sid}),
            "MIRA_DATA_DIR": str(DATA), "PYTHONIOENCODING": "utf-8",
            "FASTMCP_CHECK_FOR_UPDATES": "off", "FASTMCP_SHOW_SERVER_BANNER": "false",
            "TEMP": os.getenv("TEMP", str(ROOT / ".cache" / "tmp")),
            "TMP": os.getenv("TMP", str(ROOT / ".cache" / "tmp"))},
        keep_alive=False,
    )
    async with Client(transport, timeout=30, init_timeout=20) as client:
        yield client


async def call(client, name, args, traces=None):
    result = (await client.call_tool(name, args)).data
    if not isinstance(result, dict) or "ok" not in result:
        raise ValueError("El servidor MCP devolvió un contrato inválido.")
    if traces is not None:
        traces.append(result["traza"])
    return result


async def schemas(client):
    return [{"type": "function", "function": {"name": t.name,
        "description": t.description, "parameters": t.inputSchema}}
        for t in await client.list_tools() if t.name in MODEL_TOOLS]
