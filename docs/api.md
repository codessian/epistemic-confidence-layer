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
- `PROVIDER_TIMEOUT` → HTTP 504: Model provider API timeout
- `RATE_LIMITED` → HTTP 429: Request rate limit exceeded
- `NETWORK_ERROR` → HTTP 503: Connectivity/transport error calling provider
- `BAD_REQUEST` → HTTP 400: Invalid request to provider (client-side)
- `PROVIDER_ERROR` → HTTP 502: Provider internal/unknown error (transient)
- `CACHE_HIT`: Successful cache retrieval (info event only; not an error)
- `CALIBRATION_MISSING`: Calibration model not available
- `PROV_BUILD_FAIL`: Provenance graph construction failed

Each error includes fields: `code`, `message`, `hint`, `provider`, optional `status`, and optional `retry_after_ms` where applicable.

## Runtime Tuning

Environment variables to tune adapter behavior and caching:

- Provider timeouts and retries
  - `ECL_PROVIDER_TIMEOUT_S` (default `8.0`) per-call timeout seconds
  - `ECL_PROVIDER_MAX_ATTEMPTS` (default `3`) retry attempts
  - `ECL_PROVIDER_MAX_ELAPSED_S` (default `16.0`) max total elapsed seconds
  - `ECL_PROVIDER_BASE_DELAY_S` (default `0.6`) base backoff delay seconds
  - `ECL_PROVIDER_JITTER_S` (default `0.2`) random jitter seconds added to backoff

- Cache configuration
  - `ECL_CACHE_TTL_HOURS` (default `12`) adapter cache TTL
  - `ECL_CACHE_DIR` (default `.ecl_cache`) cache directory

- Provider credentials
  - `OPENAI_API_KEY` for OpenAI adapters
  - `ANTHROPIC_API_KEY` for Anthropic adapters
  - `GOOGLE_API_KEY` for Google Gemini adapters

## Schema Validation
Response format is validated against [`schemas/verify-response.json`](../schemas/verify-response.json).

Notes:
- `models` supports real adapters later; for now `stub:*` ensures deterministic demo.
- `hash` is a stable ID (text + span + timestamp + adapter).