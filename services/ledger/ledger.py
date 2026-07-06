#!/usr/bin/env python3
"""ledger v1 — dos divisas: euros reales y capacidad de suscripción. CLI determinista.

Uso:
  ledger.py gasto <euros> <concepto> [experimento]
  ledger.py sub <tipo> <detalle>          # tipo: rate_limit | pausa_critica | ventana_agotada
  ledger.py gate-nuevo <id> <nivel> <resumen> <rollback>   # crea solicitud pendiente
  ledger.py gate-estado <id>              # imprime estado; exit 0 solo si 'aprobado'
  ledger.py check                         # circuit breakers; exit != 0 si hay freno
  ledger.py informe [YYYY-MM]
"""
import os
import sqlite3
import sys
from datetime import date

DB = os.environ.get("MANDI_DB", "/srv/mandi/state/mandi.db")
TECHO_MES = float(os.environ.get("TECHO_MENSUAL_EUR", "300"))
FRENO_PCT = float(os.environ.get("FRENO_PCT", "0.8"))
LIMITE_EXPERIMENTO = float(os.environ.get("LIMITE_EXPERIMENTO_EUR", "30"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS spend (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, euros REAL, concepto TEXT, experimento TEXT);
CREATE TABLE IF NOT EXISTS sub_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, tipo TEXT, detalle TEXT);
CREATE TABLE IF NOT EXISTS gates (
  id TEXT PRIMARY KEY, ts_creado TEXT, nivel TEXT, resumen TEXT, rollback TEXT,
  estado TEXT DEFAULT 'pendiente', ts_resuelto TEXT, respuesta TEXT);
CREATE TABLE IF NOT EXISTS outbox (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, texto TEXT, enviado INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT);
"""


def db() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    con = sqlite3.connect(DB, timeout=30)
    con.executescript(SCHEMA)
    return con


def alerta(con, texto: str) -> None:
    con.execute("INSERT INTO outbox (ts, texto) VALUES (datetime('now'), ?)", (texto,))
    con.commit()
    print(texto)


def mes_actual() -> str:
    return date.today().strftime("%Y-%m")


def gasto_mes(con, mes: str) -> float:
    row = con.execute(
        "SELECT COALESCE(SUM(euros),0) FROM spend WHERE strftime('%Y-%m', ts)=?", (mes,)
    ).fetchone()
    return row[0]


def cmd_gasto(con, euros: str, concepto: str, experimento: str = "") -> int:
    e = float(euros)
    con.execute(
        "INSERT INTO spend (ts, euros, concepto, experimento) VALUES (datetime('now'),?,?,?)",
        (e, concepto, experimento),
    )
    con.commit()
    if experimento:
        tot = con.execute(
            "SELECT COALESCE(SUM(euros),0) FROM spend WHERE experimento=?", (experimento,)
        ).fetchone()[0]
        if tot > LIMITE_EXPERIMENTO:
            alerta(con, f"🛑 Experimento '{experimento}' en {tot:.2f}€ > límite "
                        f"{LIMITE_EXPERIMENTO:.0f}€. Tareas del experimento PAUSADAS.")
            return 2
    return 0


def cmd_sub(con, tipo: str, detalle: str) -> int:
    con.execute(
        "INSERT INTO sub_events (ts, tipo, detalle) VALUES (datetime('now'),?,?)",
        (tipo, detalle),
    )
    con.commit()
    return 0


def cmd_gate_nuevo(con, gid: str, nivel: str, resumen: str, rollback: str) -> int:
    con.execute(
        "INSERT INTO gates (id, ts_creado, nivel, resumen, rollback) "
        "VALUES (?, datetime('now'), ?, ?, ?)",
        (gid, nivel, resumen, rollback),
    )
    alerta(con, f"[GATE {nivel}] {gid} — {resumen}\nRollback: {rollback}\n"
                f"Responde: APRUEBO {gid} / RECHAZO {gid} <motivo> / PREGUNTA {gid} <texto>")
    return 0


def cmd_gate_estado(con, gid: str) -> int:
    row = con.execute("SELECT estado, respuesta FROM gates WHERE id=?", (gid,)).fetchone()
    if not row:
        print("inexistente")
        return 3
    print(row[0], row[1] or "")
    return 0 if row[0] == "aprobado" else 1


def cmd_check(con) -> int:
    """Circuit breakers deterministas. Exit != 0 => freno activo."""
    mes = mes_actual()
    gastado = gasto_mes(con, mes)
    dia = max(date.today().day, 1)
    proyeccion = gastado / dia * 30
    codigo = 0
    if proyeccion > TECHO_MES * FRENO_PCT:
        alerta(con, f"⚠️ Proyección mensual {proyeccion:.0f}€ > {FRENO_PCT*100:.0f}% del techo "
                    f"({TECHO_MES:.0f}€). Freno a gasto R1 nuevo hasta OK del propietario.")
        codigo = 2
    intentos = con.execute(
        "SELECT COUNT(*) FROM sub_events WHERE tipo='rate_limit' "
        "AND ts > datetime('now','-1 day')").fetchone()[0]
    if intentos >= 5:
        alerta(con, f"⚠️ {intentos} rate-limits de suscripción en 24h: capacidad premium "
                    "al límite. Dato para la revisión de plan en F2.")
    print(f"mes={mes} gastado={gastado:.2f}€ proyección={proyeccion:.0f}€ "
          f"rate_limits_24h={intentos}")
    return codigo


def cmd_informe(con, mes: str = "") -> int:
    mes = mes or mes_actual()
    print(f"== Informe {mes} ==")
    print(f"€ gastados: {gasto_mes(con, mes):.2f} (techo {TECHO_MES:.0f})")
    for c, e in con.execute(
        "SELECT concepto, SUM(euros) FROM spend WHERE strftime('%Y-%m',ts)=? "
        "GROUP BY concepto ORDER BY 2 DESC", (mes,)):
        print(f"  {c}: {e:.2f}€")
    for t, n in con.execute(
        "SELECT tipo, COUNT(*) FROM sub_events WHERE strftime('%Y-%m',ts)=? GROUP BY tipo",
        (mes,)):
        print(f"  sub/{t}: {n}")
    pend = con.execute("SELECT COUNT(*) FROM gates WHERE estado='pendiente'").fetchone()[0]
    print(f"gates pendientes: {pend}")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    con = db()
    cmd, args = sys.argv[1], sys.argv[2:]
    tabla = {
        "gasto": cmd_gasto, "sub": cmd_sub, "gate-nuevo": cmd_gate_nuevo,
        "gate-estado": cmd_gate_estado, "check": cmd_check, "informe": cmd_informe,
    }
    if cmd not in tabla:
        print(__doc__)
        return 1
    return tabla[cmd](con, *args)


if __name__ == "__main__":
    sys.exit(main())
