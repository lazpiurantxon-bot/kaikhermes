#!/usr/bin/env python3
"""watchdog v1 — cron cada 5 min. Determinista. Corre TAMBIÉN en pausa (es monitorización).

Comprueba: healthchecks HTTP (HEALTH_URLS, separadas por coma), uso de disco,
backup del estado (copia local rotada + GCS opcional vía gsutil).
Alerta encolando en outbox (el gateway envía).
"""
import os
import shutil
import sqlite3
import subprocess
import sys
import urllib.request
from datetime import datetime

DB = os.environ.get("MANDI_DB", "/srv/mandi/state/mandi.db")
HEALTH_URLS = [u for u in os.environ.get("HEALTH_URLS", "").split(",") if u.strip()]
DISCO_MAX_PCT = int(os.environ.get("DISCO_MAX_PCT", "85"))
BACKUP_DIR = os.environ.get("BACKUP_DIR", "/srv/mandi/state/backups")
BACKUP_BUCKET = os.environ.get("BACKUP_BUCKET", "")  # ej: gs://mandi-backups
BACKUP_KEEP = int(os.environ.get("BACKUP_KEEP", "14"))


def alerta(texto: str) -> None:
    con = sqlite3.connect(DB, timeout=30)
    con.execute("CREATE TABLE IF NOT EXISTS outbox (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                " ts TEXT, texto TEXT, enviado INTEGER DEFAULT 0)")
    con.execute("INSERT INTO outbox (ts, texto) VALUES (datetime('now'), ?)", (texto,))
    con.commit()
    con.close()
    print(texto, file=sys.stderr)


def check_salud() -> None:
    for url in HEALTH_URLS:
        url = url.strip()
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                if r.status >= 400:
                    alerta(f"🔴 Healthcheck {url}: HTTP {r.status}")
        except Exception as e:
            alerta(f"🔴 Healthcheck {url}: {e}")


def check_disco() -> None:
    total, usado, _ = shutil.disk_usage("/")
    pct = usado * 100 // total
    if pct >= DISCO_MAX_PCT:
        alerta(f"🔴 Disco al {pct}% (umbral {DISCO_MAX_PCT}%)")


def backup(diario: bool) -> None:
    if not diario or not os.path.exists(DB):
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    destino = os.path.join(BACKUP_DIR, f"mandi-{datetime.now():%Y%m%d}.db")
    if os.path.exists(destino):
        return  # ya hecho hoy
    src = sqlite3.connect(DB)
    dst = sqlite3.connect(destino)
    src.backup(dst)  # copia consistente aunque haya escrituras
    src.close(); dst.close()
    copias = sorted(os.listdir(BACKUP_DIR))
    for viejo in copias[:-BACKUP_KEEP]:
        os.remove(os.path.join(BACKUP_DIR, viejo))
    if BACKUP_BUCKET:
        r = subprocess.run(["gsutil", "cp", destino, BACKUP_BUCKET],
                           capture_output=True, text=True)
        if r.returncode != 0:
            alerta(f"🔴 Backup a GCS falló: {r.stderr[:200]}")


def main() -> None:
    check_salud()
    check_disco()
    backup(diario=datetime.now().hour == 4 or "--force-backup" in sys.argv)


if __name__ == "__main__":
    main()
