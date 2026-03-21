from src.cache import FileCache


def test_cache_key_path_and_namespaced_set_get(tmp_path):
    cache = FileCache(root=tmp_path, ttl_hours=1)
    cache.set({"value": 1}, namespace="ns", key=("a", 1))
    assert cache.get(namespace="ns", key=("a", 1)) == {"value": 1}


def test_cache_corrupt_payload_returns_none(tmp_path):
    cache = FileCache(root=tmp_path, ttl_hours=1)
    key = cache._key(namespace="ns", key=("bad",))
    path = tmp_path / key
    path.write_text("{bad-json", encoding="utf-8")
    assert cache.get(namespace="ns", key=("bad",)) is None
