import sys
from types import SimpleNamespace

import pytest
import requests

from src.adapters.gemini import GeminiAdapter
from src.adapters.google import GoogleAdapter
from src.adapters.hf import HFInferenceAdapter
from src.adapters.openrouter import OpenRouterAdapter
from src.adapters.vertex import VertexAIAdapter
from src.errors import AdapterError


def test_google_generate_success_with_fake_model(monkeypatch):
    adapter = GoogleAdapter()

    class FakeModel:
        def generate_content(self, prompt=None, contents=None):
            text = prompt if prompt is not None else contents
            return SimpleNamespace(text=f"ok:{text}")

    adapter._model = FakeModel()
    out = adapter.generate("hi")
    assert out.text.startswith("ok:")
    assert out.metadata["provider_kind"] == "google"


def test_google_generate_timeout_raises_adapter_error(monkeypatch):
    adapter = GoogleAdapter()

    class FakeModel:
        def generate_content(self, prompt=None, contents=None):
            raise TimeoutError("timeout")

    adapter._model = FakeModel()
    adapter._max_attempts = 1
    adapter._max_elapsed_s = 0.1
    with pytest.raises(AdapterError):
        adapter.generate("hi")


def test_hf_generate_success(monkeypatch):
    monkeypatch.setenv("HF_API_URL", "https://example.invalid")
    monkeypatch.setenv("HF_API_TOKEN", "token")
    adapter = HFInferenceAdapter("repo")

    class FakeResp:
        status_code = 200

        def json(self):
            return [{"generated_text": "hf-ok"}]

    monkeypatch.setattr("src.adapters.hf.requests.post", lambda *args, **kwargs: FakeResp())
    out = adapter.generate("hello")
    assert out.text == "hf-ok"


def test_hf_generate_timeout(monkeypatch):
    monkeypatch.setenv("HF_API_URL", "https://example.invalid")
    monkeypatch.setenv("HF_API_TOKEN", "token")
    adapter = HFInferenceAdapter("repo")

    def raise_timeout(*args, **kwargs):
        raise requests.Timeout("x")

    monkeypatch.setattr("src.adapters.hf.requests.post", raise_timeout)
    with pytest.raises(AdapterError):
        adapter.generate("hello")


def test_openrouter_generate_success(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "token")
    adapter = OpenRouterAdapter("openrouter/model")

    class FakeResp:
        status_code = 200

        def json(self):
            return {"choices": [{"message": {"content": "or-ok"}}]}

    monkeypatch.setattr("src.adapters.openrouter.requests.post", lambda *args, **kwargs: FakeResp())
    out = adapter.generate("hello")
    assert out.text == "or-ok"


def test_openrouter_generate_timeout(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "token")
    adapter = OpenRouterAdapter("openrouter/model")

    def raise_timeout(*args, **kwargs):
        raise requests.Timeout("x")

    monkeypatch.setattr("src.adapters.openrouter.requests.post", raise_timeout)
    with pytest.raises(AdapterError):
        adapter.generate("hello")


def test_vertex_generate_sdk_missing(monkeypatch):
    monkeypatch.setenv("VERTEX_PROJECT", "proj")
    adapter = VertexAIAdapter("model")
    with pytest.raises(AdapterError):
        adapter.generate("hello")


def test_gemini_generate_success_with_fake_sdk(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "token")
    adapter = GeminiAdapter("gemini")

    class FakeGenAI:
        @staticmethod
        def configure(api_key):
            return None

        class GenerativeModel:
            def __init__(self, model):
                self.model = model

            def generate_content(self, prompt):
                return SimpleNamespace(text=f"gem:{prompt}")

    monkeypatch.setitem(sys.modules, "google.generativeai", FakeGenAI)
    out = adapter.generate("hello")
    assert out.text.startswith("gem:")


def test_vertex_generate_success_with_fake_sdk(monkeypatch):
    monkeypatch.setenv("VERTEX_PROJECT", "proj")
    monkeypatch.setenv("VERTEX_LOCATION", "us-central1")
    adapter = VertexAIAdapter("model")

    class FakeAiplatform:
        @staticmethod
        def init(project, location):
            return None

    class FakeModel:
        def __init__(self, model):
            self.model = model

        def generate_content(self, prompt):
            return SimpleNamespace(text=f"vx:{prompt}")

    fake_google_cloud = SimpleNamespace(aiplatform=FakeAiplatform)
    fake_generative_mod = SimpleNamespace(GenerativeModel=FakeModel)
    monkeypatch.setitem(sys.modules, "google.cloud", fake_google_cloud)
    monkeypatch.setitem(sys.modules, "vertexai.preview.generative_models", fake_generative_mod)
    out = adapter.generate("hello")
    assert out.text.startswith("vx:")
