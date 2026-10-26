"""Lanza la instalación existente de Bonsai sin cambiar el PATH global."""

import argparse
import os
from pathlib import Path
import subprocess

from mira.config import ROOT  # carga .env si existe


def main():
    base = Path.home() / "Desktop" / "Bonsai" / "llama-prism-b10743-adfffbe-bin-win-cuda-12.4-x64"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server", default=os.getenv("LLAMA_SERVER", str(base / "llama-server.exe")))
    parser.add_argument("--model", default=os.getenv("LLAMA_MODEL", str(base / "Bonsai-27B" / "Ternary-Bonsai-2-27B-PQ2_0.gguf")))
    parser.add_argument("--cuda12", default=str(Path.home() / "miniconda3" / "Lib" / "site-packages" / "torch" / "lib"))
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    for value in (args.server, args.model):
        if not Path(value).is_file():
            parser.error(f"No existe: {value}. Configura --server o --model.")
    environment = os.environ.copy()
    if (Path(args.cuda12) / "cudart64_12.dll").exists():
        environment["PATH"] = args.cuda12 + os.pathsep + environment.get("PATH", "")
    command = [args.server, "--model", args.model, "--alias", "bonsai-27b",
        "--host", "127.0.0.1", "--port", str(args.port), "--ctx-size", "8192", "--parallel", "1",
        "--n-gpu-layers", "all", "--cache-type-k", "q4_0", "--cache-type-v", "q4_0",
        "--flash-attn", "on", "--batch-size", "512", "--ubatch-size", "128", "--jinja", "--reasoning", "off"]
    try:
        return subprocess.run(command, env=environment, check=False).returncode
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
