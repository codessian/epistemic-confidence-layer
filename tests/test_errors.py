import pytest

from src.errors import AdapterError, error_envelope_from_exception, normalize_error, to_generation_error


def test_normalize_error_timeout():
    err = normalize_error("openai", TimeoutError("timed out"))
    assert err.code == "PROVIDER_TIMEOUT"


def test_normalize_error_rate_limit_from_name():
    class RateLimitFailure(Exception):
        pass

    err = normalize_error("openai", RateLimitFailure("rate"))
    assert err.code == "RATE_LIMITED"


def test_normalize_error_with_status_code():
    class HttpError(Exception):
        status_code = 400

    err = normalize_error("openai", HttpError("bad"))
    assert err.code == "BAD_REQUEST"


def test_error_envelope_mapping_and_generation_error():
    exc = AdapterError(code="RATE_LIMITED", hint="slow down", provider="openai", retry_after_ms=250)
    payload = error_envelope_from_exception(exc, request_id="req-1")
    assert payload["error"]["status"] == 429
    gen = to_generation_error(exc, provider_id="openai:gpt-4o", provider_kind="openai", model="gpt-4o")
    assert gen.retryable is True
    assert gen.code == "RATE_LIMITED"
