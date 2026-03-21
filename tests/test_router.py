from src.ecl.router import DynamicRouter, ProviderSpec, RoutePolicy
from src.ecl.adapters.base import Generation, registry, BaseAdapter

class _FakeA(BaseAdapter):
    name = "fakeA"
    def generate(self, prompt:str, **kw):
        return Generation(text="alpha", metadata={"vendor":"A","arch_family":"x"})
    def is_available(self) -> bool:
        return True
        
class _FakeB(BaseAdapter):
    name = "fakeB"
    def generate(self, prompt:str, **kw):
        return Generation(text="alpha", metadata={"vendor":"B","arch_family":"y"})
    def is_available(self) -> bool:
        return True

def test_router_diversity_weights(tmp_path, monkeypatch):
    reg = registry
    reg.register("fakeA", _FakeA("fakeA"))
    reg.register("fakeB", _FakeB("fakeB"))
    specs = [ProviderSpec(id="a", kind="fakeA", model="m"), ProviderSpec(id="b", kind="fakeB", model="m")]
    policy = RoutePolicy(name="default", select={"type":"quorum_k_of_n","k":2,"providers":["a","b"]}, constraints={"budget_usd":0.01})
    router = DynamicRouter(specs, policy)
    gens, meta = router.generate("test")
    assert len(gens) >= 1
    assert 0.0 <= meta["diversity_score"] <= 1.0