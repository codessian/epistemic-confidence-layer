"""Anthropic adapter implementation with env-based stub fallback and registry."""

import os
from typing import Any
from .base import BaseAdapter, registry

try:  # pragma: no cover
    import anthropic
except Exception:
    anthropic = None  # type: ignore


class AnthropicAdapter(BaseAdapter):
    """Adapter for Anthropic models with graceful fallback when unavailable."""

    def __init__(self, model_id: str = "claude-3-5-sonnet-20240620", **kwargs: Any):
        super().__init__(model_id, **kwargs)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self._client = anthropic.Anthropic(api_key=api_key) if (anthropic and api_key) else None

    def generate(self, prompt: str, **kwargs: Any) -> str:
        if self._client is None:
            return f"[anthropic-stub] {prompt[:200]}"
        model = kwargs.get("model", self.model_id)
        temperature = float(kwargs.get("temperature", 0.2))
        max_tokens = int(kwargs.get("max_tokens", 256))
        resp = self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        # Normalize to string
        try:
            parts = [b.text for b in resp.content if getattr(b, "type", "") == "text"]
            return "\n".join(parts).strip()
        except Exception:
            return str(resp)

    def is_available(self) -> bool:
        return self._client is not None

# Register in the global registry for smoke tests and usage
registry.register("anthropic", AnthropicAdapter())