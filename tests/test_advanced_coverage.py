from types import SimpleNamespace

import numpy as np
import pytest

from src.calibration.isotonic import load_calibrator as iso_load
from src.calibration.platt import load_calibrator as platt_load
from src.router import DynamicRouter, ProviderSpec, RoutePolicy, RouteRequest
from src.server.app import app
from src.similarity import EmbeddingBackend, classify_pair


def test_calibrator_load_missing_returns_none(tmp_path):
    assert iso_load(str(tmp_path / "none.pkl")) is None
    assert platt_load(str(tmp_path / "none.pkl")) is None


def test_similarity_openai_embedding_path():
    backend = EmbeddingBackend()
    backend.backend = "openai"
    backend._embed_model = "model"

    class FakeEmbeddings:
        @staticmethod
        def create(model, input):
            data = [SimpleNamespace(embedding=[1.0, 0.0]), SimpleNamespace(embedding=[0.0, 1.0])]
            return SimpleNamespace(data=data)

    backend._client = SimpleNamespace(embeddings=FakeEmbeddings())
    matrix = backend.embed(["x", "y"])
    assert matrix.shape == (2, 2)


def test_classify_pair_labels_with_custom_backend():
    class FakeBackend:
        @staticmethod
        def embed(texts):
            return np.asarray([[1.0, 0.0], [1.0, 0.0]], dtype=np.float32)

    label, score = classify_pair("a", "b", backend=FakeBackend())
    assert label == "equivalent"
    assert score == pytest.approx(1.0)


def test_router_validate_policy_unknown_provider():
    specs = [ProviderSpec(id="p1", kind="openai", model="m")]
    policy = RoutePolicy(name="default", select={"type": "quorum_k_of_n", "k": 1, "providers": ["missing"]}, constraints={})
    router = DynamicRouter(specs, policy)
    with pytest.raises(ValueError):
        router.validate_policy()


def test_router_pii_constraint_adds_error():
    specs = [ProviderSpec(id="p1", kind="openai", model="m", allow_pii=False)]
    policy = RoutePolicy(name="default", select={"type": "quorum_k_of_n", "k": 1, "providers": ["p1"]}, constraints={})
    router = DynamicRouter(specs, policy)
    result = router.generate(RouteRequest(prompt="x", contains_pii=True, timeout_s=1, request_id="r1"))
    assert len(result.errors) == 1
    assert result.errors[0].code == "BAD_REQUEST"


def test_server_handlers_forbidden_and_rate_limited(monkeypatch):
    from fastapi.testclient import TestClient
    from src.config import load_settings
    from src.server import app as app_module

    monkeypatch.setenv("ECL_AUTH_MODE", "apikey")
    monkeypatch.setenv("ECL_API_KEYS", "k1")
    monkeypatch.setenv("ECL_RATE_LIMIT_RPM", "1")
    monkeypatch.setenv("ECL_RATE_LIMIT_KEY_STRATEGY", "ip")
    app.state.settings = load_settings()
    app_module._REQUEST_WINDOWS.clear()
    client = TestClient(app)
    forbidden = client.post("/verify", json={"prompt": "x", "contains_pii": False}, headers={"X-API-Key": "bad"})
    assert forbidden.status_code == 403
    ok = client.post("/verify", json={"prompt": "x", "contains_pii": False}, headers={"X-API-Key": "k1"})
    limited = client.post("/verify", json={"prompt": "x", "contains_pii": False}, headers={"X-API-Key": "k1"})
    assert ok.status_code in {200, 429, 503}
    assert limited.status_code in {429, 503}
