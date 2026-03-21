from __future__ import annotations
import os, requests, time
from .base import BaseAdapter, Generation, ProviderError, AdapterRegistry

class HFInferenceAdapter(BaseAdapter):
    name = "hf"
    def generate(self, prompt: str, **kwargs) -> Generation:
        api = os.getenv("HF_API_URL")  # e.g., https://api-inference.huggingface.co/models/<repo-id>
        key = os.getenv("HF_API_TOKEN")
        if not api or not key:
            raise ProviderError("HF_API_URL or HF_API_TOKEN not set")
        timeout = kwargs.get("timeout_s", 15)
        t0 = time.time()
        try:
            r = requests.post(api, headers={"Authorization": f"Bearer {key}"}, json={"inputs": prompt}, timeout=timeout)
            if r.status_code >= 400:
                raise ProviderError(f"HF HTTP {r.status_code}: {r.text[:200]}")
            data = r.json()
            # Best-effort text extraction for generic endpoints
            if isinstance(data, list) and data and isinstance(data[0], dict):
                text = data[0].get("generated_text","")
            else:
                text = str(data)
            latency = int((time.time()-t0)*1000)
            return Generation(text=text, metadata={"vendor":"hf","arch_family":"tgi","latency_ms":latency})
        except requests.Timeout as e:
            raise ProviderError(f"HF timeout: {e}")

AdapterRegistry.global_registry().register(HFInferenceAdapter())