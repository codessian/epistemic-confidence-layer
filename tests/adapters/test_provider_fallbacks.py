import requests

from src.adapters.gemini import GeminiAdapter
from src.adapters.hf import HFInferenceAdapter
from src.adapters.ollama import OllamaAdapter
from src.adapters.openrouter import OpenRouterAdapter
from src.adapters.vertex import VertexAIAdapter


def test_gemini_fallback_without_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    adapter = GeminiAdapter("gemini-1.5-flash")
    out = adapter.generate("hello")
    assert out.text.startswith("[gemini-stub]")


def test_hf_fallback_without_credentials(monkeypatch):
    monkeypatch.delenv("HF_API_URL", raising=False)
    monkeypatch.delenv("HF_API_TOKEN", raising=False)
    adapter = HFInferenceAdapter("repo-id")
    out = adapter.generate("hello")
    assert out.text.startswith("[hf-stub]")


def test_openrouter_fallback_without_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    adapter = OpenRouterAdapter("model")
    out = adapter.generate("hello")
    assert out.text.startswith("[openrouter-stub]")


def test_vertex_fallback_without_project(monkeypatch):
    monkeypatch.delenv("VERTEX_PROJECT", raising=False)
    adapter = VertexAIAdapter("model")
    out = adapter.generate("hello")
    assert out.text.startswith("[vertex-stub]")


def test_ollama_fallback_on_request_error(monkeypatch):
    adapter = OllamaAdapter("llama3.1")

    def raise_request_error(*args, **kwargs):
        raise requests.RequestException("network down")

    monkeypatch.setattr("src.adapters.ollama.requests.post", raise_request_error)
    out = adapter.generate("hello")
    assert out.text.startswith("[ollama-stub]")
