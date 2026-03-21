from typing import List

def brier_score(probs: List[float], labels: List[int]) -> float:
    if len(probs) != len(labels):
        raise ValueError("probs and labels must have same length")
    if not probs:
        raise ValueError("probs must be non-empty")
    return sum((p - y) ** 2 for p, y in zip(probs, labels)) / len(probs)

def ece(probs: List[float], labels: List[int], bins: int = 10) -> float:
    if len(probs) != len(labels):
        raise ValueError("probs and labels must have same length")
    if bins < 1:
        raise ValueError("bins must be >= 1")
    if not probs:
        return 0.0
    bucket: List[List[tuple[float, int]]] = [[] for _ in range(bins)]
    for p, y in zip(probs, labels):
        if p < 0 or p > 1:
            raise ValueError("probabilities must be within [0,1]")
        if y not in (0, 1):
            raise ValueError("labels must be 0 or 1")
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
