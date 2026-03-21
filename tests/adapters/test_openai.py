import types

import pytest

from src.adapter_metrics import get_events, reset_events
from src.adapters.base import Generation, generate_with_cache
from src.adapters.openai import OpenAIAdapter
from src.errors import AdapterError


def test_openai_stub_without_key_returns_generation(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    a = OpenAIAdapter()
    assert not a.is_available()
    out = a.generate("hello world")
    assert isinstance(out, Generation)
    assert out.text.startswith("[openai-stub]")


def test_openai_timeout_maps_to_provider_timeout():
    a = OpenAIAdapter()

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
    assert out.text == "ok"
    evts = get_events()
    assert any(e["status"] == "ok" and e["name"] == "openai" for e in evts)


def test_openai_generate_with_cache_returns_generation(monkeypatch):
    reset_events()
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    a = OpenAIAdapter()
    out1 = generate_with_cache(a, "cache me")
    out2 = generate_with_cache(a, "cache me")
    assert out1.text == out2.text
    evts = get_events()
    assert any(e["cache_hit"] and e["name"] == "openai" for e in evts)
