import time

from src.cache import FileCache

def test_cache_hit_and_expiry(tmp_path):
    c = FileCache(root=tmp_path, ttl_hours=0.0001)  # ~0.36s
    key = dict(prompt="hello", model_id="stub", temperature=0.0)
    assert c.get(**key) is None
    c.set({"ok": True}, **key)
    assert c.get(**key) == {"ok": True}
    time.sleep(0.5)
    assert c.get(**key) is None
