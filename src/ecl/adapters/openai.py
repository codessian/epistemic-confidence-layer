"""OpenAI adapter implementation with env-based stub fallback and registry."""

import os
from typing import Any
from .base import BaseAdapter, registry

try:  # pragma: no cover
    from openai import OpenAI
except Exception:
    OpenAI = None  # type: ignore


class OpenAIAdapter(BaseAdapter):
    """Adapter for OpenAI models with graceful fallback when unavailable."""

    def __init__(self, model_id: str = "gpt-4o-mini", **kwargs: Any):
        super().__init__(model_id, **kwargs)
        api_key = os.getenv("OPENAI_API_KEY")
        self._client = OpenAI(api_key=api_key) if (OpenAI and api_key) else None

    def generate(self, prompt: str, **kwargs: Any) -> str:
        if self._client is None:
            return f"[openai-stub] {prompt[:200]}"
        model = kwargs.get("model", self.model_id)
        temperature = float(kwargs.get("temperature", 0.2))
        max_tokens = int(kwargs.get("max_tokens", 256))
        resp = self._client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return (resp.choices[0].message.content or "").strip()

    def is_available(self) -> bool:
        return self._client is not None

# Register in the global registry for smoke tests and usage
registry.register("openai", OpenAIAdapter())