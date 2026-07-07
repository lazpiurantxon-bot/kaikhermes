"""Ciclo de vida del tablero: WIP, breakers, gates, kill switch, ledger."""
import pytest

from core.store import StoreError


def make_queued(store, dept="mercado", titulo="t"):
    return store.create_task(titulo=titulo, por="test", origen="proactivo",
                             estado="queued", dept=dept)


def test_flujo_completo(store):
    t = store.create_task("Analizar X", por="owner:panel", origen="panel")
    assert t["estado"] == "intake"
    t = store.assign_task(t["id"], "mercado", por="gabinete", prioridad=2)
    assert t["estado"] == "queued" and t["prioridad"] == 2
    t = store.start_task(t["id"], agente="dep-mercado")
    assert t["estado"] == "running" and t["agente"] == "dep-mercado"
    t = store.deliver_task(t["id"], "informe en x.md", por="dep-mercado")
    assert t["estado"] == "review" and t["agente"] is None
    t = store.close_task(t["id"], por="owner:panel")
    assert t["estado"] == "done"
    assert any(h["a"] == "running" for h in t["historial"])


def test_transicion_invalida(store):
    t = store.create_task("x", por="a")
    with pytest.raises(StoreError):
        store.deliver_task(t["id"], "r", por="a")  # intake → review no existe


def test_wip_global(store):
    t1, t2, t3 = (make_queued(store, d) for d in ("mercado", "producto", "marketing"))
    store.start_task(t1["id"], "a1")
    store.start_task(t2["id"], "a2")
    with pytest.raises(StoreError, match="WIP global"):
        store.start_task(t3["id"], "a3")


def test_wip_departamento(store):
    store.set_control("owner:test", wip_global=10)
    t1, t2 = make_queued(store), make_queued(store)
    store.start_task(t1["id"], "a1")
    with pytest.raises(StoreError, match="WIP de mercado"):
        store.start_task(t2["id"], "a2")


def test_departamento_pausado_no_arranca(store):
    t = make_queued(store)
    store.update_department("mercado", "owner:panel", pausado=True, pausado_motivo="test")
    with pytest.raises(StoreError, match="pausa"):
        store.start_task(t["id"], "a")


def test_breaker_tres_fallos(store):
    store.set_control("owner:test", wip_global=10)
    for i in range(3):
        t = make_queued(store, titulo=f"f{i}")
        store.start_task(t["id"], "a")
        store.fail_task(t["id"], "boom", por="a")
    d = store.departments()["mercado"]
    assert d["pausado"] and d["fallos_seguidos"] == 3
    assert any(e["tipo"] == "breaker" for e in store.events())


def test_entrega_resetea_fallos(store):
    t = make_queued(store)
    store.start_task(t["id"], "a")
    store.fail_task(t["id"], "boom", por="a")
    t2 = make_queued(store)
    store.start_task(t2["id"], "a")
    store.deliver_task(t2["id"], "ok", por="a")
    assert store.departments()["mercado"]["fallos_seguidos"] == 0


def test_kill_switch_bloquea_agentes(store):
    t = make_queued(store)
    store.set_control("gabinete", kill=True, motivo="PARA TODO")
    with pytest.raises(StoreError, match="KILL"):
        store.start_task(t["id"], "a")


def test_gate_flujo(store):
    t = make_queued(store, dept="marketing")
    store.set_control("owner:test", wip_global=10)
    store.start_task(t["id"], "dep-marketing")
    g = store.open_gate(t["id"], "R2", "publish", "Publicar X", "listo", "revert", por="dep-marketing")
    assert g["estado"] == "pendiente"
    assert store.get_task(t["id"])["estado"] == "gate"
    # un agente no decide sin cita del propietario
    with pytest.raises(StoreError, match="propietario"):
        store.decide_gate(g["id"], "aprobado", por="dep-marketing")
    g = store.decide_gate(g["id"], "aprobado", por="owner:panel", nota="ok")
    assert g["estado"] == "aprobado"
    assert store.get_task(t["id"])["estado"] == "queued"  # vuelve a cola para ejecutarse
    with pytest.raises(StoreError, match="ya está"):
        store.decide_gate(g["id"], "rechazado", por="owner:panel")


def test_gate_rechazado_vuelve_a_review(store):
    t = make_queued(store, dept="marketing")
    store.start_task(t["id"], "m")
    g = store.open_gate(t["id"], "R3", "contact", "Email a Z", "", "no enviar", por="m")
    store.decide_gate(g["id"], "rechazado", por="owner:panel", nota="no así")
    assert store.get_task(t["id"])["estado"] == "review"


def test_gate_requiere_rollback(store):
    t = make_queued(store)
    store.start_task(t["id"], "a")
    with pytest.raises(StoreError, match="rollback"):
        store.open_gate(t["id"], "R2", "publish", "X", "y", "  ", por="a")


def test_gate_via_telegram_con_cita(store):
    t = make_queued(store)
    store.start_task(t["id"], "a")
    g = store.open_gate(t["id"], "R2", "publish", "X", "y", "revert", por="a")
    g = store.decide_gate(g["id"], "aprobado", por="gabinete",
                          aprobacion_ref="APRUEBO G-0001 (Telegram 2026-07-07 09:12)")
    assert "APRUEBO" in g["nota_decision"]


def test_gasto_y_freeze(store):
    store.add_spend(10, por="dep-producto", nota="dominio")
    assert store.month_spend() == 10
    with pytest.raises(StoreError, match="política"):
        store.add_spend(50, por="dep-producto")  # > límite por tarea
    store.add_spend(20, por="a")
    store.add_spend(20, por="a")
    store.add_spend(20, por="a")
    store.add_spend(15, por="a")  # 85 ≥ 80% de 100 → freeze
    assert store.control()["freeze_gasto"] is True
    with pytest.raises(StoreError):
        store.add_spend(1, por="a")


def test_marca_oficina_y_colision(store):
    store.create_brand("aura", "Aura", por="dep-marca")
    with pytest.raises(StoreError, match="ya existe"):
        store.create_brand("aura", "Aura2", por="dep-marca")
    with pytest.raises(StoreError, match="propietario"):
        store.create_brand("otra", "Otra", por="dep-marca", status="protected")


def test_pulsos_pendientes(store):
    due = {d["slug"] for d in store.due_pulses()}
    assert due == {"mercado", "producto", "marketing", "marca"}  # nunca gabinete
    store.mark_pulse("mercado", "gabinete")
    assert "mercado" not in {d["slug"] for d in store.due_pulses()}
    # backlog lleno → sin pulso
    for i in range(3):
        make_queued(store, dept="producto", titulo=f"b{i}")
    assert "producto" not in {d["slug"] for d in store.due_pulses()}
    # pausa global → nada
    store.set_control("owner:t", pausa_global=True)
    assert store.due_pulses() == []


def test_answer_intake_y_snapshot(store):
    t = store.create_task("¿qué hora es?", por="gabinete", origen="telegram")
    store.answer_intake(t["id"], "las 12", por="gabinete")
    assert store.get_task(t["id"])["estado"] == "done"
    snap = store.snapshot()
    assert snap["control"]["wip_global"] == 2
    assert "mercado" in snap["departamentos"]
    assert isinstance(snap["gasto_mes_eur"], float)
