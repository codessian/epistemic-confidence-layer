from __future__ import annotations
import os, requests, time
from typing import Dict, Any
from .base import BaseAdapter, Generation, ProviderError, AdapterRegistry

class OpenRouterAdapter(BaseAdapter):
    name = "openrouter"

    def generate(self, prompt: str, **kwargs) -> Generation:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ProviderError("OPENROUTER_API_KEY not set")
        model = kwargs.get("model")
        timeout = kwargs.get("timeout_s", 15)
        t0 = time.time()
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "HTTP-Referer": "https://github.com/codessian/epistemic-confidence-layer"},
                json={"model": model, "messages":[{"role":"user","content":prompt}], "temperature":0},
                timeout=timeout,
            )
            if r.status_code >= 400:
                raise ProviderError(f"OpenRouter HTTP {r.status_code}: {r.text[:200]}")
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            latency = int((time.time()-t0)*1000)
            # rough cost estimate if provided
            meta = {"vendor":"openrouter","arch_family":"var","latency_ms":latency}
            return Generation(text=text, metadata=meta)
        except requests.Timeout as e:
            raise ProviderError(f"OpenRouter timeout: {e}")

AdapterRegistry.global_registry().register(OpenRouterAdapter())