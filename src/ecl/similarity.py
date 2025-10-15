from __future__ import annotations
from typing import Tuple

# Skeleton embedding-based similarity module.
# Real impl can use sentence-transformers or OpenAI embeddings via env flag.

class SimilarityBackend:
    def __init__(self, backend: str = "stub"):
        self.backend = backend
        # TODO: wire sentence-transformers (all-MiniLM-L6-v2) or OpenAI as option

    def embed(self, text: str) -> list[float]:
        # deterministic stub so CI remains hermetic
        return [hash(text) % 997 / 997.0]

    def cosine(self, v1: list[float], v2: list[float]) -> float:
        # 1D stub cosine
        a, b = v1[0], v2[0]
        if a == 0 and b == 0:
            return 1.0
        return min(1.0, max(0.0, 1.0 - abs(a - b)))

def classify_similarity(a: str, b: str, backend: SimilarityBackend | None = None) -> Tuple[str, float]:
    """Return ('equivalent'|'related'|'different', score[0..1])."""
    backend = backend or SimilarityBackend()
    s = backend.cosine(backend.embed(a), backend.embed(b))
    if s > 0.95:
        return "equivalent", s
    if s >= 0.85:
        return "related", s
    return "different", s