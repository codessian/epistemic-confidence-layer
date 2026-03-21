from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Any


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


def _extract_retry_after_ms(exc: Exception) -> Optional[int]:
    # Common locations: exc.retry_after_ms, exc.retry_after, exc.response.headers['Retry-After']
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
                # Header may be seconds
                val = int(float(hdr))
                return val * 1000
        except Exception:
            pass
    return None


def normalize_error(provider: str, exc: Exception) -> AdapterError:
    # Attempt to map well-known SDK exceptions without importing them directly
    name = exc.__class__.__name__.lower()
    status = getattr(exc, "status", None) or getattr(exc, "status_code", None)
    retry_after_ms = _extract_retry_after_ms(exc)

    if isinstance(exc, TimeoutError) or "timeout" in name:
        return AdapterError(code="PROVIDER_TIMEOUT", hint="The provider API call exceeded timeout.", provider=provider, status=status, retry_after_ms=retry_after_ms, cause=exc)

    # Rate limit detection
    if "ratelimit" in name or "rate_limit" in name:
        return AdapterError(code="RATE_LIMITED", hint="Rate limit exceeded; respect Retry-After.", provider=provider, status=status, retry_after_ms=retry_after_ms, cause=exc)

    # Network/API connection
    if "connection" in name or "network" in name:
        return AdapterError(code="NETWORK_ERROR", hint="Network/connectivity issue calling provider.", provider=provider, status=status, retry_after_ms=retry_after_ms, cause=exc)

    # Generic API error; use status if available to split
    if status is not None:
        try:
            s = int(status)
        except Exception:
            s = None
        if s is not None and s >= 500:
            return AdapterError(code="PROVIDER_ERROR", hint="Provider internal error (5xx).", provider=provider, status=s, retry_after_ms=retry_after_ms, cause=exc)
        if s is not None and s == 429:
            return AdapterError(code="RATE_LIMITED", hint="Rate limit exceeded; respect Retry-After.", provider=provider, status=s, retry_after_ms=retry_after_ms, cause=exc)
        if s is not None and 400 <= s < 500:
            return AdapterError(code="BAD_REQUEST", hint="Invalid request to provider (4xx).", provider=provider, status=s, retry_after_ms=retry_after_ms, cause=exc)

    # Fallback: treat unknown as provider error (transient)
    return AdapterError(code="PROVIDER_ERROR", hint="Provider error.", provider=provider, status=status, retry_after_ms=retry_after_ms, cause=exc)