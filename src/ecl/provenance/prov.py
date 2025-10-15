from __future__ import annotations
from dataclasses import dataclass
import hashlib, json
from typing import Dict, Any

HASH_VERSION = "prov-hash-v1"

def stable_claim_id(text: str) -> str:
    h = hashlib.sha256()
    h.update(b"ECL|claim|v1|")
    h.update(text.strip().encode("utf-8"))
    return h.hexdigest()[:16]

@dataclass
class ProvEntity:
    id: str
    attrs: Dict[str, Any]

def prov_json_for_claims(claims: list[dict]) -> dict:
    """Minimal PROV-JSON-style structure (W3C-inspired)."""
    entities = {}
    for c in claims:
        cid = c.get("id") or stable_claim_id(c.get("text",""))
        entities[cid] = {"prov:label": c.get("text",""), "ecl:support": c.get("support", [])}
        c["id"] = cid
    graph = {
        "entity": entities,
        "activity": {},
        "agent": {}
    }
    return graph