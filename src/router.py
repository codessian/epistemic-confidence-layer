from __future__ import annotations
import time, json, os, random
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple

from .adapters.base import Generation, BaseAdapter, AdapterRegistry, ProviderError
from .cache import FileCache

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
    select: Dict[str, Any]      # {type: "quorum_k_of_n", k:2, providers:[...]}
    constraints: Dict[str, Any] = field(default_factory=dict)  # {min_diversity_score: 0.6, max_latency_ms: 4000, budget_usd: 0.25}

def _diversity_score(chosen: List[Generation]) -> float:
    # Simple diversity proxy: prefer distinct vendor & arch
    vendors = {g.metadata.get("vendor") for g in chosen}
    archs   = {g.metadata.get("arch_family") for g in chosen}
    return (len(vendors) + len(archs)) / (2.0 * max(1, len(chosen)))

class DynamicRouter:
    """
    Chooses N providers per policy, orchestrates calls with budget/latency guards,
    returns generations + rich metadata for consensus/provenance.
    """
    def __init__(self, provider_specs: List[ProviderSpec], policy: RoutePolicy):
        self.provider_specs = {p.id: p for p in provider_specs}
        self.policy = policy
        from .adapters.base import registry
        self.registry = registry
        self.cache = FileCache()

    def _pick_providers(self) -> List[ProviderSpec]:
        cfg = self.policy.select
        ids = cfg.get("providers", [])
        random.shuffle(ids)
        k = min(cfg.get("k", 2), len(ids))
        return [self.provider_specs[i] for i in ids[:k]]

    def generate(self, prompt: str, route_id: Optional[str]=None, **kwargs) -> Tuple[List[Generation], Dict[str, Any]]:
        route_id = route_id or f"route-{int(time.time()*1000)}"
        t0 = time.time()
        chosen = self._pick_providers()
        budget = float(self.policy.constraints.get("budget_usd", 0.25))
        max_latency_ms = int(self.policy.constraints.get("max_latency_ms", 4000))
        spent = 0.0
        gens: List[Generation] = []

        for spec in chosen:
            adapter = self.registry.get(spec.kind)
            if not adapter:
                continue
            # PII guard
            if not spec.allow_pii and kwargs.get("contains_pii"):
                continue
            # TTL cache for idempotent calls
            cache_key = f"gen::{spec.kind}::{spec.model}::{prompt}"
            cached = self.cache.get(key=cache_key)
            if cached:
                gen = Generation(text=cached["text"], metadata=cached["metadata"])
                gens.append(gen)
                continue
            t1 = time.time()
            try:
                gen = adapter.generate(
                    prompt,
                    model=spec.model,
                    timeout_s=min(max_latency_ms/1000.0, kwargs.get("timeout_s", max_latency_ms/1000.0)),
                    route_id=route_id,
                )
                t2 = time.time()
                spent += gen.metadata.get("cost_usd", 0.0)
                gen.metadata.update({
                    "provider_id": spec.id,
                    "model": spec.model,
                    "vendor": gen.metadata.get("vendor", spec.kind),
                    "arch_family": gen.metadata.get("arch_family", "unknown"),
                    "latency_ms": int((t2 - t1)*1000),
                    "route_id": route_id,
                })
                # budget/latency guards
                if (t2 - t0)*1000 > max_latency_ms or spent > budget:
                    gens.append(gen)
                    break
                gens.append(gen)
                # cache store (respect adapter's suggested TTL)
                ttl = int(os.getenv("ECL_CACHE_TTL_HOURS", "1")) * 3600
                self.cache.set({"text": gen.text, "metadata": gen.metadata}, key=cache_key)
            except ProviderError as e:
                gens.append(Generation(text="", metadata={
                    "provider_id": spec.id,
                    "model": spec.model,
                    "error": str(e),
                    "route_id": route_id,
                }))
        meta = {
            "route_id": route_id,
            "policy": self.policy.name,
            "diversity_score": _diversity_score(gens) if gens else 0.0,
            "budget_spent_usd": round(spent, 6),
            "elapsed_ms": int((time.time()-t0)*1000),
        }
        return gens, meta