"""El CLI `oficina` es el contrato de los agentes: se prueba como subproceso."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

OFFICE_DIR = Path(__file__).resolve().parents[1]
CLI = OFFICE_DIR / "bin" / "oficina"


def run(state, *args, por="test"):
    proc = subprocess.run(
        [sys.executable, str(CLI), "--state", str(state), "--por", por, *args],
        capture_output=True, text=True)
    data = json.loads(proc.stdout) if proc.stdout.strip() else {}
    return proc.returncode, data


def seeded(tmp_path):
    state = tmp_path / "state"
    state.mkdir()
    for name in ("departamentos.json", "marcas.json", "control.json"):
        shutil.copy(OFFICE_DIR / "seeds" / name, state / name)
    return state


def test_init_y_estado(tmp_path):
    state = tmp_path / "nuevo"
    code, _ = run(state, "init")
    assert code == 0
    code, snap = run(state, "estado")
    assert code == 0
    assert "mercado" in snap["conteo_por_dept"]


def test_politica_exit_codes(tmp_path):
    state = seeded(tmp_path)
    code, v = run(state, "politica", "check", "--accion-externa", "internal")
    assert code == 0 and v["decision"] == "allow"
    code, v = run(state, "politica", "check", "--accion-externa", "publish", "--marca", "ezti")
    assert code == 3 and v["decision"] == "gate"
    code, v = run(state, "politica", "check", "--accion-externa", "publish", "--marca", "hotel")
    assert code == 4 and v["decision"] == "deny"


def test_flujo_tarea_por_cli(tmp_path):
    state = seeded(tmp_path)
    code, t = run(state, "intake", "add", "analiza el mercado de geles", "--origen", "telegram",
                  por="gabinete")
    assert code == 0 and t["estado"] == "intake"
    tid = t["id"]
    code, t = run(state, "tarea", "asignar", tid, "--dept", "mercado", "--prioridad", "2",
                  por="gabinete")
    assert code == 0 and t["estado"] == "queued"
    code, t = run(state, "tarea", "empezar", tid, por="dep-mercado")
    assert code == 0 and t["agente"] == "dep-mercado"
    code, _ = run(state, "tarea", "artefacto", tid, "--ref", "informe.md", por="dep-mercado")
    assert code == 0
    code, t = run(state, "tarea", "entregar", tid, "--resultado", "informe en informe.md",
                  por="dep-mercado")
    assert code == 0 and t["estado"] == "review"


def test_gate_decidir_requiere_owner_o_cita(tmp_path):
    state = seeded(tmp_path)
    _, t = run(state, "tarea", "crear", "--titulo", "campaña", "--dept", "marketing",
               "--nacer-en", "queued", por="gabinete")
    run(state, "tarea", "empezar", t["id"], por="dep-marketing")
    code, g = run(state, "gate", "abrir", "--tarea", t["id"], "--riesgo", "R2",
                  "--tipo", "publish", "--que", "publicar X", "--rollback", "revert",
                  por="dep-marketing")
    assert code == 0
    code, err = run(state, "gate", "decidir", g["id"], "--decision", "aprobado",
                    por="dep-marketing")
    assert code == 2 and "propietario" in err["error"]
    code, g2 = run(state, "gate", "decidir", g["id"], "--decision", "aprobado",
                   "--aprobacion", "APRUEBO (Telegram)", por="gabinete")
    assert code == 0 and g2["estado"] == "aprobado"


def test_control_owner_only(tmp_path):
    state = seeded(tmp_path)
    code, _ = run(state, "control", "set", "--kill", "on", por="gabinete")
    assert code == 0  # activar la parada la puede pedir cualquiera
    code, err = run(state, "control", "set", "--kill", "off", por="gabinete")
    assert code == 2 and "propietario" in err["error"]
    code, _ = run(state, "control", "set", "--kill", "off", por="owner:panel")
    assert code == 0


def test_por_despues_del_subcomando(tmp_path):
    """Los agentes escriben `--por` al final (como en las skills): debe funcionar."""
    state = seeded(tmp_path)
    proc = subprocess.run(
        [sys.executable, str(CLI), "intake", "add", "hola", "--origen", "telegram",
         "--por", "gabinete", "--state", str(state)],
        capture_output=True, text=True)
    assert proc.returncode == 0
    t = json.loads(proc.stdout)
    assert t["historial"][0]["por"] == "gabinete"


def test_marca_crear_por_agente(tmp_path):
    state = seeded(tmp_path)
    code, b = run(state, "marca", "crear", "--slug", "zephyr", "--nombre", "Zephyr",
                  por="dep-marca")
    assert code == 0 and b["status"] == "office"
    code, v = run(state, "politica", "check", "--accion-externa", "publish", "--marca", "zephyr")
    assert code == 0 and v["decision"] == "allow"
