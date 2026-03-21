from __future__ import annotations

import os
import time
from typing import Any

from .base import AdapterRequest, BaseAdapter, Generation, coerce_adapter_request, make_generation
from ..errors import AdapterError

class GeminiAdapter(BaseAdapter):
    provider_kind = "gemini"
    vendor = "google"
    arch_family = "gemini"

    def generate(self, req: AdapterRequest | str, **kwargs: Any) -> Generation:
        req = coerce_adapter_request(self.model_id, req, **kwargs)
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            return make_generation(
                text=f"[gemini-stub] {req.prompt[:200]}",
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
            import google.generativeai as genai  # type: ignore
        except Exception as exc:
            raise AdapterError(code="PROVIDER_ERROR", hint=f"Gemini SDK not available: {exc}", provider="gemini")
        t0 = time.time()
        genai.configure(api_key=key)
        try:
            model = genai.GenerativeModel(req.model)
            resp = model.generate_content(req.prompt)
            text = getattr(resp, "text", "") or ""
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
        except Exception as exc:
            raise AdapterError(code="PROVIDER_ERROR", hint=f"Gemini error: {exc}", provider="gemini")

    def is_available(self) -> bool:
        return bool(os.getenv("GEMINI_API_KEY"))
