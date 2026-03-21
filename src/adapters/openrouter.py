from __future__ import annotations

import os
import time
from typing import Any

import requests

from .base import AdapterRequest, BaseAdapter, Generation, coerce_adapter_request, make_generation
from ..errors import AdapterError

class OpenRouterAdapter(BaseAdapter):
    provider_kind = "openrouter"
    vendor = "openrouter"
    arch_family = "var"

    def generate(self, req: AdapterRequest | str, **kwargs: Any) -> Generation:
        req = coerce_adapter_request(self.model_id, req, **kwargs)
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return make_generation(
                text=f"[openrouter-stub] {req.prompt[:200]}",
                provider_id=self.provider_kind,
                provider_kind=self.provider_kind,
                model=req.model,
                vendor=self.vendor,
                arch_family=self.arch_family,
                latency_ms=0,
                route_id=req.route_id,
                request_id=req.request_id,
            )
        t0 = time.time()
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "HTTP-Referer": "https://github.com/codessian/epistemic-confidence-layer"},
                json={"model": req.model, "messages":[{"role":"user","content":req.prompt}], "temperature":0},
                timeout=req.timeout_s,
            )
            if r.status_code >= 400:
                raise AdapterError(
                    code="BAD_REQUEST" if r.status_code < 500 else "PROVIDER_ERROR",
                    hint=f"OpenRouter HTTP {r.status_code}: {r.text[:200]}",
                    provider="openrouter",
                    status=r.status_code,
                )
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            latency = int((time.time()-t0)*1000)
            return make_generation(
                text=text,
                provider_id=self.provider_kind,
                provider_kind=self.provider_kind,
                model=req.model,
                vendor=self.vendor,
                arch_family=self.arch_family,
                latency_ms=latency,
                route_id=req.route_id,
                request_id=req.request_id,
            )
        except requests.Timeout as e:
            raise AdapterError(code="PROVIDER_TIMEOUT", hint=f"OpenRouter timeout: {e}", provider="openrouter", status=504, cause=e)

    def is_available(self) -> bool:
        return bool(os.getenv("OPENROUTER_API_KEY"))
