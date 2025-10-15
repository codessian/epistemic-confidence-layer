from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
import json, time
from pathlib import Path
from ..provenance.prov import prov_json_for_claims, HASH_VERSION
from ..similarity import classify_similarity
from ..calibration.isotonic import IsotonicCalibrator
from ..cache import FileCache
from ..errors import AdapterError

app = FastAPI(title="ECL API")


# Standardized error payloads for adapter errors
@app.exception_handler(AdapterError)
async def adapter_error_handler(request: Request, exc: AdapterError):
    code_to_status = {
        "PROVIDER_TIMEOUT": 504,
        "RATE_LIMITED": 429,
        "NETWORK_ERROR": 503,
        "BAD_REQUEST": 400,
        "PROVIDER_ERROR": 502,
    }
    status = exc.status if exc.status is not None else code_to_status.get(exc.code, 502)
    payload = {
        "error": {
            "code": exc.code,
            "message": str(exc),
            "hint": exc.hint,
            "provider": exc.provider,
            "status": status,
            "retry_after_ms": exc.retry_after_ms,
        }
    }
    return JSONResponse(status_code=status, content=payload)

@app.get("/health")
def health():
    # minimal metrics placeholder (extend later)
    return {"status": "ok", "cache": {"enabled": True}}

@app.post("/verify")
def verify():
    t0 = time.time()
    # minimal deterministic vertical slice response
    claims = [{"text": "httpOnly cookies mitigate XSS token theft"}]
    prov = prov_json_for_claims(claims)
    # fake consensus using similarity (placeholder)
    _, sim = classify_similarity("A", "A")
    consensus = {"models": ["stub:gpt", "stub:claude"], "score": sim, "details": [{"model":"stub:gpt"}, {"model":"stub:claude"}]}
    ecs_raw = 0.62
    ecs = IsotonicCalibrator().fit([ecs_raw, 0.4, 0.8], [1,0,1]).predict([ecs_raw])[0]
    body = {
        "ecs": float(ecs),
        "claims": claims,
        "consensus": consensus,
        "provenance": {"prov_json": prov, "hash_version": HASH_VERSION},
        "errors": [],
        "timing_ms": {"total": int((time.time()-t0)*1000)}
    }
    return body