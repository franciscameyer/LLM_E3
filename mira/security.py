"""Identidades locales de demostración y autorizaciones firmadas por el backend."""

import base64
import hashlib
import hmac
import json
import secrets
import time

from mira.config import DATA, ensure_data


def secret() -> bytes:
    ensure_data()
    path = DATA / "session.key"
    try:
        with path.open("xb") as f:
            f.write(secrets.token_bytes(32))
    except FileExistsError:
        pass
    return path.read_bytes()


def sign(payload: dict, seconds: int = 3600) -> str:
    body = base64.urlsafe_b64encode(json.dumps(
        {**payload, "exp": int(time.time()) + seconds}, separators=(",", ":"),
    ).encode()).decode().rstrip("=")
    signature = hmac.new(secret(), body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{signature}"


def verify(token: str, purpose: str) -> dict:
    try:
        body, signature = token.split(".")
        expected = hmac.new(secret(), body.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError()
        payload = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
        if payload.get("purpose") != purpose or payload["exp"] <= time.time():
            raise ValueError()
        return payload
    except (ValueError, KeyError, TypeError):
        raise ValueError("Sesión o autorización no válida o vencida.") from None

