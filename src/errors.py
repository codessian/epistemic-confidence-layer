from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class AdapterError(Exception):
    code: str
    hint: str
    provider: str
    status: Optional[int] = None
    retry_after_ms: Optional[int] = None
    cause: Optional[Exception] = None

    def __str__(self) -> str:
        base = f"[{self.provider}] {self.code}: {self.hint}"
        if self.status is not None:
            base += f" (status={self.status})"
        if self.retry_after_ms is not None:
            base += f" (retry_after_ms={self.retry_after_ms})"
        return base


@dataclass
class ErrorEnvelope:
    code: str
    message: str
    status: int
    hint: str | None = None
    request_id: str | None = None
    retry_after_ms: int | None = None

    def as_dict(self) -> dict:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "status": self.status,
                "hint": self.hint,
                "request_id": self.request_id,
                "retry_after_ms": self.retry_after_ms,
            }
        }


def _extract_retry_after_ms(exc: Exception) -> Optional[int]:
    ra = getattr(exc, "retry_after_ms", None)
    if isinstance(ra, (int, float)):
        return int(ra)
    ra_s = getattr(exc, "retry_after", None)
    if isinstance(ra_s, (int, float)):
        return int(ra_s * 1000)
    resp = getattr(exc, "response", None)
    if resp is not None:
        try:
            hdr = resp.headers.get("Retry-After") or resp.headers.get("retry-after")
            if hdr:
                return int(float(hdr) * 1000)
        except Exception:
            pass
    return None


def normalize_error(provider: str, exc: Exception) -> AdapterError:
    name = exc.__class__.__name__.lower()
    status = getattr(exc, "status", None) or getattr(exc, "status_code", None)
    retry_after_ms = _extract_retry_after_ms(exc)

    if isinstance(exc, TimeoutError) or "timeout" in name:
        return AdapterError(
            code="PROVIDER_TIMEOUT",
            hint="The provider API call exceeded timeout.",
            provider=provider,
            status=status,
            retry_after_ms=retry_after_ms,
            cause=exc,
        )
    if "ratelimit" in name or "rate_limit" in name:
        return AdapterError(
            code="RATE_LIMITED",
            hint="Rate limit exceeded; respect Retry-After.",
            provider=provider,
            status=status,
            retry_after_ms=retry_after_ms,
            cause=exc,
        )
    if "connection" in name or "network" in name:
        return AdapterError(
            code="NETWORK_ERROR",
            hint="Network/connectivity issue calling provider.",
            provider=provider,
            status=status,
            retry_after_ms=retry_after_ms,
            cause=exc,
        )
    if status is not None:
        try:
            parsed_status = int(status)
        except Exception:
            parsed_status = None
        if parsed_status is not None and parsed_status >= 500:
            return AdapterError(
                code="PROVIDER_ERROR",
                hint="Provider internal error (5xx).",
                provider=provider,
                status=parsed_status,
                retry_after_ms=retry_after_ms,
                cause=exc,
            )
        if parsed_status == 429:
            return AdapterError(
                code="RATE_LIMITED",
                hint="Rate limit exceeded; respect Retry-After.",
                provider=provider,
                status=parsed_status,
                retry_after_ms=retry_after_ms,
                cause=exc,
            )
        if parsed_status is not None and 400 <= parsed_status < 500:
            return AdapterError(
                code="BAD_REQUEST",
                hint="Invalid request to provider (4xx).",
                provider=provider,
                status=parsed_status,
                retry_after_ms=retry_after_ms,
                cause=exc,
            )
    return AdapterError(
        code="PROVIDER_ERROR",
        hint="Provider error.",
        provider=provider,
        status=status,
        retry_after_ms=retry_after_ms,
        cause=exc,
    )


def to_generation_error(err: AdapterError, provider_id: str, provider_kind: str, model: str):
    from .adapters.base import GenerationError

    return GenerationError(
        provider_id=provider_id,
        provider_kind=provider_kind,
        model=model,
        code=err.code,
        message=str(err),
        retryable=err.code in {"PROVIDER_TIMEOUT", "RATE_LIMITED", "NETWORK_ERROR", "PROVIDER_ERROR"},
        retry_after_ms=err.retry_after_ms,
    )


def error_envelope_from_exception(exc: AdapterError, request_id: str | None = None) -> dict:
    code_to_status = {
        "PROVIDER_TIMEOUT": 504,
        "RATE_LIMITED": 429,
        "NETWORK_ERROR": 503,
        "BAD_REQUEST": 400,
        "PROVIDER_ERROR": 502,
        "ADAPTER_UNAVAILABLE": 503,
        "UNAUTHORIZED": 401,
        "FORBIDDEN": 403,
    }
    status = exc.status if exc.status is not None else code_to_status.get(exc.code, 502)
    return ErrorEnvelope(
        code=exc.code,
        message=str(exc),
        status=status,
        hint=exc.hint,
        request_id=request_id,
        retry_after_ms=exc.retry_after_ms,
    ).as_dict()
