import shutil
import sys
from pathlib import Path

import pytest

OFFICE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OFFICE_DIR))

from core.store import Store  # noqa: E402


def seeded_store(tmp_path: Path) -> Store:
    state = tmp_path / "state"
    state.mkdir()
    for name in ("departamentos.json", "marcas.json", "control.json"):
        shutil.copy(OFFICE_DIR / "seeds" / name, state / name)
    return Store(state)


@pytest.fixture
def store(tmp_path):
    return seeded_store(tmp_path)
