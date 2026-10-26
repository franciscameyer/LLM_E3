"""RAG léxico BM25: indexación separada, versiones, secciones y citas estables."""

from collections import Counter
from datetime import date
import hashlib
import json
import math
import re
import unicodedata

from mira.config import DATA, INDEX, KIT, ensure_data

STOP = set("a al ante bajo con contra de del desde el ella en entre es esta este hay la las lo los o para por que se si sin sobre su sus un una y cual como cuando donde quien puedo puede debe".split())
MONTHS = {m: i for i, m in enumerate(
    "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split(), 1,
)}


def tokens(text: str) -> list[str]:
    text = "".join(c for c in unicodedata.normalize("NFD", text.casefold()) if unicodedata.category(c) != "Mn")
    words = re.findall(r"[a-z0-9]+(?:_[a-z0-9]+)*", text)
    return [w for w in words if len(w) > 1 and w not in STOP]


def _date(text):
    match = re.search(r"(\d{1,2}) de (\w+) de (\d{4})", text.casefold())
    if not match:
        return ""
    return date(int(match[3]), MONTHS[match[2]], int(match[1])).isoformat()


def build_chunks(max_chars=1800):
    chunks, inventory = [], []
    for path in sorted((KIT / "corpus").glob("*.md")):
        text = path.read_text(encoding="utf-8-sig")
        header = re.split(r"^##\s+", text, maxsplit=1, flags=re.M)[0]
        fields = dict(re.findall(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", header, re.M))
        code, version = fields["Código"].strip(), fields["Versión"].strip()
        status = "derogada" if "derogad" in fields["Estado"].casefold() else "vigente"
        validity = fields["Vigencia"].strip()
        dates = re.findall(r"\d{1,2} de \w+ de \d{4}", validity)
        meta = {
            "codigo": code, "version": version, "estado": status, "vigencia": validity,
            "desde": _date(dates[0]) if dates else "",
            "hasta": _date(dates[1]) if len(dates) > 1 else "",
            "fuente": path.name, "titulo": text.splitlines()[0].lstrip("# "),
            "origen": "kit docente", "sha256": hashlib.sha256(text.encode()).hexdigest(),
        }
        inventory.append({**meta, "tokens_aproximados": math.ceil(len(text.split()) / 0.75)})
        sections = re.split(r"^##\s+", text, flags=re.M)[1:]
        for number, section in enumerate(sections, 1):
            heading, _, body = section.partition("\n")
            section_id = f"{code}@{version}#s{number:02d}"
            # La separación se decide antes de consultar; el ID conserva su sección.
            parts, current = [], ""
            for line in body.strip().splitlines():
                if current and len(current) + len(line) + 1 > max_chars:
                    parts.append(current)
                    current = ""
                while len(line) > max_chars:
                    if current:
                        parts.append(current)
                        current = ""
                    parts.append(line[:max_chars])
                    line = line[max_chars:]
                current += ("\n" if current else "") + line
            if current.strip():
                parts.append(current.strip())
            for part, body_part in enumerate(parts, 1):
                chunks.append({**meta, "id": f"{section_id}:{part:02d}",
                    "seccion": heading.strip(), "texto": body_part,
                    "texto_busqueda": f"{code} {meta['titulo']} {heading}\n{body_part}"})
    return chunks, inventory


def indexar(max_chars=1800):
    ensure_data()
    chunks, inventory = build_chunks(max_chars)
    data = {"motor": "BM25", "max_chars": max_chars, "documentos": inventory, "fragmentos": chunks}
    temp = INDEX.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(INDEX)
    return {"documentos": len(inventory), "fragmentos": len(chunks), "motor": "BM25"}


def load_index():
    if not INDEX.exists():
        raise ValueError("Falta el índice. Ejecuta: python -m mira.cli preparar")
    return json.loads(INDEX.read_text(encoding="utf-8"))


def vigente(chunk, today=None):
    today = today or date.today().isoformat()
    return (chunk["estado"] == "vigente" and (not chunk["desde"] or chunk["desde"] <= today)
        and (not chunk["hasta"] or today <= chunk["hasta"]))


def buscar(pregunta: str, k=6, incluir_derogados=False, chunks=None) -> dict:
    if not pregunta.strip() or not 1 <= k <= 12:
        raise ValueError("Indica una consulta y k entre 1 y 12.")
    docs = chunks if chunks is not None else load_index()["fragmentos"]
    docs = [d for d in docs if incluir_derogados or vigente(d)]
    query = Counter(tokens(pregunta))
    counts = [Counter(tokens(d["texto_busqueda"])) for d in docs]
    avg = sum(map(lambda c: sum(c.values()), counts)) / max(1, len(docs))
    scores = []
    for d, c in zip(docs, counts):
        score = 0.0
        for term in query:
            n = sum(term in item for item in counts)
            idf = math.log(1 + (len(docs) - n + 0.5) / (n + 0.5))
            tf = c[term]
            score += idf * tf * 2.5 / (tf + 1.5 * (0.25 + 0.75 * sum(c.values()) / max(avg, 1)))
        if score > 0:
            scores.append(({**d, "relevancia": round(score, 4)}, score))
    scores.sort(key=lambda pair: (-pair[1], pair[0]["id"]))
    selected = [d for d, _ in scores[:k]]
    # Relación de conflicto identificada por lectura del corpus; no es una regla de precedencia.
    conflicts = []
    if (re.search(r"umbral|bandeja|puntaje|\b8[025]\b", pregunta, re.I)
            and re.search(r"aprob|autom|manual|pol[ií]tica|bandeja", pregunta, re.I)):
        ids = ["MAN-REV@1#s01:01", "POL-DEC@2#s02:01"]
        pair = [d for d in docs if d["id"] in ids]
        if len(pair) == 2:
            conflicts = [{"id": "CONF-01", "fragmentos": ids,
                "obligatorio": True,
                "descripcion": "MAN-REV vigente afirma aprobación desde 80 sin fraude; POL-DEC v2 fija referencia 85, condiciones por señal y configuración por organización. No elegir una fuente por cuenta propia."}]
            selected = pair + [d for d in selected if d["id"] not in ids]
            selected = selected[:max(k, 2)]
    complementary = []
    pair_ids = {"MAN-REV@1#s01:01", "POL-DEC@2#s02:01"}
    present = {d["id"] for d in selected}
    if present & pair_ids and not conflicts:
        pair = [d for d in docs if d["id"] in pair_ids]
        if len(pair) == 2:
            complementary = [d for d in pair if d["id"] not in present]
            conflicts = [{"id": "CONF-01", "fragmentos": sorted(pair_ids), "obligatorio": False,
                "descripcion": "Alerta de fuente: si usas la regla de aprobación del manual o de la política, presenta ambas y su conflicto 80/85. Si la pregunta trata otro tema, evita añadir esa regla ajena."}]
    return {"fragmentos": selected, "complementarios_conflicto": complementary, "conflictos": conflicts,
        "advertencia": "La relevancia léxica no demuestra que una pregunta tenga respuesta. Verificar evidencia antes de afirmar."}


def fragmento(identifier):
    return next((d for d in load_index()["fragmentos"] if d["id"] == identifier), None)
