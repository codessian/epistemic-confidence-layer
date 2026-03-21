from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def _reset_server_state(monkeypatch):
    monkeypatch.setenv("ECL_AUTH_MODE", "off")
    monkeypatch.setenv("ECL_API_KEYS", "")
    monkeypatch.setenv("ECL_RATE_LIMIT_RPM", "100000")
    monkeypatch.setenv("ECL_RATE_LIMIT_KEY_STRATEGY", "ip")
    from src.config import load_settings
    from src.server import app as app_module

    app_module._REQUEST_WINDOWS.clear()
    app_module.app.state.settings = load_settings()
    yield
