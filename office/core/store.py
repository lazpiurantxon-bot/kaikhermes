"""Tablero de la oficina: estado en archivos JSON bajo `~/office/state`.

Por qué archivos y no un servicio: el sustrato de la oficina es Hermes Agent;
sus subagentes trabajan con shell y archivos con naturalidad, el estado queda
inspeccionable a simple vista (y respaldable con `tar`/git), y no añade ningún
demonio más al sistema. El CLI `oficina` y el panel web escriben a través de
este módulo, nunca a mano.

Concurrencia: un lock global (flock) por mutación. El volumen del tablero es
de decenas de operaciones por minuto como mucho; la simplicidad gana.

Layout:
  state/
    control.json         # pausa global, kill switch, presupuesto, WIP global
    departamentos.json   # roster de departamentos (cadencia, WIP, pausas)
    marcas.json          # registro de marcas (protegidas / de oficina)
    contadores.json      # ids secuenciales
    tareas/T-0001.json   # una tarea por archivo (con notas e historial)
    gates/G-0001.json
    eventos.jsonl        # feed de actividad (append-only)
    ledger/gastos.jsonl  # € reales (append-only)
"""
from __future__ import annotations

import fcntl
import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from . import policy

DEFAULT_STATE_DIR = "~/office/state"

TASK_STATES = ["intake", "queued", "running", "review", "gate", "blocked", "done", "archived"]

# Transiciones permitidas (de → a). Todo lo demás es error de protocolo.
TRANSITIONS = {
    "intake": {"queued", "done", "archived"},
    "queued": {"running", "intake", "archived"},
    "running": {"review", "gate", "blocked", "queued"},
    "gate": {"queued", "review", "archived"},
    "review": {"done", "queued", "archived"},
    "blocked": {"queued", "archived"},
    "done": {"archived"},
    "archived": set(),
}

GATE_STATES = ["pendiente", "aprobado", "rechazado"]
RISKS = ["R0", "R1", "R2", "R3"]
ORIGINS = ["owner", "panel", "telegram", "proactivo", "orquestador", "agente"]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def month_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


class StoreError(Exception):
    """Error de protocolo del tablero (transición inválida, WIP, pausa…)."""


