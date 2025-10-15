from __future__ import annotations
import json, os, time, hashlib
from pathlib import Path
from typing import Any, Optional, Tuple

class FileCache:
    def __init__(self, root: str | Path = ".ecl_cache", ttl_hours: int = 4):
        self.root = Path(root)
        self.root.mkdir(exist_ok=True)
        self.ttl = ttl_hours * 3600

    def _key(self, **kwargs) -> str:
        h = hashlib.sha256()
        h.update(json.dumps(kwargs, sort_keys=True).encode())
        return h.hexdigest()

    def get(self, **kwargs) -> Optional[Any]:
        k = self._key(**kwargs)
        p = self.root / k
        if not p.exists():
            return None
        if time.time() - p.stat().st_mtime > self.ttl:
            try: p.unlink()
            except OSError: pass
            return None
        try:
            return json.loads(p.read_text())
        except Exception:
            return None

    def set(self, value: Any, **kwargs) -> None:
        k = self._key(**kwargs)
        p = self.root / k
        p.write_text(json.dumps(value))

# --- Module-level TTL cache helpers (for adapter caching) ---
_DEFAULT_TTL_HOURS = int(os.getenv("ECL_CACHE_TTL_HOURS", "12"))
_CACHE_DIR = Path(os.getenv("ECL_CACHE_DIR", ".ecl_cache"))
_CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _now_s() -> float:
    return time.time()

def _key_hash(parts: Tuple[Any, ...]) -> str:
    raw = json.dumps(parts, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def get(namespace: str, key_parts: Tuple[Any, ...]) -> Optional[Any]:
    ttl_s = _DEFAULT_TTL_HOURS * 3600
    key = _key_hash((namespace, *key_parts))
    f = _CACHE_DIR / f"{namespace}-{key}.json"
    if not f.exists():
        return None
    try:
        payload = json.loads(f.read_text())
        if _now_s() - payload.get("ts", 0) > ttl_s:
            try:
                f.unlink()
            finally:
                return None
        return payload.get("value")
    except Exception:
        # Corrupt cache entry; delete and miss
        try:
            f.unlink()
        finally:
            return None

def set(namespace: str, key_parts: Tuple[Any, ...], value: Any) -> None:
    key = _key_hash((namespace, *key_parts))
    f = _CACHE_DIR / f"{namespace}-{key}.json"
    f.write_text(json.dumps({"ts": _now_s(), "value": value}, ensure_ascii=False))

def stats() -> dict:
    # Lightweight metrics for smoke reports
    files = list(_CACHE_DIR.glob("*.json"))
    size = sum(f.stat().st_size for f in files) if files else 0
    return {"dir": str(_CACHE_DIR), "entries": len(files), "bytes": size}