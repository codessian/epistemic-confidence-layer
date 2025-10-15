from __future__ import annotations
from dataclasses import dataclass
import hashlib
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
    entities: Dict[str, Dict[str, Any]] = {}
    for c in claims:
        cid = c.get("id") or stable_claim_id(c.get("text", ""))
        entities[cid] = {"prov:label": c.get("text", ""), "ecl:support": c.get("support", [])}
        c["id"] = cid
    graph = {
        "entity": entities,
        "activity": {},
        "agent": {},
    }
    return graph

def prov_json_for(claims: list[dict]) -> dict:
    """Richer PROV-JSON including an activity and associated agent."""
    entities: Dict[str, Dict[str, Any]] = {}
    activity_id = "activity:verify"
    agents = [{"id": "agent:ecl", "prov:label": "ECL Server"}]
    was_generated_by: list[dict] = []

    for c in claims:
        cid = c.get("id") or stable_claim_id(c.get("text", ""))
        c["id"] = cid
        entities[cid] = {
            "prov:label": c.get("text", ""),
            "ecl:support": c.get("support", []),
        }
        was_generated_by.append({"entity": cid, "activity": activity_id})

    prov = {
        "entity": entities,
        "activity": {activity_id: {"prov:label": "verify"}},
        "agent": {ag["id"]: {"prov:label": ag.get("prov:label", "agent")} for ag in agents},
        "wasGeneratedBy": was_generated_by,
        "wasAssociatedWith": [{"activity": activity_id, "agent": ag["id"]} for ag in agents],
        "hash_version": HASH_VERSION,
    }
    return prov