from src.adapter_metrics import get_events, record_adapter_event, reset_events, timing_summary


def test_adapter_metrics_record_and_summary():
    reset_events()
    record_adapter_event("openai", 10.0, retries=1, status="ok", cache_hit=False)
    record_adapter_event("openai", 5.0, retries=0, status="ok", cache_hit=True)
    record_adapter_event("anthropic", 15.0, retries=2, status="error", cache_hit=False, code="PROVIDER_ERROR")
    events = get_events()
    assert len(events) == 3
    summary = timing_summary()
    assert summary["openai"]["calls"] == 2
    assert summary["openai"]["cache_hits"] == 1
    assert summary["anthropic"]["retries_total"] == 2
