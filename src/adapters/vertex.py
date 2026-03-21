from __future__ import annotations
import os, time
from .base import BaseAdapter, Generation, ProviderError, AdapterRegistry

class VertexAIAdapter(BaseAdapter):
    name = "vertex"
    def generate(self, prompt: str, **kwargs) -> Generation:
        project = os.getenv("VERTEX_PROJECT")
        location = os.getenv("VERTEX_LOCATION","us-central1")
        if not project:
            raise ProviderError("VERTEX_PROJECT not set")
        try:
            from google.cloud import aiplatform
        except Exception as e:
            raise ProviderError(f"Vertex SDK not available: {e}")
        model = kwargs.get("model", "gemini-1.5-flash")
        t0 = time.time()
        try:
            aiplatform.init(project=project, location=location)
            from vertexai.preview.generative_models import GenerativeModel
            m = GenerativeModel(model)
            resp = m.generate_content(prompt)
            text = getattr(resp, "text", "") or ""
            latency = int((time.time()-t0)*1000)
            return Generation(text=text, metadata={"vendor":"google","arch_family":"gemini/vertex","latency_ms":latency, "region": location})
        except Exception as e:
            raise ProviderError(f"Vertex error: {e}")

AdapterRegistry.global_registry().register(VertexAIAdapter())