"""Base adapter interface for model providers."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass


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


# Global registry instance
registry = AdapterRegistry()