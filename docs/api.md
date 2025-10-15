# API

## `POST /verify`
Request:
```json
{
  "prompt": "string",
  "models": ["stub:gpt","stub:claude"]
}
```

Response:
```json
{
  "claims": [
    {"id":"c_1","text":"...", "hash":"...", "provenance":{"source":"extraction:heuristic"}}
  ],
  "consensus": [
    {"claim_id":"c_1","agreement_score":0.95,"diversity_score":0.60,"evidence":[],"recency":1.0,"stability":0.9,"language_integrity":0.95,"ecs":0.88}
  ]
}
```

## Error Handling

ECL uses standard HTTP status codes and structured error responses:

### Rate Limiting (429)
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded",
    "hint": "Try again later",
    "retry_after_ms": 60000
  }
}
```

### Error Codes
- `PROVIDER_TIMEOUT`: Model provider API timeout
- `CACHE_HIT`: Successful cache retrieval (info only)
- `CALIBRATION_MISSING`: Calibration model not available
- `PROV_BUILD_FAIL`: Provenance graph construction failed
- `RATE_LIMITED`: Request rate limit exceeded

## Schema Validation
Response format is validated against [`schemas/verify-response.json`](../schemas/verify-response.json).

Notes:
- `models` supports real adapters later; for now `stub:*` ensures deterministic demo.
- `hash` is a stable ID (text + span + timestamp + adapter).