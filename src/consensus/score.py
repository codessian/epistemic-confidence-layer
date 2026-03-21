from typing import Dict, List, Optional

def score_consensus(model_texts, router_meta=None):
    """
    Consensus scorer with diversity weighting (if router metadata present).
    """
    if not model_texts:
        return 0.0, {"pairs": 0}
    base = 1.0 if len(set(model_texts)) == 1 else (0.5 if len(model_texts) > 1 else 0.0)
    details = {"pairs": len(model_texts)}
    if router_meta:
        # Nudge score up/down by diversity (bounded)
        div = float(router_meta.get("diversity_score", 0.0))
        base = max(0.0, min(1.0, 0.8*base + 0.2*div))
        details["diversity_score"] = div
    return base, details

def score_consensus_legacy(claims: List[Dict], models: List[str]) -> List[Dict]:
    """
    Legacy deterministic stub: agreement scales with number of models,
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