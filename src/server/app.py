from __future__ import annotations

import logging
import time
import uuid
from collections import defaultdict, deque
from threading import Lock
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..adapters.anthropic import AnthropicAdapter
from ..adapters.base import registry
from ..adapters.gemini import GeminiAdapter
from ..adapters.google import GoogleAdapter
from ..adapters.hf import HFInferenceAdapter
from ..adapters.ollama import OllamaAdapter
from ..adapters.openai import OpenAIAdapter
from ..adapters.openrouter import OpenRouterAdapter
from ..adapters.vertex import VertexAIAdapter
from ..calibration.isotonic import IsotonicCalibrator
from ..config import ConfigError, load_policy, load_settings, validate_runtime
from ..consensus.score import score_consensus
from ..errors import AdapterError, error_envelope_from_exception
from ..provenance.prov import HASH_VERSION, prov_from_generations
from ..router import DynamicRouter, ProviderSpec, RoutePolicy, RouteRequest

logger = logging.getLogger("ecl.server")
app = FastAPI(title="ECL API", version="1.2.0")


class VerifyRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000)
    contains_pii: bool
    timeout_s: float | None = None
    request_id: str | None = None


class Claim(BaseModel):
    text: str


class Timing(BaseModel):
    total: int


class ProviderErrorModel(BaseModel):
    provider_id: str
    provider_kind: str
    model: str
    code: str
    message: str
    retryable: bool
    retry_after_ms: int | None = None


class Consensus(BaseModel):
    score: float
    details: dict[str, Any]
    models: list[str | None]


class VerifyResponse(BaseModel):
    x_schema_version: str
    request_id: str
    route_id: str | None = None
    ecs: float
    claims: list[Claim]
    consensus: Consensus
    provenance: dict[str, Any]
    errors: list[ProviderErrorModel]
    timing_ms: Timing


_REQUEST_WINDOWS: dict[str, deque[float]] = defaultdict(deque)
_RATE_LOCK = Lock()


def _register_default_adapters() -> None:
    adapters = {
        "openai": OpenAIAdapter(),
        "anthropic": AnthropicAdapter(),
        "google": GoogleAdapter(),
        "gemini": GeminiAdapter("gemini-1.5-flash"),
        "hf": HFInferenceAdapter("repo-id"),
        "vertex": VertexAIAdapter("gemini-1.5-flash"),
        "ollama": OllamaAdapter("llama3.1"),
        "openrouter": OpenRouterAdapter("default"),
    }
    for name, adapter in adapters.items():
        registry.register(name, adapter)


def _startup_state() -> None:
    _register_default_adapters()
    settings = load_settings()
    policy = load_policy(settings.policy_file)
    validate_runtime(settings, policy, registry)
    app.state.settings = settings
    app.state.policy = policy
    logger.info("startup validation complete")


_register_default_adapters()


@app.on_event("startup")
def startup_event() -> None:
    _startup_state()


@app.exception_handler(AdapterError)
async def adapter_error_handler(request: Request, exc: AdapterError):
    request_id = getattr(request.state, "request_id", None)
    payload = error_envelope_from_exception(exc, request_id)
    return JSONResponse(status_code=payload["error"]["status"], content=payload)


