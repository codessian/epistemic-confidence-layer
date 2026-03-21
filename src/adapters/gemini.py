from __future__ import annotations
import os, time
from .base import BaseAdapter, Generation, ProviderError, AdapterRegistry

class GeminiAdapter(BaseAdapter):
    name = "gemini"
    def generate(self, prompt: str, **kwargs) -> Generation:
        # Lazy import to avoid hard dependency
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise ProviderError("GEMINI_API_KEY not set")
        try:
            import google.generativeai as genai
        except Exception as e:
            raise ProviderError(f"Gemini SDK not available: {e}")
        model_id = kwargs.get("model", "gemini-1.5-flash")
        timeout = kwargs.get("timeout_s", 15)
        t0 = time.time()
        genai.configure(api_key=key)
        try:
            model = genai.GenerativeModel(model_id)
            # No direct timeout param; rely on client/network defaults.
            resp = model.generate_content(prompt)
            text = getattr(resp, "text", "") or ""
            latency = int((time.time()-t0)*1000)
            return Generation(text=text, metadata={"vendor":"google","arch_family":"gemini","latency_ms":latency})
        except Exception as e:
            raise ProviderError(f"Gemini error: {e}")

AdapterRegistry.global_registry().register(GeminiAdapter())