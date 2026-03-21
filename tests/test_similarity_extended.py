import numpy as np

from src.similarity import EmbeddingBackend, classify_similarity, cosine_sim


def test_cosine_zero_vector_guard():
    a = np.array([0.0, 0.0], dtype=np.float32)
    b = np.array([1.0, 0.0], dtype=np.float32)
    assert cosine_sim(a, b) == 0.0


def test_similarity_stub_backend_produces_shape():
    backend = EmbeddingBackend()
    backend.backend = "stub"
    emb = backend.embed(["abc", "def"])
    assert emb.shape[0] == 2
    assert emb.shape[1] > 1


def test_similarity_classify_bounds():
    label, score = classify_similarity("same", "same")
    assert label in {"same", "overlap", "drift"}
    assert -1.0 <= score <= 1.0
