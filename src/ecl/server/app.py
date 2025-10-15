from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict
import orjson

from src.ecl.claims.extract import heuristic_extract
from src.ecl.consensus.score import score_consensus

class VerifyRequest(BaseModel):
    prompt: str
    models: List[str] = Field(default_factory=lambda: ["stub:gpt","stub:claude"])

class VerifyResponse(BaseModel):
    claims: List[Dict]
    consensus: List[Dict]

def _dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()

app = FastAPI(title="ECL API")

@app.post("/verify", response_model=VerifyResponse)
def verify(req: VerifyRequest):
    claims = heuristic_extract(req.prompt)
    consensus = score_consensus(claims, req.models)
    return VerifyResponse(claims=claims, consensus=consensus)