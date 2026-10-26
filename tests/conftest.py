import pytest

from mira import bridge, config, rag, security, store


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    path = tmp_path / "data"
    path.mkdir()
    monkeypatch.setattr(config, "DATA", path)
    monkeypatch.setattr(config, "DB", path / "mira.sqlite3")
    monkeypatch.setattr(config, "INDEX", path / "indice.json")
    for module in [bridge, rag, security, store]:
        monkeypatch.setattr(module, "DATA", path)
    monkeypatch.setattr(store, "DB", path / "mira.sqlite3")
    monkeypatch.setattr(rag, "INDEX", path / "indice.json")
    from mira import api
    monkeypatch.setattr(api, "DATA", path)
    monkeypatch.setenv("MIRA_DATA_DIR", str(path))
    security.secret()
    store.cargar_kit()
    rag.indexar()
    yield path