class Store:
    def __init__(self, state_dir: str | Path | None = None):
        raw = state_dir or os.environ.get("OFICINA_STATE") or DEFAULT_STATE_DIR
        self.dir = Path(raw).expanduser()
        self.tasks_dir = self.dir / "tareas"
        self.gates_dir = self.dir / "gates"
        self.ledger_dir = self.dir / "ledger"
        for d in (self.dir, self.tasks_dir, self.gates_dir, self.ledger_dir):
            d.mkdir(parents=True, exist_ok=True)
        self._lock_path = self.dir / ".lock"
        self._lock_path.touch(exist_ok=True)

    # -- primitivas ----------------------------------------------------------
    @contextmanager
    def lock(self):
        with open(self._lock_path, "r+") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(fh, fcntl.LOCK_UN)

    @staticmethod
    def _read(path: Path, default):
        if not path.exists():
            return default
        return json.loads(path.read_text() or "null") or default

    @staticmethod
    def _write(path: Path, data):
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n")
        os.replace(tmp, path)

    def _append_jsonl(self, path: Path, obj: dict):
        with open(path, "a") as fh:
            fh.write(json.dumps(obj, ensure_ascii=False) + "\n")

    def _next_id(self, kind: str, prefix: str) -> str:
        path = self.dir / "contadores.json"
        counters = self._read(path, {})
        counters[kind] = int(counters.get(kind, 0)) + 1
        self._write(path, counters)
        return f"{prefix}-{counters[kind]:04d}"

    # -- control global -------------------------------------------------------
    def control(self) -> dict:
        return self._read(self.dir / "control.json", {})

    def set_control(self, por: str, **flags) -> dict:
        with self.lock():
            ctl = self.control()
            allowed = {"pausa_global", "kill", "freeze_gasto", "wip_global",
                       "presupuesto_mes_eur", "limite_tarea_eur", "motivo"}
            for k, v in flags.items():
                if k in allowed and v is not None:
                    ctl[k] = v
            ctl["actualizado"] = now_iso()
            self._write(self.dir / "control.json", ctl)
        self.event("control", f"Control actualizado por {por}: "
                   + ", ".join(f"{k}={v}" for k, v in flags.items() if v is not None), actor=por)
        return ctl

    def assert_agent_writable(self):
        """Los agentes no mutan el tablero con el kill switch echado o pausa global."""
        ctl = self.control()
        if ctl.get("kill"):
            raise StoreError("KILL SWITCH activo: la oficina está detenida. No mutes el tablero; "
                             "termina tu sesión e informa.")
        if ctl.get("pausa_global"):
            raise StoreError("Pausa global activa: no arranques ni muevas trabajo. "
                             "Solo el propietario puede reanudar.")

    # -- eventos ---------------------------------------------------------------
    def event(self, tipo: str, mensaje: str, ref: str | None = None, actor: str = "sistema"):
        self._append_jsonl(self.dir / "eventos.jsonl",
                           {"ts": now_iso(), "tipo": tipo, "ref": ref, "actor": actor,
                            "mensaje": mensaje})

    def events(self, limit: int = 100) -> list[dict]:
        path = self.dir / "eventos.jsonl"
        if not path.exists():
            return []
        lines = path.read_text().strip().splitlines()[-limit:]
        return [json.loads(l) for l in reversed(lines)]

    # -- departamentos -----------------------------------------------------------
    def departments(self) -> dict:
        return self._read(self.dir / "departamentos.json", {})

    def save_departments(self, depts: dict):
        self._write(self.dir / "departamentos.json", depts)

    def update_department(self, slug: str, por: str, **fields) -> dict:
        with self.lock():
            depts = self.departments()
            if slug not in depts:
                raise StoreError(f"Departamento desconocido: {slug}")
            allowed = {"pausado", "pausado_motivo", "cadencia_min", "wip",
                       "backlog_objetivo", "ultimo_pulso", "fallos_seguidos", "mision"}
            for k, v in fields.items():
                if k in allowed and v is not None:
                    depts[slug][k] = v
            self.save_departments(depts)
        self.event("departamento", f"{slug} actualizado por {por}: "
                   + ", ".join(f"{k}={v}" for k, v in fields.items() if v is not None), actor=por)
        return depts[slug]

    def due_pulses(self) -> list[dict]:
        """Departamentos cuyo pulso proactivo toca: cadencia vencida, sin pausa,
        y con hueco en su backlog (queued+running < backlog_objetivo)."""
        ctl = self.control()
        if ctl.get("kill") or ctl.get("pausa_global"):
            return []
        out = []
        now = datetime.now(timezone.utc)
        for slug, d in self.departments().items():
            if d.get("orquestador") or d.get("pausado"):
                continue
            last = d.get("ultimo_pulso")
            if last:
                elapsed = (now - datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ")
                           .replace(tzinfo=timezone.utc)).total_seconds() / 60
                if elapsed < float(d.get("cadencia_min", 1440)):
                    continue
            active = len(self.list_tasks(dept=slug, states=("queued", "running")))
            if active >= int(d.get("backlog_objetivo", 3)):
                continue
            out.append({"slug": slug, **d})
        return out

    def mark_pulse(self, slug: str, por: str):
        self.update_department(slug, por, ultimo_pulso=now_iso())

    # -- marcas -------------------------------------------------------------------
    def brands(self) -> dict:
        return self._read(self.dir / "marcas.json", {})

    def brand(self, slug: str | None) -> dict | None:
        if not slug:
            return None
        b = self.brands().get(slug)
        return {"slug": slug, **b} if b else None

    def create_brand(self, slug: str, nombre: str, por: str, status: str = "office",
                     enforcement: str = "allow", notas: str = "") -> dict:
        slug = slug.strip().lower()
        if not slug or not slug.replace("-", "").isalnum():
            raise StoreError("Slug de marca inválido (usa minúsculas, dígitos y guiones).")
        with self.lock():
            brands = self.brands()
            if slug in brands:
                raise StoreError(f"La marca '{slug}' ya existe ({brands[slug]['status']}).")
            if status == "protected" and not por.startswith("owner"):
                raise StoreError("Solo el propietario registra marcas protegidas.")
            if status == "office":
                enforcement = "allow"
            brands[slug] = {"nombre": nombre, "status": status, "enforcement": enforcement,
                            "notas": notas, "creada_por": por, "creada": now_iso()}
            self._write(self.dir / "marcas.json", brands)
        self.event("marca", f"Marca '{slug}' ({nombre}) registrada como {status} por {por}",
                   ref=slug, actor=por)
        return {"slug": slug, **brands[slug]}

    # -- política -------------------------------------------------------------------
    def check_action(self, accion: str, marca: str | None = None,
                     importe: float | None = None) -> policy.Verdict:
        ctl = self.control()
        return policy.evaluate(
            accion, self.brand(marca), amount_eur=importe,
            per_task_limit_eur=float(ctl.get("limite_tarea_eur", 20)),
            spend_freeze=bool(ctl.get("freeze_gasto")),
        )

    # -- tareas -----------------------------------------------------------------------
    def _task_path(self, tid: str) -> Path:
        if "/" in tid or "\\" in tid or ".." in tid:
            raise StoreError(f"Id de tarea inválido: {tid}")
        return self.tasks_dir / f"{tid}.json"

    def get_task(self, tid: str) -> dict:
        path = self._task_path(tid)
        if not path.exists():
            raise StoreError(f"Tarea inexistente: {tid}")
        return self._read(path, {})

    def list_tasks(self, estado: str | None = None, dept: str | None = None,
                   states: tuple = ()) -> list[dict]:
        out = []
        for f in sorted(self.tasks_dir.glob("T-*.json")):
            t = self._read(f, {})
            if estado and t.get("estado") != estado:
                continue
            if states and t.get("estado") not in states:
                continue
            if dept and t.get("dept") != dept:
                continue
            out.append(t)
        out.sort(key=lambda t: (int(t.get("prioridad", 3)), t.get("creada", "")))
        return out

    def create_task(self, titulo: str, por: str, descripcion: str = "",
                    origen: str = "agente", estado: str = "intake",
                    dept: str | None = None, prioridad: int = 3, riesgo: str = "R0",
                    marca: str | None = None, padre: str | None = None) -> dict:
        if estado not in ("intake", "queued"):
            raise StoreError("Una tarea nace en 'intake' o directamente en 'queued'.")
        if estado == "queued" and not dept:
            raise StoreError("Para nacer en cola la tarea necesita departamento.")
        if dept and dept not in self.departments():
            raise StoreError(f"Departamento desconocido: {dept}")
        if riesgo not in RISKS:
            raise StoreError(f"Riesgo inválido: {riesgo}")
        with self.lock():
            tid = self._next_id("tarea", "T")
            task = {
                "id": tid, "titulo": titulo.strip(), "descripcion": descripcion,
                "origen": origen, "estado": estado, "dept": dept,
                "prioridad": int(prioridad), "riesgo": riesgo, "marca": marca,
                "padre": padre, "agente": None, "resultado": None,
                "artefactos": [], "notas": [],
                "historial": [{"ts": now_iso(), "a": estado, "por": por, "motivo": "creación"}],
                "creada": now_iso(), "actualizada": now_iso(),
            }
            self._write(self._task_path(tid), task)
        self.event("tarea", f"{tid} creada ({origen}, {estado}"
                   + (f", dept {dept}" if dept else "") + f"): {titulo}", ref=tid, actor=por)
        return task

    def _transition(self, task: dict, nuevo: str, por: str, motivo: str = ""):
        actual = task["estado"]
        if nuevo not in TRANSITIONS.get(actual, set()):
            raise StoreError(f"Transición inválida {actual} → {nuevo} en {task['id']}.")
        task["estado"] = nuevo
        task["actualizada"] = now_iso()
        task["historial"].append({"ts": now_iso(), "de": actual, "a": nuevo,
                                  "por": por, "motivo": motivo})

    def update_task_fields(self, tid: str, por: str, **fields) -> dict:
        allowed = {"titulo", "descripcion", "prioridad", "riesgo", "marca", "dept"}
        with self.lock():
            task = self.get_task(tid)
            changed = []
            for k, v in fields.items():
                if k in allowed and v is not None:
                    if k == "dept" and v not in self.departments():
                        raise StoreError(f"Departamento desconocido: {v}")
                    task[k] = int(v) if k == "prioridad" else v
                    changed.append(k)
            task["actualizada"] = now_iso()
            self._write(self._task_path(tid), task)
        if changed:
            self.event("tarea", f"{tid} editada por {por}: {', '.join(changed)}",
                       ref=tid, actor=por)
        return task

    def assign_task(self, tid: str, dept: str, por: str, prioridad: int | None = None,
                    riesgo: str | None = None, marca: str | None = None) -> dict:
        with self.lock():
            task = self.get_task(tid)
            if dept not in self.departments():
                raise StoreError(f"Departamento desconocido: {dept}")
            self._transition(task, "queued", por, f"asignada a {dept}")
            task["dept"] = dept
            if prioridad is not None:
                task["prioridad"] = int(prioridad)
            if riesgo:
                if riesgo not in RISKS:
                    raise StoreError(f"Riesgo inválido: {riesgo}")
                task["riesgo"] = riesgo
            if marca:
                task["marca"] = marca
            self._write(self._task_path(tid), task)
        self.event("triaje", f"{tid} → {dept} (prioridad {task['prioridad']}, "
                   f"riesgo {task['riesgo']})", ref=tid, actor=por)
        return task

    def start_task(self, tid: str, agente: str) -> dict:
        """Un subagente toma la tarea. Aplica pausa/kill, pausa de dept y WIP."""
        self.assert_agent_writable()
        with self.lock():
            task = self.get_task(tid)
            dept_slug = task.get("dept")
            depts = self.departments()
            dept = depts.get(dept_slug or "")
            if not dept:
                raise StoreError(f"{tid} no tiene departamento asignado.")
            if dept.get("pausado"):
                raise StoreError(f"Departamento {dept_slug} en pausa: "
                                 f"{dept.get('pausado_motivo', 'sin motivo')}.")
            ctl = self.control()
            wip_global = int(ctl.get("wip_global", 2))
            running_all = self.list_tasks(estado="running")
            if len(running_all) >= wip_global:
                raise StoreError(f"WIP global alcanzado ({wip_global}): espera a que algo termine.")
            running_dept = [t for t in running_all if t.get("dept") == dept_slug]
            if len(running_dept) >= int(dept.get("wip", 2)):
                raise StoreError(f"WIP de {dept_slug} alcanzado ({dept.get('wip', 2)}).")
            self._transition(task, "running", agente, "trabajo iniciado")
            task["agente"] = agente
            self._write(self._task_path(tid), task)
        self.event("tarea", f"{tid} en curso — agente {agente}", ref=tid, actor=agente)
        return task

    def deliver_task(self, tid: str, resultado: str, por: str) -> dict:
        with self.lock():
            task = self.get_task(tid)
            self._transition(task, "review", por, "entregada")
            task["resultado"] = resultado
            task["agente"] = None
            self._write(self._task_path(tid), task)
            if task.get("dept"):
                depts = self.departments()
                if task["dept"] in depts:
                    depts[task["dept"]]["fallos_seguidos"] = 0
                    self.save_departments(depts)
        self.event("tarea", f"{tid} entregada a revisión por {por}", ref=tid, actor=por)
        return task

    def fail_task(self, tid: str, motivo: str, por: str) -> dict:
        """Fallo de ejecución. Tres seguidos en un dept → breaker: dept en pausa."""
        with self.lock():
            task = self.get_task(tid)
            self._transition(task, "blocked", por, f"fallo: {motivo}")
            task["agente"] = None
            self._write(self._task_path(tid), task)
            dept_slug = task.get("dept")
            breaker = False
            if dept_slug:
                depts = self.departments()
                d = depts.get(dept_slug)
                if d is not None:
                    d["fallos_seguidos"] = int(d.get("fallos_seguidos", 0)) + 1
                    if d["fallos_seguidos"] >= 3 and not d.get("pausado"):
                        d["pausado"] = True
                        d["pausado_motivo"] = "circuit breaker: 3 fallos consecutivos"
                        breaker = True
                    self.save_departments(depts)
        self.event("tarea", f"{tid} bloqueada: {motivo}", ref=tid, actor=por)
        if breaker:
            self.event("breaker", f"Departamento {dept_slug} PAUSADO por 3 fallos consecutivos. "
                       "Requiere revisión del propietario u orquestador.", ref=dept_slug,
                       actor="sistema")
        return task

    def close_task(self, tid: str, por: str, resultado: str | None = None) -> dict:
        with self.lock():
            task = self.get_task(tid)
            self._transition(task, "done", por, "cerrada")
            if resultado:
                task["resultado"] = resultado
            self._write(self._task_path(tid), task)
        self.event("tarea", f"{tid} cerrada por {por}", ref=tid, actor=por)
        return task

    def archive_task(self, tid: str, motivo: str, por: str) -> dict:
        with self.lock():
            task = self.get_task(tid)
            self._transition(task, "archived", por, motivo or "archivada")
            task["agente"] = None
            self._write(self._task_path(tid), task)
        self.event("tarea", f"{tid} archivada por {por}: {motivo}", ref=tid, actor=por)
        return task

    def requeue_task(self, tid: str, por: str, motivo: str = "devuelta a cola") -> dict:
        with self.lock():
            task = self.get_task(tid)
            self._transition(task, "queued", por, motivo)
            task["agente"] = None
            self._write(self._task_path(tid), task)
        self.event("tarea", f"{tid} devuelta a cola por {por}: {motivo}", ref=tid, actor=por)
        return task

    def answer_intake(self, tid: str, respuesta: str, por: str) -> dict:
        """El orquestador responde una entrada directamente, sin delegarla."""
        with self.lock():
            task = self.get_task(tid)
            self._transition(task, "done", por, "respuesta directa del orquestador")
            task["resultado"] = respuesta
            self._write(self._task_path(tid), task)
        self.event("triaje", f"{tid} respondida directamente por {por}", ref=tid, actor=por)
        return task

    def add_note(self, tid: str, texto: str, autor: str) -> dict:
        with self.lock():
            task = self.get_task(tid)
            task["notas"].append({"ts": now_iso(), "autor": autor, "texto": texto})
            task["actualizada"] = now_iso()
            self._write(self._task_path(tid), task)
        self.event("nota", f"Nota de {autor} en {tid}", ref=tid, actor=autor)
        return task

    def add_artifact(self, tid: str, ref: str, tipo: str, nota: str, por: str) -> dict:
        with self.lock():
            task = self.get_task(tid)
            task["artefactos"].append({"ts": now_iso(), "tipo": tipo, "ref": ref, "nota": nota})
            task["actualizada"] = now_iso()
            self._write(self._task_path(tid), task)
        self.event("artefacto", f"{tid}: {tipo} → {ref}", ref=tid, actor=por)
        return task

    # -- gates ------------------------------------------------------------------------
    def _gate_path(self, gid: str) -> Path:
        if "/" in gid or "\\" in gid or ".." in gid:
            raise StoreError(f"Id de gate inválido: {gid}")
        return self.gates_dir / f"{gid}.json"

    def get_gate(self, gid: str) -> dict:
        path = self._gate_path(gid)
        if not path.exists():
            raise StoreError(f"Gate inexistente: {gid}")
        return self._read(path, {})

    def list_gates(self, estado: str | None = None) -> list[dict]:
        out = []
        for f in sorted(self.gates_dir.glob("G-*.json")):
            g = self._read(f, {})
            if estado and g.get("estado") != estado:
                continue
            out.append(g)
        out.sort(key=lambda g: g.get("creado", ""), reverse=True)
        return out

    def open_gate(self, tarea: str, riesgo: str, tipo: str, que: str, porque: str,
                  rollback: str, por: str) -> dict:
        if riesgo not in ("R2", "R3"):
            raise StoreError("Un gate es R2 o R3; lo demás no necesita gate.")
        if not que.strip() or not rollback.strip():
            raise StoreError("Un gate sin 'qué' o sin rollback no está listo para pedirse "
                             "(doc 06 §5: si el rollback no cabe en 2 líneas, no está listo).")
        with self.lock():
            task = self.get_task(tarea)
            gid = self._next_id("gate", "G")
            gate = {"id": gid, "tarea": tarea, "riesgo": riesgo, "tipo": tipo,
                    "que": que, "porque": porque, "rollback": rollback,
                    "estado": "pendiente", "abierto_por": por, "nota_decision": None,
                    "decidido": None, "creado": now_iso()}
            self._write(self._gate_path(gid), gate)
            if task["estado"] == "running":
                self._transition(task, "gate", por, f"gate {gid} abierto")
                task["agente"] = None
                self._write(self._task_path(tarea), task)
        self.event("gate", f"[GATE {riesgo}] {gid} — {que}", ref=gid, actor=por)
        return gate

    def decide_gate(self, gid: str, decision: str, por: str, nota: str = "",
                    aprobacion_ref: str = "") -> dict:
        """Decisión del propietario. `por` debe ser el propietario (panel) o el
        orquestador citando la aprobación literal recibida por Telegram."""
        if decision not in ("aprobado", "rechazado"):
            raise StoreError("Decisión inválida: aprobado | rechazado.")
        if not por.startswith("owner") and not aprobacion_ref.strip():
            raise StoreError("Solo el propietario decide gates. Si transcribes una decisión "
                             "de Telegram, cita el mensaje literal en --aprobacion.")
        with self.lock():
            gate = self.get_gate(gid)
            if gate["estado"] != "pendiente":
                raise StoreError(f"El gate {gid} ya está {gate['estado']}.")
            gate["estado"] = decision
            gate["nota_decision"] = (nota + (f" [ref: {aprobacion_ref}]" if aprobacion_ref else "")).strip()
            gate["decidido"] = now_iso()
            self._write(self._gate_path(gid), gate)
            task = self.get_task(gate["tarea"])
            if task["estado"] == "gate":
                if decision == "aprobado":
                    self._transition(task, "queued", por, f"gate {gid} aprobado → ejecutar")
                else:
                    self._transition(task, "review", por, f"gate {gid} rechazado")
                self._write(self._task_path(task["id"]), task)
        self.event("gate", f"{gid} {decision.upper()} por {por}"
                   + (f": {nota}" if nota else ""), ref=gid, actor=por)
        return gate

    # -- ledger de € reales --------------------------------------------------------
    def add_spend(self, importe: float, por: str, tarea: str | None = None,
                  nota: str = "") -> dict:
        verdict = self.check_action("spend", importe=importe)
        entry = {"ts": now_iso(), "mes": month_key(), "importe_eur": float(importe),
                 "tarea": tarea, "nota": nota, "por": por, "veredicto": verdict.decision}
        if verdict.decision != "allow":
            raise StoreError(f"Gasto no autorizado por política: {verdict.reason} "
                             "Abre un gate R3 con el importe y el porqué.")
        with self.lock():
            self._append_jsonl(self.ledger_dir / "gastos.jsonl", entry)
            total = self.month_spend()
            ctl = self.control()
            techo = float(ctl.get("presupuesto_mes_eur", 100))
            if techo > 0 and total >= 0.8 * techo and not ctl.get("freeze_gasto"):
                ctl["freeze_gasto"] = True
                ctl["actualizado"] = now_iso()
                self._write(self.dir / "control.json", ctl)
                self.event("breaker", f"Gasto mensual {total:.2f} € ≥ 80% del techo "
                           f"({techo:.2f} €): FREEZE de gasto activado.", actor="sistema")
        self.event("gasto", f"{importe:.2f} € ({nota or 'sin nota'})"
                   + (f" [{tarea}]" if tarea else ""), ref=tarea, actor=por)
        return entry

    def month_spend(self) -> float:
        path = self.ledger_dir / "gastos.jsonl"
        if not path.exists():
            return 0.0
        total = 0.0
        mk = month_key()
        for line in path.read_text().strip().splitlines():
            e = json.loads(line)
            if e.get("mes") == mk:
                total += float(e.get("importe_eur", 0))
        return total

    # -- snapshot para el panel ------------------------------------------------------
    def snapshot(self) -> dict:
        tasks = self.list_tasks()
        depts = self.departments()
        by_dept: dict = {slug: {"queued": 0, "running": 0, "review": 0, "gate": 0,
                                "blocked": 0, "done": 0} for slug in depts}
        agents = []
        for t in tasks:
            d = t.get("dept")
            if d in by_dept and t["estado"] in by_dept[d]:
                by_dept[d][t["estado"]] += 1
            if t["estado"] == "running" and t.get("agente"):
                agents.append({"tarea": t["id"], "titulo": t["titulo"],
                               "dept": d, "agente": t["agente"],
                               "desde": t["actualizada"]})
        ctl = self.control()
        return {
            "control": ctl,
            "departamentos": depts,
            "conteo_por_dept": by_dept,
            "tareas": tasks,
            "agentes_en_trabajo": agents,
            "gates_pendientes": self.list_gates(estado="pendiente"),
            "gates_recientes": self.list_gates()[:20],
            "marcas": self.brands(),
            "gasto_mes_eur": self.month_spend(),
            "eventos": self.events(limit=80),
            "pulsos_pendientes": [d["slug"] for d in self.due_pulses()],
            "ts": now_iso(),
        }
