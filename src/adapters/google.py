from __future__ import annotations

import os
import random
import time
from typing import Any

try:
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover
    genai = None

from .base import AdapterRequest, BaseAdapter, Generation, coerce_adapter_request, make_generation
from ..errors import AdapterError, normalize_error
from ..adapter_metrics import record_adapter_event


class GoogleAdapter(BaseAdapter):
    provider_kind = "google"
    vendor = "google"
    arch_family = "gemini"

    def __init__(self, model_id: str = "gemini-1.5-flash", **kwargs: Any):
        super().__init__(model_id, **kwargs)
        api_key = os.getenv("GOOGLE_API_KEY")
        self._timeout_s = float(os.getenv("ECL_PROVIDER_TIMEOUT_S", "8.0"))
        self._max_attempts = int(os.getenv("ECL_PROVIDER_MAX_ATTEMPTS", "3"))
        self._max_elapsed_s = float(os.getenv("ECL_PROVIDER_MAX_ELAPSED_S", "16.0"))
        self._base_delay_s = float(os.getenv("ECL_PROVIDER_BASE_DELAY_S", "0.6"))
        self._jitter_s = float(os.getenv("ECL_PROVIDER_JITTER_S", "0.2"))
        try:
            if genai and api_key:
                genai.configure(api_key=api_key)
                self._model = genai.GenerativeModel(self.model_id)
            else:
                self._model = None
        except Exception:
            self._model = None

    def generate(self, req: AdapterRequest | str, **kwargs: Any) -> Generation:
        req = coerce_adapter_request(self.model_id, req, **kwargs)
        if not self.is_available():
            return make_generation(
                text=f"[google-stub] {req.prompt[:200]}",
                provider_id=self.provider_kind,
                provider_kind=self.provider_kind,
                model=req.model,
                vendor=self.vendor,
                arch_family=self.arch_family,
                latency_ms=0,
                route_id=req.route_id,
                request_id=req.request_id,
            )
        attempts = 0
        last_err: AdapterError | None = None
        t0 = time.time()
        deadline = t0 + max(self._timeout_s, self._max_elapsed_s)
        while attempts < self._max_attempts and time.time() < deadline:
            attempts += 1
            try:
                try:
                    resp = self._model.generate_content(req.prompt)
                except TypeError:
                    resp = self._model.generate_content(contents=req.prompt)
                text: str | None = None
                if hasattr(resp, "text"):
                    text = getattr(resp, "text", "")
                elif hasattr(resp, "candidates") and resp.candidates:
                    c0 = resp.candidates[0]
                    if isinstance(getattr(c0, "content", None), dict):
                        text = getattr(c0, "content", {}).get("parts", [{}])[0].get("text", "")
                text = (text or "").strip()
                elapsed_ms = int((time.time() - t0) * 1000)
                record_adapter_event("google", elapsed_ms, attempts - 1, status="ok", cache_hit=False)
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
                err = normalize_error("google", exc)
                last_err = err
                retryable = err.code in {"RATE_LIMITED", "PROVIDER_ERROR", "NETWORK_ERROR", "PROVIDER_TIMEOUT"}
                if not retryable:
                    record_adapter_event(
                        "google",
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
            "google",
            (time.time() - t0) * 1000.0,
            attempts - 1,
            status="error",
            cache_hit=False,
            code=(last_err.code if last_err else "PROVIDER_ERROR"),
        )
        raise (last_err or AdapterError(code="PROVIDER_ERROR", hint="Exceeded retry/time budget.", provider="google"))

    def is_available(self) -> bool:
        return self._model is not None
