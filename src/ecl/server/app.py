from fastapi import FastAPI, Response
import json, time
from pathlib import Path
from ..provenance.prov import prov_json_for_claims, HASH_VERSION
from ..similarity import classify_similarity
from ..calibration.isotonic import IsotonicCalibrator
from ..cache import FileCache

app = FastAPI(title="ECL API")

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