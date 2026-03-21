import time
from types import SimpleNamespace
from src.ecl.adapters.base import BaseAdapter, Generation, ProviderError

class FlakyAdapter(BaseAdapter):
    name = "flaky"
    def __init__(self):
        super().__init__("flaky")
        self.calls = 0
    def generate(self, prompt:str, **kw):
        self.calls += 1
        if self.calls < 2:
            raise ProviderError("transient", "Temporary failure", "flaky")
        return Generation(text="ok", metadata={})
    def is_available(self) -> bool:
        return True

def test_retry_like_backoff():
    a = FlakyAdapter()
    # emulate simple backoff loop here (router would wrap in future)
    for i in range(2):
        try:
            g = a.generate("ping")
            assert g.text == "ok"
            break
        except ProviderError:
            time.sleep(0.01)