from typing import Dict

def minimal_prov(entity_hash: str) -> Dict:
    return {
        "entity": {"id": f"e:{entity_hash}"},
        "activity": {"id": "act:extraction:heuristic"},
        "agent": {"id": "agent:ecl:stub"},
    }