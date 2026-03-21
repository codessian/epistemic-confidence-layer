from src.adapters.base import AdapterRequest, BaseAdapter, Generation, registry
from src.router import DynamicRouter, ProviderSpec, RoutePolicy, RouteRequest

class _FakeA(BaseAdapter):
    provider_kind = "fakeA"
    vendor = "A"
    arch_family = "x"

    def generate(self, req: AdapterRequest | str, **kw):
        return Generation(text="alpha", metadata={"vendor": "A", "arch_family": "x", "provider_kind": "fakeA", "model": "m"})

    def is_available(self) -> bool:
        return True

class _FakeB(BaseAdapter):
    provider_kind = "fakeB"
    vendor = "B"
    arch_family = "y"

    def generate(self, req: AdapterRequest | str, **kw):
        return Generation(text="alpha", metadata={"vendor": "B", "arch_family": "y", "provider_kind": "fakeB", "model": "m"})

    def is_available(self) -> bool:
        return True


class _Failing(BaseAdapter):
    provider_kind = "fail"

    def generate(self, req: AdapterRequest | str, **kw):
        from src.errors import AdapterError
        raise AdapterError(code="PROVIDER_ERROR", hint="boom", provider="fail", status=502)

    def is_available(self) -> bool:
        return True


def test_router_returns_route_result_with_errors_array():
    registry.register("fakeA", _FakeA("fakeA"))
    registry.register("fakeB", _FakeB("fakeB"))
    specs = [ProviderSpec(id="a", kind="fakeA", model="m"), ProviderSpec(id="b", kind="fakeB", model="m")]
    policy = RoutePolicy(name="default", select={"type": "quorum_k_of_n", "k": 2, "providers": ["a", "b"]}, constraints={"budget_usd": 0.01})
    router = DynamicRouter(specs, policy)
    result = router.generate(RouteRequest(prompt="test", contains_pii=False, timeout_s=2, request_id="req-1"))
    assert len(result.generations) >= 1
    assert 0.0 <= result.meta.diversity_score <= 1.0
    assert isinstance(result.errors, list)


def test_router_collects_partial_failures_without_fake_empty_generations():
    registry.register("ok", _FakeA("ok"))
    registry.register("fail", _Failing("fail"))
    specs = [ProviderSpec(id="ok1", kind="ok", model="m"), ProviderSpec(id="bad1", kind="fail", model="m")]
    policy = RoutePolicy(name="default", select={"type": "quorum_k_of_n", "k": 2, "providers": ["ok1", "bad1"]}, constraints={})
    router = DynamicRouter(specs, policy)
    result = router.generate(RouteRequest(prompt="test", contains_pii=False, timeout_s=2, request_id="req-2"))
    assert any(g.text == "alpha" for g in result.generations)
    assert len(result.errors) == 1
    assert result.errors[0].code == "PROVIDER_ERROR"
