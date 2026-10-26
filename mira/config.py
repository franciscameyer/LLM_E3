from pathlib import Path
import os

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
KIT = ROOT / "Kit_Entrega_3_MIRA" / "CU-1_operador_revision"
DATA = Path(os.getenv("MIRA_DATA_DIR", str(ROOT / ".data"))).resolve()
DB = DATA / "mira.sqlite3"
INDEX = DATA / "indice.json"


def ensure_data():
    DATA.mkdir(parents=True, exist_ok=True)

