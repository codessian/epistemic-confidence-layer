from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, ValidationError

from .adapters.base import AdapterRegistry


class AuthSettings(BaseModel):
    auth_mode: Literal["off", "apikey"] = "off"
    api_keys: list[str] = Field(default_factory=list)


class RateLimitSettings(BaseModel):
    rpm: int = 60
    burst: int = 10
    key_strategy: Literal["ip", "api_key"] = "ip"


class AppSettings(BaseModel):
    policy_file: str = "policies/providers.yml"
    default_timeout_s: float = 8.0
    max_timeout_s: float = 60.0
    max_prompt_length: int = 10000
    cache_ttl_hours: int = 4
    auth: AuthSettings = Field(default_factory=AuthSettings)
    rate_limit: RateLimitSettings = Field(default_factory=RateLimitSettings)


class ProviderSpecModel(BaseModel):
    id: str
    kind: str
    model: str
    allow_pii: bool = False
    region: str | None = None
    max_tps: float | None = None


class StrategySelect(BaseModel):
    type: str
    k: int = 2
    providers: list[str] = Field(default_factory=list)


class StrategyModel(BaseModel):
    name: str
    select: StrategySelect
    constraints: dict = Field(default_factory=dict)


class ProviderPolicy(BaseModel):
    providers: list[ProviderSpecModel]
    strategies: list[StrategyModel]


class ConfigError(RuntimeError):
    pass


def load_settings() -> AppSettings:
    api_keys = [k.strip() for k in os.getenv("ECL_API_KEYS", "").split(",") if k.strip()]
    auth_mode = os.getenv("ECL_AUTH_MODE", "off")
    if auth_mode not in {"off", "apikey"}:
        auth_mode = "off"
    key_strategy = os.getenv("ECL_RATE_LIMIT_KEY_STRATEGY", "ip")
    if key_strategy not in {"ip", "api_key"}:
        key_strategy = "ip"
    return AppSettings(
        policy_file=os.getenv("ECL_POLICY_FILE", "policies/providers.yml"),
        default_timeout_s=float(os.getenv("ECL_DEFAULT_TIMEOUT_S", "8.0")),
        max_timeout_s=float(os.getenv("ECL_MAX_TIMEOUT_S", "60.0")),
        max_prompt_length=int(os.getenv("ECL_MAX_PROMPT_LENGTH", "10000")),
        cache_ttl_hours=int(os.getenv("ECL_CACHE_TTL_HOURS", "4")),
        auth=AuthSettings(
            auth_mode=auth_mode,
            api_keys=api_keys,
        ),
        rate_limit=RateLimitSettings(
            rpm=int(os.getenv("ECL_RATE_LIMIT_RPM", "60")),
            burst=int(os.getenv("ECL_RATE_LIMIT_BURST", "10")),
            key_strategy=key_strategy,
        ),
    )


def load_policy(path: str) -> ProviderPolicy:
    try:
        with open(path, "r", encoding="utf-8") as file:
            raw = yaml.safe_load(file) or {}
    except FileNotFoundError as exc:
        raise ConfigError(f"Policy file not found: {path}") from exc
    try:
        return ProviderPolicy.model_validate(raw)
    except ValidationError as exc:
        raise ConfigError(f"Invalid provider policy: {exc}") from exc


def validate_runtime(settings: AppSettings, policy: ProviderPolicy, registry: AdapterRegistry) -> None:
    provider_ids = {provider.id for provider in policy.providers}
    if len(provider_ids) != len(policy.providers):
        raise ConfigError("Duplicate provider IDs found in policy file")

    registered = registry.list()
    missing_kinds = sorted({provider.kind for provider in policy.providers if provider.kind not in registered})
    if missing_kinds:
        raise ConfigError(f"Provider kinds missing from registry: {', '.join(missing_kinds)}")

    for strategy in policy.strategies:
        unknown = [provider_id for provider_id in strategy.select.providers if provider_id not in provider_ids]
        if unknown:
            raise ConfigError(f"Strategy '{strategy.name}' references unknown providers: {', '.join(unknown)}")
        if strategy.select.k < 1:
            raise ConfigError(f"Strategy '{strategy.name}' has invalid quorum k={strategy.select.k}")

    if settings.default_timeout_s <= 0 or settings.max_timeout_s <= 0:
        raise ConfigError("Timeout settings must be positive")
    if settings.default_timeout_s > settings.max_timeout_s:
        raise ConfigError("Default timeout cannot exceed max timeout")


def resolve_policy_path(path: str) -> str:
    return str(Path(path).resolve())
