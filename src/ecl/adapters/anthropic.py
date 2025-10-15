from __future__ import annotations
"""Anthropic adapter with robust generate(): timeouts, retries, and error normalization."""

import os
import time
import random
from typing import Any

try:
    from anthropic import Anthropic  # type: ignore
except Exception:
    Anthropic = None

from .base import BaseAdapter
from ..errors import AdapterError, normalize_error
from ..adapter_metrics import record_adapter_event


def _extract_text(resp: Any) -> str:
    # Try messages API shape first
    content = getattr(resp, "content", None)
    if isinstance(content, list):
        parts = []
        for c in content:
            t = None
            if isinstance(c, dict):
                t = c.get("text") or c.get("content")
            else:
                t = getattr(c, "text", None)
            if t:
                parts.append(t)
        if parts:
            return "\n".join(p.strip() for p in parts if p)
    # Fallback: completion-style
    txt = getattr(resp, "completion", None) or getattr(resp, "text", None)
    if isinstance(txt, str):
        return txt.strip()
    return ""


class AnthropicAdapter(BaseAdapter):
    """Adapter for Anthropic models with graceful fallback when unavailable."""

    def __init__(self, model_id: str = "claude-3-haiku-20240307", **kwargs: Any):
        super().__init__(model_id, **kwargs)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        # Config
        self._timeout_s = float(os.getenv("ECL_PROVIDER_TIMEOUT_S", "8.0"))
        self._max_attempts = int(os.getenv("ECL_PROVIDER_MAX_ATTEMPTS", "3"))
        self._max_elapsed_s = float(os.getenv("ECL_PROVIDER_MAX_ELAPSED_S", "16.0"))
        self._base_delay_s = float(os.getenv("ECL_PROVIDER_BASE_DELAY_S", "0.6"))
        self._jitter_s = float(os.getenv("ECL_PROVIDER_JITTER_S", "0.2"))
        # Defer client creation to avoid import-time failures across SDK versions
        self._client = None
        self._has_key = bool(Anthropic) and bool(api_key)

    def generate(self, prompt: str, **kwargs: Any) -> str:
        if self._client is None:
            if not self._has_key:
                return f"[anthropic-stub] {prompt[:200]}"
            try:
                self._client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            except Exception:
                return f"[anthropic-stub] {prompt[:200]}"
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
                # Prefer messages API; only fallback on TypeError (unsupported args/SDK)
                try:
                    resp = self._client.messages.create(
                        model=model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        messages=[{"role": "user", "content": prompt}],
                        timeout=call_timeout,
                    )
                except TypeError:
                    # Fallback to older completions API
                    resp = self._client.completions.create(
                        model=model,
                        max_tokens_to_sample=max_tokens,
                        temperature=temperature,
                        prompt=prompt,
                    )
                text = _extract_text(resp)
                record_adapter_event("anthropic", (time.time()-t0)*1000.0, attempts-1, status="ok", cache_hit=False)
                return text
            except Exception as e:
                err = normalize_error("anthropic", e)
                last_err = err
                retryable = err.code in {"RATE_LIMITED", "PROVIDER_ERROR", "NETWORK_ERROR", "PROVIDER_TIMEOUT"}
                if not retryable:
                    record_adapter_event("anthropic", (time.time()-t0)*1000.0, attempts-1, status="error", cache_hit=False, code=err.code)
                    raise err
                delay = self._base_delay_s * (2 ** max(0, attempts-1)) + random.random() * self._jitter_s
                if err.retry_after_ms:
                    delay = max(delay, err.retry_after_ms / 1000.0)
                remaining = max(0.0, deadline - time.time())
                if remaining <= 0.01:
                    break
                time.sleep(min(delay, remaining))

        record_adapter_event("anthropic", (time.time()-t0)*1000.0, attempts-1, status="error", cache_hit=False, code=(last_err.code if last_err else "PROVIDER_ERROR"))
        raise (last_err or AdapterError(code="PROVIDER_ERROR", hint="Exceeded retry/time budget.", provider="anthropic"))

    def is_available(self) -> bool:
        return self._has_key


# Registration is optional and should be done by integrators to avoid import-time side effects.