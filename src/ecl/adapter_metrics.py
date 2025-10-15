from __future__ import annotations
from typing import Any, Dict, List, Optional

_EVENTS: List[Dict[str, Any]] = []

def record_adapter_event(name: str, elapsed_ms: float, retries: int, status: str, cache_hit: bool = False, code: Optional[str] = None) -> None:
    _EVENTS.append({
        "name": name,
        "elapsed_ms": float(elapsed_ms),
        "retries": int(retries),
        "status": status,
        "cache_hit": bool(cache_hit),
        "code": code,
    })

def get_events() -> List[Dict[str, Any]]:
    return list(_EVENTS)

def reset_events() -> None:
    _EVENTS.clear()

def timing_summary() -> Dict[str, Any]:
    by_name: Dict[str, Dict[str, Any]] = {}
    for e in _EVENTS:
        n = e["name"]
        t = by_name.setdefault(n, {"calls": 0, "last_ms": 0.0, "retries_total": 0, "cache_hits": 0})
        t["calls"] += 1
        t["last_ms"] = e["elapsed_ms"]
        t["retries_total"] += e["retries"]
        if e.get("cache_hit"):
            t["cache_hits"] += 1
    return by_name