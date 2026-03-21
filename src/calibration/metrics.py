from typing import List

def brier_score(probs: List[float], labels: List[int]) -> float:
    assert len(probs) == len(labels)
    return sum((p - y) ** 2 for p, y in zip(probs, labels)) / len(probs)

def ece(probs: List[float], labels: List[int], bins: int = 10) -> float:
    """Simple ECE for toy evaluation."""
    assert len(probs) == len(labels)
    bucket: List[List[tuple[float, int]]] = [[] for _ in range(bins)]
    for p, y in zip(probs, labels):
        i = min(bins - 1, int(p * bins))
        bucket[i].append((p, y))
    total = 0.0
    n = len(probs)
    for b in bucket:
        if not b:
            continue
        acc = sum(y for _, y in b) / len(b)
        conf = sum(p for p, _ in b) / len(b)
        total += (len(b) / n) * abs(acc - conf)
    return total