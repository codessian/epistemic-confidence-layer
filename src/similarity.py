from __future__ import annotations

import os
from typing import Iterable, Tuple

import numpy as np

_BACKEND = os.getenv("ECL_EMBED_BACKEND", "sentence-transformers").lower()

class EmbeddingBackend:
    def __init__(self) -> None:
        self.backend = _BACKEND
        self._model = None
        self._client = None
        self._embed_model = None
        if self.backend == "sentence-transformers":
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore
            except Exception:
                self.backend = "stub"
                return
            model_name = os.getenv("ECL_ST_MODEL", "all-MiniLM-L6-v2")
            self._model = SentenceTransformer(model_name)
        elif self.backend == "openai":
            try:
                from openai import OpenAI  # type: ignore
            except Exception as e:  # pragma: no cover
                raise RuntimeError("openai SDK not installed") from e
            api_key = os.getenv("OPENAI_API_KEY")
            self._client = OpenAI(api_key=api_key)
            self._embed_model = os.getenv("ECL_OPENAI_EMBED_MODEL", "text-embedding-3-small")
        else:
            pass

    def embed(self, texts: Iterable[str]) -> np.ndarray:
        text_list = list(texts)
        if self.backend == "sentence-transformers" and self._model is not None:
            encoded = self._model.encode(text_list, normalize_embeddings=True)
            return np.asarray(encoded, dtype=np.float32)
        if self.backend == "openai" and self._client is not None and self._embed_model:
            resp = self._client.embeddings.create(model=self._embed_model, input=text_list)
            vectors = [np.asarray(item.embedding, dtype=np.float32) for item in resp.data]
            normalized = [vector / np.linalg.norm(vector) if np.linalg.norm(vector) > 0 else vector for vector in vectors]
            return np.vstack(normalized)
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789 "
        fallback_vectors: list[np.ndarray] = []
        for text in text_list:
            lowered = text.lower()
            vector = np.asarray([lowered.count(ch) for ch in alphabet], dtype=np.float32)
            norm = np.linalg.norm(vector)
            if norm > 0:
                vector = vector / norm
            fallback_vectors.append(vector)
        return np.vstack(fallback_vectors)


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def classify_pair(
    a: str,
    b: str,
    backend: EmbeddingBackend | None = None,
    eq_thresh: float = 0.95,
    rel_bounds: Tuple[float, float] = (0.85, 0.95),
) -> Tuple[str, float]:
    """
    Returns (label, similarity) with labels:
      - "equivalent" if sim >= eq_thresh
      - "related" if rel_bounds[0] <= sim < rel_bounds[1]
      - "different" otherwise
    """
    be = backend or EmbeddingBackend()
    v = be.embed([a, b])
    sim = cosine_sim(v[0], v[1])
    if sim >= eq_thresh:
        return "equivalent", sim
    if rel_bounds[0] <= sim < rel_bounds[1]:
        return "related", sim
    return "different", sim


# Backward-compat wrapper used elsewhere in the repo
def classify_similarity(a: str, b: str, backend: EmbeddingBackend | None = None) -> Tuple[str, float]:
    return classify_pair(a, b, backend=backend)