@app.exception_handler(ConfigError)
async def config_error_handler(request: Request, exc: ConfigError):
    payload = {
        "error": {
            "code": "CONFIG_ERROR",
            "message": str(exc),
            "status": 500,
            "hint": None,
            "request_id": getattr(request.state, "request_id", None),
            "retry_after_ms": None,
        }
    }
    return JSONResponse(status_code=500, content=payload)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request.state.request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    path = request.url.path
    if path in {"/livez", "/readyz", "/health"}:
        return await call_next(request)
    settings = getattr(app.state, "settings", None) or load_settings()
    if settings.auth.auth_mode == "apikey":
        key = request.headers.get("X-API-Key")
        if not key:
            payload = error_envelope_from_exception(
                AdapterError(code="UNAUTHORIZED", hint="Missing API key", provider="server", status=401),
                getattr(request.state, "request_id", None),
            )
            return JSONResponse(status_code=401, content=payload)
        if key not in settings.auth.api_keys:
            payload = error_envelope_from_exception(
                AdapterError(code="FORBIDDEN", hint="Invalid API key", provider="server", status=403),
                getattr(request.state, "request_id", None),
            )
            return JSONResponse(status_code=403, content=payload)
    return await call_next(request)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    path = request.url.path
    if path in {"/livez", "/readyz", "/health"}:
        return await call_next(request)
    settings = getattr(app.state, "settings", None) or load_settings()
    strategy = settings.rate_limit.key_strategy
    if strategy == "api_key":
        key = request.headers.get("X-API-Key") or "anonymous"
    else:
        key = request.client.host if request.client else "unknown"
    now = time.time()
    with _RATE_LOCK:
        window = _REQUEST_WINDOWS[key]
        while window and now - window[0] > 60:
            window.popleft()
        if len(window) >= settings.rate_limit.rpm:
            payload = error_envelope_from_exception(
                AdapterError(
                    code="RATE_LIMITED",
                    hint="Rate limit exceeded; respect Retry-After.",
                    provider="server",
                    status=429,
                    retry_after_ms=1000,
                ),
                getattr(request.state, "request_id", None),
            )
            return JSONResponse(status_code=429, content=payload)
        window.append(now)
    return await call_next(request)


@app.get("/livez")
def livez():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    try:
        settings = getattr(app.state, "settings", None)
        policy = getattr(app.state, "policy", None)
        if settings is None or policy is None:
            _startup_state()
            settings = app.state.settings
            policy = app.state.policy
        validate_runtime(settings, policy, registry)
        return {"status": "ready", "registered_adapters": sorted(registry.list().keys())}
    except Exception as exc:
        return JSONResponse(status_code=503, content={"status": "not_ready", "detail": str(exc)})


@app.get("/health")
def health():
    return livez()


@app.post("/verify", response_model=VerifyResponse)
def verify(req: VerifyRequest, request: Request):
    t0 = time.time()
    settings = getattr(app.state, "settings", None) or load_settings()
    policy_data = getattr(app.state, "policy", None) or load_policy(settings.policy_file)

    provider_specs = [ProviderSpec(**provider.model_dump()) for provider in policy_data.providers]
    strategy = policy_data.strategies[0]
    policy = RoutePolicy(name=strategy.name, select=strategy.select.model_dump(), constraints=strategy.constraints)
    router = DynamicRouter(provider_specs, policy, registry=registry)

    request_id = req.request_id or getattr(request.state, "request_id", None) or str(uuid.uuid4())
    timeout_s = min(req.timeout_s or settings.default_timeout_s, settings.max_timeout_s)
    route_req = RouteRequest(prompt=req.prompt, contains_pii=req.contains_pii, timeout_s=timeout_s, request_id=request_id)
    route_result = router.generate(route_req)

    texts = [generation.text for generation in route_result.generations if generation.text]
    cscore, cdetail = score_consensus(texts, router_meta=route_result.meta.__dict__)
    ecs = IsotonicCalibrator().fit([cscore, 0.4, 0.8], [1, 0, 1]).predict([cscore])[0]
    provenance = prov_from_generations(route_result.generations, route_meta=route_result.meta.__dict__)

    logger.info(
        "verify completed",
        extra={"request_id": request_id, "route_id": route_result.meta.route_id, "errors": len(route_result.errors)},
    )
    return VerifyResponse(
        x_schema_version="1.2",
        request_id=request_id,
        route_id=route_result.meta.route_id,
        ecs=float(ecs),
        claims=[Claim(text=text) for text in texts[:3]],
        consensus=Consensus(
            score=cscore,
            details=cdetail,
            models=[generation.metadata.get("model") for generation in route_result.generations],
        ),
        provenance={"prov_json": provenance, "hash_version": HASH_VERSION},
        errors=[ProviderErrorModel(**error.__dict__) for error in route_result.errors],
        timing_ms=Timing(total=int((time.time() - t0) * 1000)),
    )
