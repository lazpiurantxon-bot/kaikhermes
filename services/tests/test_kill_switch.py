#!/usr/bin/env python3
"""Prueba del kill switch (precondición 5 de ADR-002). Ejecutable en local/CI sin red:
simula PARA TODO / REANUDA directamente sobre el esquema y verifica el contrato
que todo job programado debe cumplir (abortar si pausado='1')."""
import os
import sqlite3
import sys
import tempfile

os.environ["MANDI_DB"] = os.path.join(tempfile.mkdtemp(), "mandi.db")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "gateway-telegram"))
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test:token")
os.environ.setdefault("OWNER_CHAT_ID", "1")

import gateway  # noqa: E402


def job_respetuoso(con) -> str:
    """Contrato que TODO job programado debe implementar."""
    if gateway.pausado(con):
        return "abortado"
    return "ejecutado"


def main() -> int:
    con = gateway.db()
    assert job_respetuoso(con) == "ejecutado", "sin pausa debe ejecutar"
    gateway.set_pausa(con, "1")   # equivale a PARA TODO
    assert gateway.pausado(con), "PARA TODO debe marcar pausado=1"
    assert job_respetuoso(con) == "abortado", "job debe abortar en pausa"
    gateway.set_pausa(con, "0")   # equivale a REANUDA
    assert job_respetuoso(con) == "ejecutado", "REANUDA debe rearmar"
    print("OK: kill switch marca, bloquea jobs y rearma correctamente")
    return 0


if __name__ == "__main__":
    sys.exit(main())
