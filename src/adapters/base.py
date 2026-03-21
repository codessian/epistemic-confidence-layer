"""Base adapter interface for model providers with TTL caching and typed requests."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from ..adapter_metrics import record_adapter_event
from ..cache import get as cache_get
from ..cache import set as cache_set
from ..errors import AdapterError


@dataclass
class AdapterRequest:
    prompt: str
    model: str
    timeout_s: float
    route_id: str
    request_id: str
    contains_pii: bool
    temperature: float | None = None
    max_tokens: int | None = None


@dataclass
class Generation:
    """Canonical generation result with text and metadata."""
    text: str
    metadata: Dict[str, Any]


@dataclass
class GenerationError:
    provider_id: str
    provider_kind: str
    model: str
    code: str
    message: str
    retryable: bool
    retry_after_ms: int | None


AdapterResponse = Generation
ProviderError = AdapterError


class AdapterNotRegisteredError(KeyError):
    """Raised when an adapter kind is missing from the registry."""


class BaseAdapter(ABC):
    """Abstract base class for all model adapters."""

    provider_kind: str = "unknown"
    vendor: str = "unknown"
    arch_family: str = "unknown"

    def __init__(self, model_id: str, **kwargs: Any):
        self.model_id = model_id
        self.config = kwargs

    @abstractmethod
    def generate(self, req: AdapterRequest | str, **kwargs: Any) -> Generation:
        """Generate a response from the model."""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the adapter is properly configured and available."""

    def available(self) -> bool:
        return self.is_available()


class AdapterRegistry:
    """Registry for managing model adapters."""

    def __init__(self):
        self._adapters: Dict[str, BaseAdapter] = {}

    def register(self, name: str, adapter: BaseAdapter) -> None:
        self._adapters[name] = adapter

    def get(self, name: str) -> BaseAdapter:
        adapter = self._adapters.get(name)
        if adapter is None:
            raise AdapterNotRegisteredError(f"Adapter '{name}' not found")
        return adapter

    def get_optional(self, name: str) -> BaseAdapter | None:
        return self._adapters.get(name)

    def list_available(self) -> List[str]:
        return [name for name, adapter in self._adapters.items() if adapter.is_available()]

    def list(self) -> Dict[str, BaseAdapter]:
        return dict(self._adapters)


registry = AdapterRegistry()


def coerce_adapter_request(
    default_model_id: str,
    req_or_prompt: AdapterRequest | str,
    **kwargs: Any,
) -> AdapterRequest:
    if isinstance(req_or_prompt, AdapterRequest):
        return req_or_prompt
    return AdapterRequest(
        prompt=req_or_prompt,
        model=str(kwargs.get("model", default_model_id)),
        timeout_s=float(kwargs.get("timeout_s", 8.0)),
        route_id=str(kwargs.get("route_id", "route-legacy")),
        request_id=str(kwargs.get("request_id", "legacy-request")),
        contains_pii=bool(kwargs.get("contains_pii", False)),
        temperature=(float(kwargs["temperature"]) if kwargs.get("temperature") is not None else None),
        max_tokens=(int(kwargs["max_tokens"]) if kwargs.get("max_tokens") is not None else None),
    )


def make_generation(
    text: str,
    *,
    provider_id: str,
    provider_kind: str,
    model: str,
    vendor: str,
    arch_family: str,
    latency_ms: int,
    route_id: str,
    request_id: str,
    **extra_metadata: Any,
) -> Generation:
    metadata: Dict[str, Any] = {
        "provider_id": provider_id,
        "provider_kind": provider_kind,
        "model": model,
        "vendor": vendor,
        "arch_family": arch_family,
        "latency_ms": int(latency_ms),
        "route_id": route_id,
        "request_id": request_id,
    }
    metadata.update(extra_metadata)
    return Generation(text=text, metadata=metadata)


def _cache_key_from_request(req: AdapterRequest) -> Tuple[Any, ...]:
    filtered = {
        "model": req.model,
        "temperature": req.temperature,
        "max_tokens": req.max_tokens,
        "timeout_s": req.timeout_s,
        "contains_pii": req.contains_pii,
    }
    stable = {k: v for k, v in filtered.items() if v is not None}
    return (req.prompt, tuple(sorted(stable.items())))


def generate_with_cache(
    adapter: BaseAdapter,
    req_or_prompt: AdapterRequest | str,
    **kwargs: Any,
) -> Generation:
    req = coerce_adapter_request(adapter.model_id, req_or_prompt, **kwargs)
    key = _cache_key_from_request(req)
    namespace = adapter.__class__.__name__.lower()
    slug = namespace.replace("adapter", "")
    hit = cache_get(namespace, key)
    if hit is not None:
        record_adapter_event(slug, elapsed_ms=0.0, retries=0, status="ok", cache_hit=True, code="CACHE_HIT")
        if isinstance(hit, dict):
            return Generation(text=str(hit.get("text", "")), metadata=dict(hit.get("metadata", {})))
        return make_generation(
            text=str(hit),
            provider_id=slug,
            provider_kind=getattr(adapter, "provider_kind", slug),
            model=req.model,
            vendor=getattr(adapter, "vendor", slug),
            arch_family=getattr(adapter, "arch_family", "unknown"),
            latency_ms=0,
            route_id=req.route_id,
            request_id=req.request_id,
        )
    out = adapter.generate(req)
    cache_set(namespace, key, {"text": out.text, "metadata": out.metadata})
    return out
