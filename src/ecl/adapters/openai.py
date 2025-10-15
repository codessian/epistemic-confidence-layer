from __future__ import annotations
"""OpenAI adapter with robust generate(): timeouts, retries, and error normalization."""

import os
import time
import random
from typing import Any

try:
    from openai import OpenAI  # type: ignore
except Exception:
    OpenAI = None  # graceful fallback

from .base import BaseAdapter
from ..errors import AdapterError, normalize_error
from ..adapter_metrics import record_adapter_event


class OpenAIAdapter(BaseAdapter):
    """Adapter for OpenAI models with graceful fallback when unavailable."""

    def __init__(self, model_id: str = "gpt-4o-mini", **kwargs: Any):
        super().__init__(model_id, **kwargs)
        api_key = os.getenv("OPENAI_API_KEY")
        # Config
        self._timeout_s = float(os.getenv("ECL_PROVIDER_TIMEOUT_S", "8.0"))
        self._max_attempts = int(os.getenv("ECL_PROVIDER_MAX_ATTEMPTS", "3"))
        self._max_elapsed_s = float(os.getenv("ECL_PROVIDER_MAX_ELAPSED_S", "16.0"))
        self._base_delay_s = float(os.getenv("ECL_PROVIDER_BASE_DELAY_S", "0.6"))
        self._jitter_s = float(os.getenv("ECL_PROVIDER_JITTER_S", "0.2"))
        # Defer client creation to avoid import-time failures across SDK versions
        self._client = None
        self._has_key = bool(OpenAI) and bool(api_key)

    def generate(self, prompt: str, **kwargs: Any) -> str:
        # Lazily create client on first real call
        if self._client is None:
            if not self._has_key:
                return f"[openai-stub] {prompt[:200]}"
            try:
                self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except Exception:
                # Fallback: remain in stub mode if SDK init fails
                return f"[openai-stub] {prompt[:200]}"
        model = kwargs.get("model", self.model_id)
        temperature = float(kwargs.get("temperature", 0.2))
        max_tokens = int(kwargs.get("max_tokens", 256))

        t0 = time.time()
        attempts = 0
        deadline = t0 + self._max_elapsed_s
        last_err: AdapterError | None = None

        while attempts < self._max_attempts and time.time() < deadline:
            attempts += 1
            remaining = max(0.1, deadline - time.time())
            call_timeout = min(self._timeout_s, remaining)
            try:
                try:
                    resp = self._client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=temperature,
                        max_tokens=max_tokens,
                        timeout=call_timeout,
                    )
                except TypeError:
                    # Some SDK versions may not accept per-call timeout
                    resp = self._client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                text = (resp.choices[0].message.content or "").strip()
                record_adapter_event("openai", (time.time()-t0)*1000.0, attempts-1, status="ok", cache_hit=False)
                return text
            except Exception as e:
                err = normalize_error("openai", e)
                last_err = err
                # Determine if retry is appropriate
                retryable = err.code in {"RATE_LIMITED", "PROVIDER_ERROR", "NETWORK_ERROR", "PROVIDER_TIMEOUT"}
                if not retryable:
                    record_adapter_event("openai", (time.time()-t0)*1000.0, attempts-1, status="error", cache_hit=False, code=err.code)
                    raise err
                # Compute backoff (respect Retry-After if present)
                delay = self._base_delay_s * (2 ** max(0, attempts-1)) + random.random() * self._jitter_s
                if err.retry_after_ms:
                    delay = max(delay, err.retry_after_ms / 1000.0)
                # Respect remaining time
                remaining = max(0.0, deadline - time.time())
                if remaining <= 0.01:
                    break
                time.sleep(min(delay, remaining))

        # Exhausted attempts or time
        record_adapter_event("openai", (time.time()-t0)*1000.0, attempts-1, status="error", cache_hit=False, code=(last_err.code if last_err else "PROVIDER_ERROR"))
        raise (last_err or AdapterError(code="PROVIDER_ERROR", hint="Exceeded retry/time budget.", provider="openai"))

    def is_available(self) -> bool:
        return self._has_key


# Registration is optional and should be done by integrators to avoid import-time side effects.