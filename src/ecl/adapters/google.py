"""Google adapter with robust generate(): timeouts, retries, and error normalization."""

from __future__ import annotations
import os
import time
import random
from typing import Any, Optional

try:
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover
    genai = None  # graceful fallback

from .base import BaseAdapter, registry
from ..errors import AdapterError, normalize_error
from ..adapter_metrics import record_adapter_event


class GoogleAdapter(BaseAdapter):
    """Adapter for Google Gemini models with graceful fallback when unavailable."""

    def __init__(self, model_id: str = "gemini-1.5-flash", **kwargs: Any):
        super().__init__(model_id, **kwargs)
        api_key = os.getenv("GOOGLE_API_KEY")
        # Config
        self._timeout_s = float(os.getenv("ECL_PROVIDER_TIMEOUT_S", "8.0"))
        self._max_attempts = int(os.getenv("ECL_PROVIDER_MAX_ATTEMPTS", "3"))
        self._max_elapsed_s = float(os.getenv("ECL_PROVIDER_MAX_ELAPSED_S", "16.0"))
        self._base_delay_s = float(os.getenv("ECL_PROVIDER_BASE_DELAY_S", "0.6"))
        self._jitter_s = float(os.getenv("ECL_PROVIDER_JITTER_S", "0.2"))
        try:
            if genai and api_key:
                genai.configure(api_key=api_key)
                # Create model instance; will use default timeouts internally
                self._model = genai.GenerativeModel(self.model_id)
            else:
                self._model = None
        except Exception:
            self._model = None

    def generate(self, prompt: str, **kwargs: Any) -> str:
        # Graceful stub if no key/SDK
        if not self.is_available():
            return f"[google-stub] {prompt[:200]}"
        attempts = 0
        last_err: Optional[AdapterError] = None
        t0 = time.time()
        deadline = t0 + max(self._timeout_s, self._max_elapsed_s)
        while attempts < self._max_attempts and time.time() < deadline:
            attempts += 1
            try:
                # Some versions support generation_config; keep simple for compatibility
                resp = None
                try:
                    resp = self._model.generate_content(prompt)
                except TypeError as te:
                    # Fallback call signature if library changes
                    resp = self._model.generate_content(contents=prompt)
                # Extract text consistently across SDK versions
                text = None
                if hasattr(resp, "text"):
                    text = getattr(resp, "text", "")
                elif hasattr(resp, "candidates") and resp.candidates:
                    c0 = resp.candidates[0]
                    text = getattr(c0, "content", {}).get("parts", [{}])[0].get("text", "") if isinstance(getattr(c0, "content", None), dict) else ""
                text = (text or "").strip()
                record_adapter_event("google", (time.time()-t0)*1000.0, attempts-1, status="ok", cache_hit=False)
                return text
            except Exception as e:
                err = normalize_error("google", e)
                last_err = err
                retryable = err.code in {"RATE_LIMITED", "PROVIDER_ERROR", "NETWORK_ERROR", "PROVIDER_TIMEOUT"}
                if not retryable:
                    record_adapter_event("google", (time.time()-t0)*1000.0, attempts-1, status="error", cache_hit=False, code=err.code)
                    raise err
                delay = self._base_delay_s * (2 ** max(0, attempts-1)) + random.random() * self._jitter_s
                if err.retry_after_ms:
                    delay = max(delay, err.retry_after_ms / 1000.0)
                remaining = max(0.0, deadline - time.time())
                if remaining <= 0.01:
                    break
                time.sleep(min(delay, remaining))

        record_adapter_event("google", (time.time()-t0)*1000.0, attempts-1, status="error", cache_hit=False, code=(last_err.code if last_err else "PROVIDER_ERROR"))
        raise (last_err or AdapterError(code="PROVIDER_ERROR", hint="Exceeded retry/time budget.", provider="google"))

    def is_available(self) -> bool:
        return self._model is not None


# Register in the global registry
registry.register("google", GoogleAdapter())