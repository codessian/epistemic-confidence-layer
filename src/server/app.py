from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json, time, yaml, os
from pathlib import Path
from ..provenance.prov import prov_json_for, prov_from_generations, HASH_VERSION
from ..similarity import classify_similarity
from ..calibration.isotonic import IsotonicCalibrator
from ..cache import FileCache
from ..errors import AdapterError
from ..consensus.score import score_consensus
from ..router import DynamicRouter, ProviderSpec, RoutePolicy

app = FastAPI(title="ECL API", version="0.2.0")

class VerifyRequest(BaseModel):
    prompt: str = "State one security best practice for cookies."
    contains_pii: bool = False
    timeout_s: float = 8.0


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
def verify(req: VerifyRequest):
    t0 = time.time()
    # Dynamic Router load (policy & providers)
    pol_path = os.getenv("ECL_POLICY_FILE", "policies/providers.yml")
    try:
        with open(pol_path) as f:
            pol = yaml.safe_load(f)
    except FileNotFoundError:
        # Fallback to stub behavior if no policy file
        claims = [{"text": "httpOnly cookies mitigate XSS token theft"}]
        prov = prov_json_for(claims)
        _, sim = classify_similarity("A", "A")
        consensus = {"models": ["stub:gpt", "stub:claude"], "score": sim, "details": [{"model":"stub:gpt"}, {"model":"stub:claude"}]}
        ecs_raw = 0.62
        ecs = IsotonicCalibrator().fit([ecs_raw, 0.4, 0.8], [1,0,1]).predict([ecs_raw])[0]
        return {
            "ecs": float(ecs),
            "claims": claims,
            "consensus": consensus,
            "provenance": {"prov_json": prov, "hash_version": HASH_VERSION},
            "errors": [],
            "timing_ms": {"total": int((time.time()-t0)*1000)},
            "x_schema_version": "1.1",
        }
    
    specs = [ProviderSpec(**p) for p in pol.get("providers",[])]
    pol_cfg = pol.get("strategies",[{"name":"default","select":{"type":"quorum_k_of_n","k":2,"providers":[]}}])[0]
    policy = RoutePolicy(name=pol_cfg["name"], select=pol_cfg["select"], constraints=pol_cfg.get("constraints",{}))
    router = DynamicRouter(specs, policy)
    gens, rmeta = router.generate(req.prompt, contains_pii=req.contains_pii, timeout_s=req.timeout_s)
    texts = [g.text for g in gens if g.text]
    cscore, cdetail = score_consensus(texts, router_meta=rmeta)
    ecs = IsotonicCalibrator().fit([cscore, 0.4, 0.8], [1,0,1]).predict([cscore])[0]
    prov = prov_from_generations(gens, route_meta=rmeta)
    return {
        "x_schema_version": "1.1",
        "ecs": float(ecs),
        "claims": [{"text": t} for t in texts[:3]],
        "consensus": {"score": cscore, "details": cdetail, "models": [g.metadata.get("model") for g in gens]},
        "provenance": {"prov_json": prov, "hash_version": HASH_VERSION},
        "errors": [],
        "timing_ms": {"total": int((time.time()-t0)*1000)},
    }