# Troubleshooting

This page lists common issues and how to diagnose and resolve them.

## Server Startup Issues

### `ModuleNotFoundError` when running `uvicorn`

Symptoms:
- `ModuleNotFoundError: No module named 'src.server'` (or similar)

Checks:
- Ensure you are running from the repository root (the directory that contains `src/`).
- Ensure dependencies are installed in the active virtual environment.

Fix:

```bash
uvicorn src.server.app:app --reload
```

### Startup fails with `CONFIG_ERROR`

Symptoms:
- API returns a `CONFIG_ERROR` response.
- `/readyz` returns `503 not_ready` with a config-related message.

Common causes:
- `ECL_POLICY_FILE` points to a missing file.
- `policies/providers.yml` is invalid YAML or fails validation.
- Policy references an adapter kind that is not registered.

Actions:
- Verify the policy path: `ECL_POLICY_FILE` (default: `policies/providers.yml`).
- Review `policies/providers.yml` for valid provider IDs, kinds, and models.
- Call `GET /readyz` to see the set of registered adapters.

## Authentication and Authorization

### `401 UNAUTHORIZED` / `403 FORBIDDEN`

When `ECL_AUTH_MODE=apikey`, `/verify` requires `X-API-Key`.

Actions:
- Confirm `ECL_AUTH_MODE=apikey`.
- Set `ECL_API_KEYS` to a comma-separated list of valid keys.
- Provide `X-API-Key: <key>` on requests.

Example:

```bash
curl -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_key_here" \
  -d '{"prompt":"Test prompt","contains_pii":false}'
```

## Rate Limiting

### `429 RATE_LIMITED`

The server enforces a per-minute request budget.

Actions:
- Wait and retry.
- Increase `ECL_RATE_LIMIT_RPM` for your deployment.
- If `ECL_RATE_LIMIT_KEY_STRATEGY=api_key`, ensure clients send `X-API-Key` consistently.

## Provider and Adapter Issues

### Providers return stubbed outputs

Symptoms:
- Output text includes a provider stub prefix (e.g., `[openai-stub]`).

Explanation:
- If a provider SDK is unavailable or the corresponding API key is missing, ECL returns stubs for that adapter.

Actions:
- Set provider keys in `.env`:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `GOOGLE_API_KEY`
- Confirm the provider’s Python SDK is installed if required by that adapter.

### Timeouts calling providers

Symptoms:
- Response `errors[]` includes `PROVIDER_TIMEOUT` or `NETWORK_ERROR`.

Actions:
- Increase `ECL_DEFAULT_TIMEOUT_S` (and/or `ECL_MAX_TIMEOUT_S`) for server-side time budgeting.
- Ensure your reverse proxy timeouts (if any) are compatible with expected model latency.
- For provider-specific retries/backoff, see variables like `ECL_PROVIDER_TIMEOUT_S`, `ECL_PROVIDER_MAX_ATTEMPTS`, and `ECL_PROVIDER_MAX_ELAPSED_S`.

## Request Validation Errors

### `422 Unprocessable Entity`

FastAPI returns `422` when request JSON does not match the request model.

Common causes:
- Missing required fields (notably `contains_pii`)
- Wrong types (e.g., `"timeout_s": "8"` as a string)

Minimal valid request:

```json
{
  "prompt": "Hello",
  "contains_pii": false
}
```

## Diagnostics Checklist

- `GET /livez`: basic process health
- `GET /readyz`: startup validation + adapter registry sanity check
- `X-Request-ID` header: correlate logs and requests
- `errors[]` field in `/verify` responses: partial-failure visibility
