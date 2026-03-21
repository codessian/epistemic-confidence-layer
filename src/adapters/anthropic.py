from __future__ import annotations

import os
import random
import time
from typing import Any

AnthropicClient: Any = None
try:
    from anthropic import Anthropic as AnthropicClient  # type: ignore
except Exception:
    AnthropicClient = None

from .base import AdapterRequest, BaseAdapter, Generation, coerce_adapter_request, make_generation
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
    provider_kind = "anthropic"
    vendor = "anthropic"
    arch_family = "claude"

    def __init__(self, model_id: str = "claude-3-haiku-20240307", **kwargs: Any):
        super().__init__(model_id, **kwargs)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self._timeout_s = float(os.getenv("ECL_PROVIDER_TIMEOUT_S", "8.0"))
        self._max_attempts = int(os.getenv("ECL_PROVIDER_MAX_ATTEMPTS", "3"))
        self._max_elapsed_s = float(os.getenv("ECL_PROVIDER_MAX_ELAPSED_S", "16.0"))
        self._base_delay_s = float(os.getenv("ECL_PROVIDER_BASE_DELAY_S", "0.6"))
        self._jitter_s = float(os.getenv("ECL_PROVIDER_JITTER_S", "0.2"))
        self._client = None
        self._has_key = bool(AnthropicClient) and bool(api_key)

    def generate(self, req: AdapterRequest | str, **kwargs: Any) -> Generation:
        req = coerce_adapter_request(self.model_id, req, **kwargs)
        if self._client is None:
            if not self._has_key:
                return make_generation(
                    text=f"[anthropic-stub] {req.prompt[:200]}",
                    provider_id=self.provider_kind,
                    provider_kind=self.provider_kind,
                    model=req.model,
                    vendor=self.vendor,
                    arch_family=self.arch_family,
                    latency_ms=0,
                    route_id=req.route_id,
                    request_id=req.request_id,
                )
            try:
                self._client = AnthropicClient(api_key=os.getenv("ANTHROPIC_API_KEY"))
            except Exception:
                return make_generation(
                    text=f"[anthropic-stub] {req.prompt[:200]}",
                    provider_id=self.provider_kind,
                    provider_kind=self.provider_kind,
                    model=req.model,
                    vendor=self.vendor,
                    arch_family=self.arch_family,
                    latency_ms=0,
                    route_id=req.route_id,
                    request_id=req.request_id,
                )
        temperature = float(req.temperature if req.temperature is not None else 0.2)
        max_tokens = int(req.max_tokens if req.max_tokens is not None else 256)

        t0 = time.time()
        attempts = 0
        deadline = t0 + self._max_elapsed_s
        last_err: AdapterError | None = None

        while attempts < self._max_attempts and time.time() < deadline:
            attempts += 1
            remaining = max(0.1, deadline - time.time())
            call_timeout = min(req.timeout_s or self._timeout_s, remaining, self._timeout_s)
            try:
                try:
                    resp = self._client.messages.create(
                        model=req.model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        messages=[{"role": "user", "content": req.prompt}],
                        timeout=call_timeout,
                    )
                except TypeError:
                    resp = self._client.completions.create(
                        model=req.model,
                        max_tokens_to_sample=max_tokens,
                        temperature=temperature,
                        prompt=req.prompt,
                    )
                text = _extract_text(resp)
                elapsed_ms = int((time.time() - t0) * 1000)
                record_adapter_event("anthropic", elapsed_ms, attempts - 1, status="ok", cache_hit=False)
                return make_generation(
                    text=text,
                    provider_id=self.provider_kind,
                    provider_kind=self.provider_kind,
                    model=req.model,
                    vendor=self.vendor,
                    arch_family=self.arch_family,
                    latency_ms=elapsed_ms,
                    route_id=req.route_id,
                    request_id=req.request_id,
                )
            except Exception as exc:
                err = normalize_error("anthropic", exc)
                last_err = err
                retryable = err.code in {"RATE_LIMITED", "PROVIDER_ERROR", "NETWORK_ERROR", "PROVIDER_TIMEOUT"}
                if not retryable:
                    record_adapter_event(
                        "anthropic",
                        (time.time() - t0) * 1000.0,
                        attempts - 1,
                        status="error",
                        cache_hit=False,
                        code=err.code,
                    )
                    raise err
                delay = self._base_delay_s * (2 ** max(0, attempts - 1)) + random.random() * self._jitter_s
                if err.retry_after_ms:
                    delay = max(delay, err.retry_after_ms / 1000.0)
                remaining = max(0.0, deadline - time.time())
                if remaining <= 0.01:
                    break
                time.sleep(min(delay, remaining))

        record_adapter_event(
            "anthropic",
            (time.time() - t0) * 1000.0,
            attempts - 1,
            status="error",
            cache_hit=False,
            code=(last_err.code if last_err else "PROVIDER_ERROR"),
        )
        raise (last_err or AdapterError(code="PROVIDER_ERROR", hint="Exceeded retry/time budget.", provider="anthropic"))

    def is_available(self) -> bool:
        return self._has_key
