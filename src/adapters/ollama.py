from __future__ import annotations

import time
from typing import Any

import requests

from .base import AdapterRequest, BaseAdapter, Generation, coerce_adapter_request, make_generation
from ..errors import AdapterError

class OllamaAdapter(BaseAdapter):
    provider_kind = "ollama"
    vendor = "ollama"
    arch_family = "local"

    def generate(self, req: AdapterRequest | str, **kwargs: Any) -> Generation:
        req = coerce_adapter_request(self.model_id, req, **kwargs)
        t0 = time.time()
        try:
            r = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={"model": req.model, "prompt": req.prompt, "stream": False},
                timeout=req.timeout_s,
            )
            if r.status_code >= 400:
                raise AdapterError(
                    code="BAD_REQUEST" if r.status_code < 500 else "PROVIDER_ERROR",
                    hint=f"Ollama HTTP {r.status_code}: {r.text[:200]}",
                    provider="ollama",
                    status=r.status_code,
                )
            data = r.json()
            latency = int((time.time()-t0)*1000)
            return make_generation(
                text=data.get("response", ""),
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
            raise AdapterError(code="PROVIDER_TIMEOUT", hint=f"Ollama timeout: {e}", provider="ollama", status=504, cause=e)
        except requests.RequestException:
            return make_generation(
                text=f"[ollama-stub] {req.prompt[:200]}",
                provider_id=self.provider_kind,
                provider_kind=self.provider_kind,
                model=req.model,
                vendor=self.vendor,
                arch_family=self.arch_family,
                latency_ms=0,
                route_id=req.route_id,
                request_id=req.request_id,
            )

    def is_available(self) -> bool:
        return True
