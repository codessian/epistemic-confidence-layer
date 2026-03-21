from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .adapters.base import (
    AdapterNotRegisteredError,
    AdapterRegistry,
    AdapterRequest,
    Generation,
    GenerationError,
)
from .cache import FileCache
from .errors import AdapterError, to_generation_error

@dataclass
class ProviderSpec:
    id: str
    kind: str                 # "gemini" | "vertex" | "ollama" | "hf" | "openrouter" | "openai" | "anthropic"
    model: str
    allow_pii: bool = False
    region: Optional[str] = None
    max_tps: Optional[float] = None

@dataclass
class RoutePolicy:
    name: str
    select: Dict[str, Any]
    constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RouteRequest:
    prompt: str
    contains_pii: bool
    timeout_s: float
    request_id: str
    strategy_name: str | None = None


@dataclass
class RouteMeta:
    route_id: str
    policy: str
    diversity_score: float
    budget_spent_usd: float
    elapsed_ms: int


@dataclass
class RouteResult:
    generations: list[Generation]
    errors: list[GenerationError]
    meta: RouteMeta

def _diversity_score(chosen: List[Generation]) -> float:
    vendors = {g.metadata.get("vendor") for g in chosen if g.metadata.get("vendor")}
    archs = {g.metadata.get("arch_family") for g in chosen if g.metadata.get("arch_family")}
    return (len(vendors) + len(archs)) / (2.0 * max(1, len(chosen)))

class DynamicRouter:
    def __init__(self, provider_specs: List[ProviderSpec], policy: RoutePolicy, registry: AdapterRegistry | None = None):
        self.provider_specs = {p.id: p for p in provider_specs}
        self.policy = policy
        if registry is None:
            from .adapters.base import registry as global_registry
            registry = global_registry
        self.registry = registry
        self.cache = FileCache()

    def validate_policy(self) -> None:
        cfg = self.policy.select
        ids = cfg.get("providers", [])
        for provider_id in ids:
            if provider_id not in self.provider_specs:
                raise ValueError(f"Unknown provider ID in policy: {provider_id}")
            kind = self.provider_specs[provider_id].kind
            if self.registry.get_optional(kind) is None:
                raise AdapterNotRegisteredError(
                    f"Adapter kind '{kind}' required by provider '{provider_id}' is not registered"
                )

    def _pick_providers(self) -> list[ProviderSpec]:
        cfg = self.policy.select
        ids = list(cfg.get("providers", []))
        random.shuffle(ids)
        k = min(cfg.get("k", 2), len(ids))
        return [self.provider_specs[i] for i in ids[:k]]

    def generate(self, req: RouteRequest, route_id: str | None = None) -> RouteResult:
        route_id = route_id or f"route-{int(time.time()*1000)}"
        t0 = time.time()
        self.validate_policy()
        chosen = self._pick_providers()
        budget = float(self.policy.constraints.get("budget_usd", 0.25))
        max_latency_ms = int(self.policy.constraints.get("max_latency_ms", 4000))
        spent = 0.0
        generations: list[Generation] = []
        errors: list[GenerationError] = []

        for spec in chosen:
            if not spec.allow_pii and req.contains_pii:
                errors.append(
                    GenerationError(
                        provider_id=spec.id,
                        provider_kind=spec.kind,
                        model=spec.model,
                        code="BAD_REQUEST",
                        message="PII not allowed for selected provider",
                        retryable=False,
                        retry_after_ms=None,
                    )
                )
                continue

            adapter = self.registry.get(spec.kind)
            adapter_req = AdapterRequest(
                prompt=req.prompt,
                model=spec.model,
                timeout_s=min(max_latency_ms / 1000.0, req.timeout_s),
                route_id=route_id,
                request_id=req.request_id,
                contains_pii=req.contains_pii,
            )
            cache_key = f"gen::{spec.kind}::{spec.model}::{req.prompt}"
            cached = self.cache.get(key=cache_key)
            if cached:
                gen = Generation(text=cached["text"], metadata=cached["metadata"])
                generations.append(gen)
                continue

            try:
                gen = adapter.generate(adapter_req)
                gen.metadata.setdefault("provider_id", spec.id)
                gen.metadata.setdefault("provider_kind", spec.kind)
                gen.metadata.setdefault("model", spec.model)
                gen.metadata.setdefault("route_id", route_id)
                gen.metadata.setdefault("request_id", req.request_id)
                spent += float(gen.metadata.get("cost_usd", 0.0) or 0.0)
                generations.append(gen)
                self.cache.set({"text": gen.text, "metadata": gen.metadata}, key=cache_key)
                if (time.time() - t0) * 1000 > max_latency_ms or spent > budget:
                    break
            except AdapterError as exc:
                errors.append(to_generation_error(exc, provider_id=spec.id, provider_kind=spec.kind, model=spec.model))

        meta = RouteMeta(
            route_id=route_id,
            policy=self.policy.name,
            diversity_score=_diversity_score(generations) if generations else 0.0,
            budget_spent_usd=round(spent, 6),
            elapsed_ms=int((time.time() - t0) * 1000),
        )
        return RouteResult(generations=generations, errors=errors, meta=meta)
