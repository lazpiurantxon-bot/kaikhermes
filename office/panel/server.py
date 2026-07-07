"""Panel de la oficina Hermes — API + UI estática.

Interfaz del propietario para orquestar, supervisar y usar la oficina:
- intake directo al orquestador (misma bandeja que Telegram),
- cola/kanban de tareas por departamento, agentes en trabajo,
- gates R2/R3 con APRUEBO/RECHAZO,
- pausas por departamento, pulso inmediato, kill switch, presupuesto,
- registro de marcas y feed de actividad.

Todas las mutaciones pasan por core.store (idéntico camino que el CLI
`oficina` de los agentes), con actor 'owner:panel'. El panel escucha en
127.0.0.1 por defecto: acceso vía túnel SSH (ver office/README.md).
"""
from __future__ import annotations

import os
import secrets
from pathlib import Path

import yaml
from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.store import Store, StoreError  # noqa: E402

OWNER = "owner:panel"
STATIC_DIR = Path(__file__).resolve().parent / "static"
DEFAULT_CONFIG = "~/.hermes-office/panel.yaml"


def load_panel_config() -> dict:
    cfg_path = Path(os.environ.get("PANEL_CONFIG", DEFAULT_CONFIG)).expanduser()
    cfg: dict = {}
    if cfg_path.exists():
        cfg = yaml.safe_load(cfg_path.read_text()) or {}
    cfg.setdefault("host", os.environ.get("PANEL_HOST", "127.0.0.1"))
    cfg.setdefault("port", int(os.environ.get("PANEL_PORT", "8787")))
    cfg.setdefault("token", os.environ.get("PANEL_TOKEN", ""))
    cfg.setdefault("state_dir", os.environ.get("OFICINA_STATE", ""))
    if not cfg["token"]:
        # Sin token configurado: se genera uno efímero y se imprime (modo demo).
        cfg["token"] = "demo-" + secrets.token_hex(16)
        print(f"[panel] AVISO: sin token configurado; token efímero: {cfg['token']}")
    return cfg


CONFIG = load_panel_config()
store = Store(CONFIG["state_dir"] or None)
app = FastAPI(title="Hermes Office Panel", docs_url=None, redoc_url=None)


def auth(request: Request):
    header = request.headers.get("authorization", "")
    if not header.startswith("Bearer ") or not secrets.compare_digest(
            header.removeprefix("Bearer ").strip(), CONFIG["token"]):
        raise HTTPException(status_code=401, detail="Token inválido")


@app.exception_handler(StoreError)
async def store_error_handler(_req, exc: StoreError):
    return JSONResponse(status_code=409, content={"error": str(exc)})


@app.get("/healthz")
def healthz():
    return {"ok": True}


# ---- lectura -----------------------------------------------------------------
@app.get("/api/estado", dependencies=[Depends(auth)])
def estado():
    return store.snapshot()


@app.get("/api/tareas/{tid}", dependencies=[Depends(auth)])
def tarea(tid: str):
    return store.get_task(tid)


@app.get("/api/eventos", dependencies=[Depends(auth)])
def eventos(n: int = 100):
    return store.events(limit=min(n, 500))


# ---- intake y tareas -----------------------------------------------------------
@app.post("/api/intake", dependencies=[Depends(auth)])
def intake(body: dict = Body(...)):
    texto = (body.get("texto") or "").strip()
    if not texto:
        raise StoreError("El intake está vacío.")
    t = store.create_task(titulo=texto[:120], descripcion=texto, por=OWNER,
                          origen="panel", estado="intake",
                          prioridad=int(body.get("prioridad") or 3))
    return t


@app.post("/api/tareas", dependencies=[Depends(auth)])
def crear_tarea(body: dict = Body(...)):
    if not (body.get("titulo") or "").strip():
        raise StoreError("Falta el título.")
    return store.create_task(
        titulo=body["titulo"].strip(), descripcion=body.get("desc") or "",
        por=OWNER, origen="owner",
        estado="queued" if body.get("dept") else "intake",
        dept=body.get("dept") or None, prioridad=int(body.get("prioridad") or 3),
        riesgo=body.get("riesgo") or "R0", marca=body.get("marca") or None)


