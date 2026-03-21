from __future__ import annotations

import os
import time
from typing import Any

from .base import AdapterRequest, BaseAdapter, Generation, coerce_adapter_request, make_generation
from ..errors import AdapterError

class VertexAIAdapter(BaseAdapter):
    provider_kind = "vertex"
    vendor = "google"
    arch_family = "gemini/vertex"

    def generate(self, req: AdapterRequest | str, **kwargs: Any) -> Generation:
        req = coerce_adapter_request(self.model_id, req, **kwargs)
        project = os.getenv("VERTEX_PROJECT")
        location = os.getenv("VERTEX_LOCATION","us-central1")
        if not project:
            return make_generation(
                text=f"[vertex-stub] {req.prompt[:200]}",
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
            from google.cloud import aiplatform  # type: ignore
            from vertexai.preview.generative_models import GenerativeModel  # type: ignore
        except Exception as exc:
            raise AdapterError(code="PROVIDER_ERROR", hint=f"Vertex SDK not available: {exc}", provider="vertex")
        t0 = time.time()
        try:
            aiplatform.init(project=project, location=location)
            m = GenerativeModel(req.model)
            resp = m.generate_content(req.prompt)
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
                region=location,
            )
        except Exception as exc:
            raise AdapterError(code="PROVIDER_ERROR", hint=f"Vertex error: {exc}", provider="vertex")

    def is_available(self) -> bool:
        return bool(os.getenv("VERTEX_PROJECT"))
