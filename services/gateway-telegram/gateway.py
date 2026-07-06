#!/usr/bin/env python3
"""gateway-telegram v1 — capa determinista, sin LLM, sin dependencias externas.

Funciones: intake (IDEA:), gates (APRUEBO/RECHAZO/PREGUNTA <id>), kill switch
(PARA TODO / REANUDA), consulta (ESTADO) y envío del outbox.
Solo acepta mensajes del chat OWNER_CHAT_ID; el resto se registra y se ignora.
"""
import json
import os
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DB = os.environ.get("MANDI_DB", "/srv/mandi/state/mandi.db")
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OWNER = int(os.environ["OWNER_CHAT_ID"])
API = f"https://api.telegram.org/bot{TOKEN}"

SCHEMA = """
CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS intake (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, texto TEXT, procesado INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS gates (
  id TEXT PRIMARY KEY, ts_creado TEXT, nivel TEXT, resumen TEXT, rollback TEXT,
  estado TEXT DEFAULT 'pendiente', ts_resuelto TEXT, respuesta TEXT);
CREATE TABLE IF NOT EXISTS outbox (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, texto TEXT, enviado INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS acciones (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, origen TEXT, tipo TEXT, detalle TEXT);
"""

AYUDA = (
    "Comandos:\n"
    "IDEA: <texto> — registrar idea en intake\n"
    "APRUEBO <id> — aprobar gate\n"
    "RECHAZO <id> <motivo> — rechazar gate\n"
    "PREGUNTA <id> <texto> — pedir aclaración sobre un gate\n"
    "ESTADO — pausa, gates pendientes, intake\n"
    "PARA TODO — kill switch global\n"
    "REANUDA — rearmar tras kill switch"
)


def db() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    con = sqlite3.connect(DB, timeout=30)
    con.executescript(SCHEMA)
    return con


def api(method: str, **params):
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(f"{API}/{method}", data=data, timeout=90) as r:
        return json.load(r)


def send(texto: str) -> None:
    api("sendMessage", chat_id=OWNER, text=texto[:4000])


def log(con, origen: str, tipo: str, detalle: str) -> None:
    con.execute(
        "INSERT INTO acciones (ts, origen, tipo, detalle) VALUES (datetime('now'),?,?,?)",
        (origen, tipo, detalle[:500]),
    )
    con.commit()


def set_pausa(con, valor: str) -> None:
    con.execute("INSERT OR REPLACE INTO kv (k, v) VALUES ('pausado', ?)", (valor,))
    con.commit()


def pausado(con) -> bool:
    row = con.execute("SELECT v FROM kv WHERE k='pausado'").fetchone()
    return bool(row and row[0] == "1")


def resolver_gate(con, verbo: str, resto: str) -> None:
    gid, _, comentario = resto.strip().partition(" ")
    if not gid:
        send("Falta el id del gate.")
        return
    row = con.execute("SELECT estado FROM gates WHERE id=?", (gid,)).fetchone()
    if not row:
        send(f"No existe el gate {gid}.")
        return
    if verbo == "PREGUNTA":
        log(con, "owner", "gate_pregunta", f"{gid}: {comentario}")
        send(f"Pregunta registrada para {gid}; se responderá en el hilo del issue.")
        return
    if row[0] != "pendiente":
        send(f"El gate {gid} ya está '{row[0]}'. Nada que hacer.")
        return
    if verbo == "RECHAZO" and not comentario:
        send("RECHAZO requiere motivo: RECHAZO <id> <motivo>")
        return
    estado = "aprobado" if verbo == "APRUEBO" else "rechazado"
    con.execute(
        "UPDATE gates SET estado=?, ts_resuelto=datetime('now'), respuesta=? WHERE id=?",
        (estado, comentario, gid),
    )
    con.commit()
    log(con, "owner", f"gate_{estado}", f"{gid} {comentario}")
    send(f"Gate {gid}: {estado}. Registrado en el ledger.")


def estado(con) -> None:
    pend = con.execute(
        "SELECT id, nivel, resumen FROM gates WHERE estado='pendiente' ORDER BY ts_creado"
    ).fetchall()
    n_intake = con.execute("SELECT COUNT(*) FROM intake WHERE procesado=0").fetchone()[0]
    lineas = [
        f"Pausado: {'sí ⛔' if pausado(con) else 'no'}",
        f"Intake sin triar: {n_intake}",
        f"Gates pendientes: {len(pend)}",
    ]
    lineas += [f"  [{g[1]}] {g[0]}: {g[2][:70]}" for g in pend[:10]]
    send("\n".join(lineas))


def handle(con, texto: str) -> None:
    t = texto.strip()
    up = t.upper()
    if up == "PARA TODO":
        set_pausa(con, "1")
        log(con, "owner", "kill_switch", "PARA TODO")
        send("⛔ Sistema pausado. Ningún job programado arrancará. REANUDA para rearmar.")
    elif up == "REANUDA":
        set_pausa(con, "0")
        log(con, "owner", "kill_switch", "REANUDA")
        send("▶️ Sistema reanudado.")
    elif up.startswith(("APRUEBO ", "RECHAZO ", "PREGUNTA ")):
        verbo, _, resto = t.partition(" ")
        resolver_gate(con, verbo.upper(), resto)
    elif up.startswith("IDEA:"):
        con.execute(
            "INSERT INTO intake (ts, texto) VALUES (datetime('now'), ?)", (t[5:].strip(),)
        )
        con.commit()
        log(con, "owner", "intake", t)
        send("Idea registrada. Entrará en TRIAGE en la próxima sesión del JdG.")
    elif up == "ESTADO":
        estado(con)
    else:
        send(AYUDA)


def flush_outbox(con) -> None:
    for oid, texto in con.execute(
        "SELECT id, texto FROM outbox WHERE enviado=0 ORDER BY id LIMIT 20"
    ).fetchall():
        send(texto)
        con.execute("UPDATE outbox SET enviado=1 WHERE id=?", (oid,))
        con.commit()


def main() -> None:
    con = db()
    log(con, "gateway", "arranque", "gateway v1 iniciado")
    offset = 0
    while True:
        try:
            flush_outbox(con)
            res = api("getUpdates", offset=offset, timeout=60)
            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message") or {}
                chat_id = (msg.get("chat") or {}).get("id")
                texto = msg.get("text") or ""
                if chat_id != OWNER:
                    log(con, "gateway", "rechazo_no_owner", f"chat={chat_id}")
                    continue
                if texto:
                    handle(con, texto)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            print(f"[gateway] error de red: {e}", file=sys.stderr)
            time.sleep(5)
        except Exception as e:  # nunca morir por un update malformado
            print(f"[gateway] error: {e}", file=sys.stderr)
            time.sleep(2)


if __name__ == "__main__":
    main()
