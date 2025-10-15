"""Base adapter interface for model providers with simple TTL caching."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from ..cache import get as cache_get, set as cache_set


@dataclass
class AdapterResponse:
    """Standardized response from model adapters."""
    text: str
    model_id: str
    metadata: Dict[str, Any]


class BaseAdapter(ABC):
    """Abstract base class for all model adapters."""
    
    def __init__(self, model_id: str, **kwargs):
        self.model_id = model_id
        self.config = kwargs
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text response from the model.
        
        Args:
            prompt: Input text prompt
            **kwargs: Model-specific parameters (temperature, max_tokens, etc.)
            
        Returns:
            Generated text response
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the adapter is properly configured and available."""
        pass

    # Back-compat alias so external tools can call adapter.available()
    def available(self) -> bool:
        return self.is_available()


class AdapterRegistry:
    """Registry for managing model adapters."""
    
    def __init__(self):
        self._adapters: Dict[str, BaseAdapter] = {}
    
    def register(self, name: str, adapter: BaseAdapter) -> None:
        """Register an adapter with a given name."""
        self._adapters[name] = adapter
    
    def get(self, name: str) -> BaseAdapter:
        """Get an adapter by name."""
        if name not in self._adapters:
            raise ValueError(f"Adapter '{name}' not found")
        return self._adapters[name]
    
    def list_available(self) -> List[str]:
        """List all available adapter names."""
        return [name for name, adapter in self._adapters.items() if adapter.is_available()]

    def list(self) -> Dict[str, BaseAdapter]:
        """List all registered adapters (name → instance)."""
        return dict(self._adapters)


# Global registry instance
registry = AdapterRegistry()


def _cache_key(prompt: str, kwargs: Dict[str, Any]) -> Tuple[Any, ...]:
    """Build a cache key from prompt and selected stable params."""
    allow = {"model", "temperature", "max_tokens", "top_p"}
    filtered = {k: v for k, v in kwargs.items() if k in allow and v is not None}
    return (prompt, tuple(sorted(filtered.items())))

def generate_with_cache(adapter: BaseAdapter, prompt: str, **kwargs: Any) -> str:
    """Wrap adapter.generate with a simple TTL cache (namespace = adapter name)."""
    key = _cache_key(prompt, kwargs)
    namespace = adapter.__class__.__name__.lower()
    hit = cache_get(namespace, key)
    if hit is not None:
        return hit
    out = adapter.generate(prompt, **kwargs)
    cache_set(namespace, key, out)
    return out