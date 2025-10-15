from typing import Dict, List

def score_consensus(claims: List[Dict], models: List[str]) -> List[Dict]:
    """
    Deterministic stub: agreement scales with number of models,
    diversity fixed, other dimensions near 1.0 for demo.
    """
    k = max(1, len(models))
    out: List[Dict] = []
    for c in claims:
        out.append({
            "claim_id": c["id"],
            "agreement_score": min(0.95, 0.6 + 0.1 * k),
            "diversity_score": 0.60,
            "evidence": [],
            "recency": 1.0,
            "stability": 0.90,
            "language_integrity": 0.95,
            "ecs": 0.88  # calibrated ECS would be produced later
        })
    return out