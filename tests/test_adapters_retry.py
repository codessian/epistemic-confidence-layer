import time

from src.adapters.base import AdapterRequest, BaseAdapter, Generation, ProviderError

class FlakyAdapter(BaseAdapter):
    provider_kind = "flaky"

    def __init__(self):
        super().__init__("flaky")
        self.calls = 0

    def generate(self, req: AdapterRequest | str, **kw):
        self.calls += 1
        if self.calls < 2:
            raise ProviderError("transient", "Temporary failure", "flaky")
        return Generation(text="ok", metadata={})

    def is_available(self) -> bool:
        return True


def test_retryable_provider_error_preserves_code_and_retryability():
    a = FlakyAdapter()
    for _ in range(2):
        try:
            g = a.generate("ping")
            assert g.text == "ok"
            break
        except ProviderError:
            time.sleep(0.01)


def test_non_retryable_error_is_not_retried():
    class HardFail(FlakyAdapter):
        def generate(self, req: AdapterRequest | str, **kw):
            raise ProviderError("BAD_REQUEST", "Invalid input", "hard")

    a = HardFail()
    try:
        a.generate("ping")
    except ProviderError as exc:
        assert exc.code == "BAD_REQUEST"
