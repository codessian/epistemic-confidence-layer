import types
import pytest

from src.ecl.adapters.openai import OpenAIAdapter
from src.ecl.adapters.base import generate_with_cache
from src.ecl.adapter_metrics import reset_events, get_events
from src.ecl.errors import AdapterError


def test_openai_stub_without_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    a = OpenAIAdapter()
    assert not a.is_available()
    out = a.generate("hello world")
    assert out.startswith("[openai-stub]")


def test_openai_timeout_maps_to_provider_timeout(monkeypatch):
    # Create adapter with fake client that always times out
    a = OpenAIAdapter()
    # Inject fake client
    class FakeClient:
        class chat:
            class completions:
                @staticmethod
                def create(**kwargs):
                    raise TimeoutError("deadline exceeded")
    a._client = FakeClient()
    a._max_attempts = 1
    a._max_elapsed_s = 0.5
    with pytest.raises(AdapterError) as ei:
        a.generate("hello")
    assert ei.value.code == "PROVIDER_TIMEOUT"


def test_openai_retry_backoff_and_success(monkeypatch):
    reset_events()
    # No actual sleep
    monkeypatch.setattr("time.sleep", lambda s: None)

    a = OpenAIAdapter()
    calls = {"n": 0}

    class FakeRateLimitError(Exception):
        def __init__(self):
            self.response = types.SimpleNamespace(status_code=429, headers={"Retry-After": "0"})

    class Resp:
        def __init__(self, text):
            self.choices = [types.SimpleNamespace(message=types.SimpleNamespace(content=text))]

    class FakeClient:
        class chat:
            class completions:
                @staticmethod
                def create(**kwargs):
                    calls["n"] += 1
                    if calls["n"] == 1:
                        raise FakeRateLimitError()
                    return Resp("ok")

    a._client = FakeClient()
    a._max_attempts = 3
    a._max_elapsed_s = 3.0
    out = a.generate("say ok")
    assert out == "ok"
    evts = get_events()
    assert any(e["status"] == "ok" and e["name"] == "openai" for e in evts)


def test_openai_generate_with_cache_hits(monkeypatch):
    reset_events()
    # Use stub path to avoid network
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    a = OpenAIAdapter()
    out1 = generate_with_cache(a, "cache me")
    out2 = generate_with_cache(a, "cache me")
    assert out1 == out2
    # Ensure a cache hit was recorded
    evts = get_events()
    assert any(e["cache_hit"] and e["name"] == "openai" for e in evts)