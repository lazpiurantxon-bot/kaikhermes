"""API del panel: mismas garantías que el CLI, con auth de propietario."""
import importlib
import shutil
import sys
from pathlib import Path

import pytest

OFFICE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OFFICE_DIR))


@pytest.fixture(scope="module")
def client(tmp_path_factory, request):
    from fastapi.testclient import TestClient
    state = tmp_path_factory.mktemp("panel") / "state"
    state.mkdir()
    for name in ("departamentos.json", "marcas.json", "control.json"):
        shutil.copy(OFFICE_DIR / "seeds" / name, state / name)
    mp = pytest.MonkeyPatch()
    request.addfinalizer(mp.undo)
    mp.setenv("OFICINA_STATE", str(state))
    mp.setenv("PANEL_TOKEN", "token-test")
    mp.setenv("PANEL_CONFIG", str(state / "no-existe.yaml"))
    import panel.server as server
    importlib.reload(server)
    return TestClient(server.app)


AUTH = {"Authorization": "Bearer token-test"}


def test_healthz_sin_auth(client):
    assert client.get("/healthz").json() == {"ok": True}


def test_auth_obligatoria(client):
    assert client.get("/api/estado").status_code == 401
    assert client.get("/api/estado", headers={"Authorization": "Bearer malo"}).status_code == 401


def test_estado(client):
    snap = client.get("/api/estado", headers=AUTH).json()
    assert "departamentos" in snap and "gates_pendientes" in snap


def test_intake_y_ciclo(client):
    t = client.post("/api/intake", json={"texto": "estudia el mercado X", "prioridad": 2},
                    headers=AUTH).json()
    assert t["estado"] == "intake" and t["origen"] == "panel"
    r = client.post(f"/api/tareas/{t['id']}/accion",
                    json={"accion": "asignar", "dept": "mercado"}, headers=AUTH)
    assert r.json()["estado"] == "queued"
    r = client.post(f"/api/tareas/{t['id']}/accion",
                    json={"accion": "nota", "texto": "céntrate en Euskadi"}, headers=AUTH)
    assert r.json()["notas"][0]["texto"] == "céntrate en Euskadi"
    r = client.post(f"/api/tareas/{t['id']}/accion",
                    json={"accion": "archivar", "motivo": "test"}, headers=AUTH)
    assert r.json()["estado"] == "archived"


def test_intake_vacio_409(client):
    r = client.post("/api/intake", json={"texto": "  "}, headers=AUTH)
    assert r.status_code == 409 and "error" in r.json()


def test_departamento_pausa_y_pulso(client):
    r = client.post("/api/departamentos/mercado/accion",
                    json={"accion": "pausar", "motivo": "test"}, headers=AUTH)
    assert r.json()["pausado"] is True
    r = client.post("/api/departamentos/mercado/accion",
                    json={"accion": "reanudar"}, headers=AUTH)
    assert r.json()["pausado"] is False
    r = client.post("/api/departamentos/mercado/accion",
                    json={"accion": "pulso-ahora"}, headers=AUTH)
    assert r.json()["ultimo_pulso"] == "1970-01-01T00:00:00Z"


def test_control_kill(client):
    r = client.post("/api/control", json={"kill": True, "motivo": "test"}, headers=AUTH)
    assert r.json()["kill"] is True
    client.post("/api/control", json={"kill": False}, headers=AUTH)


def test_marca_protegida_desde_panel(client):
    r = client.post("/api/marcas", json={"slug": "vieja", "nombre": "Marca Vieja",
                                         "status": "protected"}, headers=AUTH)
    assert r.json()["enforcement"] == "gate"


def test_gate_decidir(client):
    t = client.post("/api/tareas", json={"titulo": "campaña Y", "dept": "marketing"},
                    headers=AUTH).json()
    import panel.server as server
    server.store.start_task(t["id"], agente="dep-marketing")
    g = server.store.open_gate(t["id"], "R2", "publish", "publicar Y", "", "revert",
                               por="dep-marketing")
    r = client.post(f"/api/gates/{g['id']}/decidir",
                    json={"decision": "aprobado", "nota": "ok"}, headers=AUTH)
    assert r.json()["estado"] == "aprobado"
