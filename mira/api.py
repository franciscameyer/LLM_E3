"""Frontend y API del asistente; todos los datos de negocio pasan por MCP."""

import hmac
import json
import os
import secrets
import time

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from mira import agent, rag
from mira.bridge import call, connection
from mira.config import DATA, ROOT
from mira.security import sign, verify

app = FastAPI(title="MIRA · Revisión asistida", version="0.1.0")
app.mount("/static", StaticFiles(directory=ROOT / "web"), name="static")


class Login(BaseModel):
    usuario_id: str = Field(pattern=r"^U-\d{2}$")
    password: str = Field(max_length=200)


class Chat(BaseModel):
    pregunta: str = Field(min_length=3, max_length=3000)


class Proposal(BaseModel):
    caso_id: str = Field(pattern=r"^C-\d{3}$")
    documentos: str = Field(min_length=5, max_length=1000)
    motivo: str = Field(min_length=10, max_length=1500)


class Confirmation(BaseModel):
    confirmo: bool


def users():
    path = DATA / "usuarios_demo.json"
    if not path.exists():
        raise HTTPException(503, "Prepara primero el proyecto: python -m mira.cli preparar")
    return json.loads(path.read_text(encoding="utf-8"))


async def session(request: Request):
    try:
        payload = verify(request.cookies.get("mira_session", ""), "web")
        if request.method != "GET":
            if not hmac.compare_digest(request.headers.get("X-MIRA-CSRF", ""), payload["csrf"]):
                raise ValueError()
        return payload
    except (ValueError, KeyError):
        raise HTTPException(401, "Inicia sesión de nuevo.") from None


@app.middleware("http")
async def local_origin(request: Request, call_next):
    # Impide formularios externos y DNS rebinding en esta demostración local.
    if request.url.hostname not in {"127.0.0.1", "localhost", "testserver"}:
        return Response("Host no autorizado", status_code=403)
    origin = request.headers.get("origin")
    if request.method not in {"GET", "HEAD", "OPTIONS"} and origin:
        if origin != str(request.base_url).rstrip("/"):
            return Response("Origen no autorizado", status_code=403)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'"
    return response


@app.get("/")
def index():
    return FileResponse(ROOT / "web" / "index.html")


@app.get("/api/status")
async def status():
    return {"modelo": await agent.model_info(), "preparado": (DATA / "importacion.json").exists() and rag.INDEX.exists(),
        "modo": "Demostración local con datos ficticios y contraseña compartida"}


@app.get("/api/usuarios")
def demo_users():
    return users()


login_attempts = {}


@app.post("/api/login")
def login(body: Login, response: Response, request: Request):
    remote = request.client.host if request.client else "local"
    attempts = [stamp for stamp in login_attempts.get(remote, []) if stamp > time.time() - 60]
    if len(attempts) >= 10:
        raise HTTPException(429, "Demasiados intentos. Espera un minuto.")
    known = next((u for u in users() if u["usuario_id"] == body.usuario_id), None)
    if not known or not hmac.compare_digest(body.password, os.getenv("MIRA_DEMO_PASSWORD", "mira-demo")):
        login_attempts[remote] = attempts + [time.time()]
        raise HTTPException(401, "Usuario o contraseña incorrectos.")
    payload = {"purpose": "web", "sub": body.usuario_id, "sid": secrets.token_hex(16), "csrf": secrets.token_hex(24)}
    response.set_cookie("mira_session", sign(payload), httponly=True, samesite="strict", max_age=3600)
    return {"usuario": known, "csrf": payload["csrf"]}


@app.get("/api/session")
def current(payload=Depends(session)):
    user = next((u for u in users() if u["usuario_id"] == payload["sub"]), None)
    if not user:
        raise HTTPException(401, "Usuario no disponible.")
    return {"usuario": user, "csrf": payload["csrf"]}


@app.post("/api/logout")
def logout(response: Response, payload=Depends(session)):
    response.delete_cookie("mira_session")
    return {"ok": True}


async def single(payload, tool, args):
    traces = []
    try:
        async with connection(payload["sub"], payload["sid"]) as client:
            result = await call(client, tool, args, traces)
        return {**result, "trazas": traces}
    except (ValueError, OSError, TimeoutError) as error:
        raise HTTPException(503, f"El servicio MCP no está disponible: {error}") from None


@app.get("/api/casos")
async def cases(payload=Depends(session)):
    return await single(payload, "listar_casos", {})


@app.get("/api/casos/{caso_id}")
async def case(caso_id: str, payload=Depends(session)):
    return await single(payload, "consultar_caso", {"caso_id": caso_id})


@app.post("/api/chat")
async def chat(body: Chat, payload=Depends(session)):
    return await agent.answer(payload["sub"], payload["sid"], body.pregunta)


@app.post("/api/buscar")
async def search(body: Chat, payload=Depends(session)):
    return await single(payload, "buscar_reglas", {"pregunta": body.pregunta})


@app.get("/api/citas/{identifier:path}")
def citation(identifier: str, payload=Depends(session)):
    item = rag.fragmento(identifier)
    if item is None:
        raise HTTPException(404, "Fragmento no disponible.")
    return item


@app.get("/api/propuestas")
async def pending(payload=Depends(session)):
    return await single(payload, "ver_propuestas", {})


@app.post("/api/propuestas")
async def proposal(body: Proposal, payload=Depends(session)):
    return await single(payload, "preparar_solicitud", body.model_dump())


@app.post("/api/propuestas/{accion_id}/confirmar")
async def confirm(accion_id: str, body: Confirmation, payload=Depends(session)):
    if body.confirmo is not True:
        raise HTTPException(400, "La acción requiere confirmación explícita.")
    proof = sign({"purpose": "confirmacion", "sub": payload["sub"], "sid": payload["sid"], "accion": accion_id}, seconds=30)
    return await single(payload, "confirmar_solicitud", {"accion_id": accion_id, "autorizacion": proof})


@app.post("/api/propuestas/{accion_id}/cancelar")
async def cancel(accion_id: str, payload=Depends(session)):
    return await single(payload, "cancelar_propuesta", {"accion_id": accion_id})


@app.get("/api/trazas")
async def traces(payload=Depends(session)):
    return await single(payload, "ver_trazas", {})


@app.get("/api/corpus")
def corpus(payload=Depends(session)):
    return rag.load_index()["documentos"]
