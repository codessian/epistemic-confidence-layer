from __future__ import annotations
import requests, time
from typing import Any
from .base import BaseAdapter, Generation, ProviderError, AdapterRegistry

class OllamaAdapter(BaseAdapter):
    name = "ollama"
    def generate(self, prompt: str, **kwargs) -> Generation:
        model = kwargs.get("model", "llama3.1")
        timeout = kwargs.get("timeout_s", 15)
        t0 = time.time()
        try:
            r = requests.post("http://127.0.0.1:11434/api/generate",
                              json={"model": model, "prompt": prompt, "stream": False},
                              timeout=timeout)
            if r.status_code >= 400:
                raise ProviderError(f"Ollama HTTP {r.status_code}: {r.text[:200]}")
            data = r.json()
            latency = int((time.time()-t0)*1000)
            return Generation(text=data.get("response",""), metadata={"vendor":"ollama","arch_family":"local","latency_ms":latency})
        except requests.Timeout as e:
            raise ProviderError(f"Ollama timeout: {e}")

AdapterRegistry.global_registry().register(OllamaAdapter())