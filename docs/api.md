# API

The ECL API is implemented in [app.py](file:///c:/Projects/ecl/src/server/app.py) using FastAPI.

## Base URL

Default local base URL:

- `http://127.0.0.1:8000`

## Endpoints

### `GET /livez`

Liveness probe.

Response:

```json
{ "status": "ok" }
```

### `GET /readyz`

Readiness probe. Performs runtime validation and returns the set of registered adapter kinds.

Success response:

```json
{
  "status": "ready",
  "registered_adapters": ["anthropic", "openai", "ollama"]
}
```

Failure response (`503`):

```json
{
  "status": "not_ready",
  "detail": "…"
}
```

### `GET /health`

Alias for `/livez`.

### `POST /verify`

Verifies a prompt by routing to providers (per policy), scoring consensus, calibrating to ECS, and returning provenance plus partial-failure details.

#### Request

```json
{
  "prompt": "string (1..10000 chars)",
  "contains_pii": false,
  "timeout_s": 8.0,
  "request_id": "optional string"
}
```

Fields:

- `prompt` (required): The prompt to verify.
- `contains_pii` (required): Whether the prompt contains PII. Routing enforces provider PII constraints.
- `timeout_s` (optional): Per-request time budget (clamped by server max timeout).
- `request_id` (optional): Client-supplied correlation identifier. If omitted, the server generates one.

#### Response (Schema v1.2)

Response schema is validated by [`schemas/verify-response.json`](../schemas/verify-response.json).

Example response:

```json
{
  "x_schema_version": "1.2",
  "request_id": "a7e02f09-0e68-4bd1-ae5e-5a245e9f4046",
  "route_id": "route-1732660100123",
  "ecs": 0.88,
  "claims": [
    { "text": "…" }
  ],
  "consensus": {
    "score": 0.7,
    "details": {},
    "models": ["gpt-4o-mini", null]
  },
  "provenance": {
    "prov_json": {},
    "hash_version": "…"
  },
  "errors": [
    {
      "provider_id": "openai_primary",
      "provider_kind": "openai",
      "model": "gpt-4o-mini",
      "code": "PROVIDER_TIMEOUT",
      "message": "[openai] PROVIDER_TIMEOUT: … (status=504)",
      "retryable": true,
      "retry_after_ms": null
    }
  ],
  "timing_ms": { "total": 1234 }
}
```

#### HTTP Headers

- `X-Request-ID` (response): correlation ID assigned by the server (or forwarded from request).
- `X-Request-ID` (request, optional): if provided, becomes the server request ID unless overridden by `request_id` in the JSON body.
- `X-API-Key` (request, conditional): required when API key auth is enabled (see below).

## Authentication

ECL supports optional API key authentication at the HTTP layer:

- Configure `ECL_AUTH_MODE=apikey`
- Set `ECL_API_KEYS` to a comma-separated list of valid keys
- Send `X-API-Key: <key>` on requests to `/verify`

Health endpoints (`/livez`, `/readyz`, `/health`) are always accessible without authentication.

## Rate Limiting

ECL applies a per-minute request budget to non-health endpoints:

- `ECL_RATE_LIMIT_RPM`: requests per minute
- `ECL_RATE_LIMIT_KEY_STRATEGY`: `ip` or `api_key`

When limited, ECL returns `429` and a structured error envelope.

## Error Handling

ECL uses standard HTTP status codes and a structured error envelope for top-level API errors:

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "[server] RATE_LIMITED: Rate limit exceeded; respect Retry-After. (status=429) (retry_after_ms=1000)",
    "status": 429,
    "hint": "Rate limit exceeded; respect Retry-After.",
    "request_id": "…",
    "retry_after_ms": 1000
  }
}
```

Common error codes:

- `BAD_REQUEST` (400)
- `UNAUTHORIZED` (401)
- `FORBIDDEN` (403)
- `RATE_LIMITED` (429)
- `NETWORK_ERROR` (503)
- `ADAPTER_UNAVAILABLE` (503)
- `PROVIDER_TIMEOUT` (504)
- `PROVIDER_ERROR` (502)

Partial provider failures do not necessarily fail the request. Provider-level issues are surfaced in the `/verify` response as `errors[]`.

## Examples

### cURL

```bash
curl -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Is Knysna in the Western Cape of South Africa?","contains_pii":false}'
```

### Python (requests)

```python
import requests

resp = requests.post(
    "http://127.0.0.1:8000/verify",
    json={"prompt": "What is the capital of France?", "contains_pii": False},
    timeout=30,
)
resp.raise_for_status()
data = resp.json()
print(data["ecs"])
```
