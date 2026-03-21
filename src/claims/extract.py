import hashlib
import uuid
from typing import Dict, List

def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def heuristic_extract(prompt: str) -> List[Dict]:
    """
    Deterministic stub: treat the whole prompt as one claim if it ends with '?'
    Otherwise, split by '.' and keep non-empty sentences as claims.
    """
    claims: List[Dict] = []
    texts: List[str] = []
    if prompt.strip().endswith("?"):
        texts = [prompt.strip()]
    else:
        texts = [t.strip() for t in prompt.split(".") if t.strip()]
    for t in texts:
        cid = f"c_{uuid.uuid4().hex[:8]}"
        claims.append({
            "id": cid,
            "text": t,
            "hash": _hash(t),
            "provenance": {"source": "extraction:heuristic"}
        })
    return claims