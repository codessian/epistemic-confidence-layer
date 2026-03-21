import hashlib
from typing import Dict, List

def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def heuristic_extract(prompt: str) -> List[Dict]:
    cleaned = (prompt or "").strip()
    if not cleaned:
        return []
    claims: List[Dict] = []
    if cleaned.endswith("?"):
        texts = [cleaned]
    else:
        texts = [token.strip() for token in cleaned.split(".") if token.strip()]
    for t in texts:
        cid = f"c_{_hash(t)[:8]}"
        claims.append({
            "id": cid,
            "text": t,
            "hash": _hash(t),
            "provenance": {"source": "extraction:heuristic"}
        })
    return claims
