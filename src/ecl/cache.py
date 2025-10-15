from __future__ import annotations
import json, os, time, hashlib
from pathlib import Path
from typing import Any, Optional

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