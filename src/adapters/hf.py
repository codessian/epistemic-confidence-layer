from __future__ import annotations

import os
import time
from typing import Any

import requests

from .base import AdapterRequest, BaseAdapter, Generation, coerce_adapter_request, make_generation
from ..errors import AdapterError

class HFInferenceAdapter(BaseAdapter):
    provider_kind = "hf"
    vendor = "hf"
    arch_family = "tgi"

    def generate(self, req: AdapterRequest | str, **kwargs: Any) -> Generation:
        req = coerce_adapter_request(self.model_id, req, **kwargs)
        api = os.getenv("HF_API_URL")
        key = os.getenv("HF_API_TOKEN")
        if not api or not key:
            return make_generation(
                text=f"[hf-stub] {req.prompt[:200]}",
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
            r = requests.post(api, headers={"Authorization": f"Bearer {key}"}, json={"inputs": req.prompt}, timeout=req.timeout_s)
            if r.status_code >= 400:
                raise AdapterError(
                    code="BAD_REQUEST" if r.status_code < 500 else "PROVIDER_ERROR",
                    hint=f"HF HTTP {r.status_code}: {r.text[:200]}",
                    provider="hf",
                    status=r.status_code,
                )
            data = r.json()
            if isinstance(data, list) and data and isinstance(data[0], dict):
                text = data[0].get("generated_text","")
            else:
                text = str(data)
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
            raise AdapterError(code="PROVIDER_TIMEOUT", hint=f"HF timeout: {e}", provider="hf", status=504, cause=e)

    def is_available(self) -> bool:
        return bool(os.getenv("HF_API_URL")) and bool(os.getenv("HF_API_TOKEN"))
