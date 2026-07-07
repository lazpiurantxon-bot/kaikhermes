"""Arranque del panel: `python3 -m panel.main` (desde office/) o vía systemd."""
import uvicorn

from panel.server import CONFIG, app


def run():
    uvicorn.run(app, host=CONFIG["host"], port=int(CONFIG["port"]), log_level="info")


if __name__ == "__main__":
    run()