@app.post("/api/tareas/{tid}/accion", dependencies=[Depends(auth)])
def accion_tarea(tid: str, body: dict = Body(...)):
    acc = body.get("accion")
    if acc == "asignar":
        return store.assign_task(tid, body["dept"], OWNER,
                                 prioridad=body.get("prioridad"),
                                 riesgo=body.get("riesgo"))
    if acc == "recolar":
        return store.requeue_task(tid, OWNER, body.get("motivo") or "devuelta a cola")
    if acc == "cerrar":
        return store.close_task(tid, OWNER, resultado=body.get("resultado"))
    if acc == "archivar":
        return store.archive_task(tid, body.get("motivo") or "archivada por el propietario", OWNER)
    if acc == "responder":
        return store.answer_intake(tid, body.get("resultado") or "", OWNER)
    if acc == "nota":
        return store.add_note(tid, body.get("texto") or "", OWNER)
    if acc == "editar":
        return store.update_task_fields(tid, OWNER, prioridad=body.get("prioridad"),
                                        riesgo=body.get("riesgo"), dept=body.get("dept"),
                                        marca=body.get("marca"))
    raise StoreError(f"Acción desconocida: {acc}")


# ---- gates -----------------------------------------------------------------------
@app.post("/api/gates/{gid}/decidir", dependencies=[Depends(auth)])
def decidir_gate(gid: str, body: dict = Body(...)):
    decision = body.get("decision")
    if decision not in ("aprobado", "rechazado"):
        raise StoreError("Decisión inválida: aprobado | rechazado.")
    return store.decide_gate(gid, decision, OWNER, nota=body.get("nota") or "")


# ---- departamentos -----------------------------------------------------------------
@app.post("/api/departamentos/{slug}/accion", dependencies=[Depends(auth)])
def accion_dept(slug: str, body: dict = Body(...)):
    acc = body.get("accion")
    if acc == "pausar":
        return store.update_department(slug, OWNER, pausado=True,
                                       pausado_motivo=body.get("motivo") or "pausado desde el panel")
    if acc == "reanudar":
        return store.update_department(slug, OWNER, pausado=False, pausado_motivo="",
                                       fallos_seguidos=0)
    if acc == "set":
        return store.update_department(slug, OWNER, cadencia_min=body.get("cadencia"),
                                       wip=body.get("wip"),
                                       backlog_objetivo=body.get("backlog"),
                                       mision=body.get("mision"))
    if acc == "pulso-ahora":
        # Fuerza el pulso: el próximo despacho del orquestador lo verá vencido.
        d = store.update_department(slug, OWNER, ultimo_pulso="1970-01-01T00:00:00Z")
        store.event("pulso", f"Pulso inmediato de {slug} solicitado desde el panel; "
                    "se ejecutará en el próximo despacho del orquestador.",
                    ref=slug, actor=OWNER)
        return d
    raise StoreError(f"Acción desconocida: {acc}")


# ---- control global -------------------------------------------------------------
@app.post("/api/control", dependencies=[Depends(auth)])
def control(body: dict = Body(...)):
    return store.set_control(OWNER, **{
        k: body.get(k) for k in ("pausa_global", "kill", "freeze_gasto", "wip_global",
                                 "presupuesto_mes_eur", "limite_tarea_eur", "motivo")
    })


# ---- marcas ---------------------------------------------------------------------
@app.post("/api/marcas", dependencies=[Depends(auth)])
def crear_marca(body: dict = Body(...)):
    status = body.get("status") or "office"
    return store.create_brand(
        body.get("slug") or "", body.get("nombre") or "", OWNER, status=status,
        enforcement="gate" if status == "protected" else "allow",
        notas=body.get("notas") or "")


# ---- UI estática -------------------------------------------------------------------
@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
