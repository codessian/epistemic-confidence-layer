from fastapi.testclient import TestClient

from src.config import load_settings
from src.server.app import app
from src.server import app as app_module


def test_auth_middleware_requires_api_key(monkeypatch):
    monkeypatch.setenv("ECL_AUTH_MODE", "apikey")
    monkeypatch.setenv("ECL_API_KEYS", "k1")
    app.state.settings = load_settings()
    app_module._REQUEST_WINDOWS.clear()
    client = TestClient(app)
    response = client.post("/verify", json={"prompt": "hello", "contains_pii": False})
    assert response.status_code in {401, 403}


def test_rate_limit_middleware_blocks(monkeypatch):
    monkeypatch.setenv("ECL_AUTH_MODE", "off")
    monkeypatch.setenv("ECL_RATE_LIMIT_RPM", "1")
    monkeypatch.setenv("ECL_RATE_LIMIT_KEY_STRATEGY", "ip")
    app.state.settings = load_settings()
    app_module._REQUEST_WINDOWS.clear()
    client = TestClient(app)
    first = client.post("/verify", json={"prompt": "hello", "contains_pii": False})
    second = client.post("/verify", json={"prompt": "hello", "contains_pii": False})
    assert first.status_code in {200, 503}
    assert second.status_code in {429, 503}
