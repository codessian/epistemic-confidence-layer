# Architecture

```
                 +-------------------------+
  Prompt  ───▶   |  Claim Extraction       |  ───▶ claims[]
                 +-------------------------+
                            │
                            ▼
                 +-------------------------+
                 | Cross-Model Comparison |  ───▶ agreement/contradiction
                 +-------------------------+
                            │
                            ▼
                 +-------------------------+
                 |   Calibration Layer     |  ───▶ ECS (calibrated)
                 |   (ECE/Brier/Isotonic)  |
                 +-------------------------+
                            │
                            ▼
                 +-------------------------+
                 |  Synthesis & Reporting  |  ───▶ JSON/Markdown
                 +-------------------------+
```

## Key Ideas

- **Atomic claims** reduce surface area for error and enable finer-grained scoring.
- **Consensus** is not “truth”; ECL also tracks diversity and other signals to avoid overconfidence.
- **Calibration** is a contract: the reported ECS should match real-world accuracy at the chosen operating point.
- **Auditability** is a first-class output: provenance is returned alongside the score.

## Runtime Component Map

ECL is organized as a small set of cooperating modules:

- **API server**: [app.py](file:///c:/Projects/ecl/src/server/app.py)
  - FastAPI app definition (`FastAPI(title="ECL API", version="1.2.0")`)
  - Middleware: request IDs, API key auth, rate limiting
  - Endpoints: `/verify`, `/livez`, `/readyz`, `/health`
- **Configuration**: [config.py](file:///c:/Projects/ecl/src/config.py)
  - Environment variable settings
  - Policy file loading and validation (`policies/providers.yml`)
- **Routing**: [router.py](file:///c:/Projects/ecl/src/router.py)
  - Policy validation and provider selection
  - Partial-failure execution model: successful generations + `errors[]`
  - File-backed caching to avoid repeated provider calls for identical prompts
- **Providers (adapters)**: `src/adapters/`
  - Normalizes provider APIs to a common `generate()` method
  - Implements retry/backoff and consistent error normalization
  - Supports stubbed output when SDK/keys are missing (useful for offline dev/CI)
- **Consensus scoring**: `src/consensus/`
  - Produces a raw consensus score and metadata for calibration
- **Calibration**: `src/calibration/`
  - Converts raw signals into ECS and provides calibration metrics (ECE, Brier, etc.)
- **Provenance**: `src/provenance/`
  - Constructs provenance artifacts (returned as `provenance.prov_json`)

## Request Flow (Concrete)

This is the execution path for `POST /verify`:

1. **Request parsing and validation**
   - FastAPI validates the JSON body (notably: `prompt` and `contains_pii`).
2. **Request context**
   - Middleware assigns `request_id` (also returned in the `X-Request-ID` header).
3. **Auth and rate limits**
   - Optional API key enforcement (when enabled) and per-minute request limiting.
4. **Settings and policy load**
   - Settings from environment variables; policy from `policies/providers.yml`.
5. **Provider selection**
   - Router selects `k` providers from the configured strategy (shuffled).
6. **Generation loop**
   - For each provider:
     - Enforces PII constraints (`allow_pii` vs `contains_pii`)
     - Attempts cached generation, otherwise calls adapter `generate()`
     - Records any failures into `errors[]` without necessarily failing the request
7. **Consensus + calibration**
   - Computes a raw consensus score over returned texts
   - Calibrates to ECS (`ecs` field)
8. **Provenance**
   - Builds provenance output from provider generations and routing metadata
9. **Response**
   - Returns schema versioned result (`x_schema_version=1.2`) with timing and errors

## Extension Points

### Add a New Provider

1. Implement an adapter in `src/adapters/` that follows the BaseAdapter interface.
2. Register it at startup in [app.py](file:///c:/Projects/ecl/src/server/app.py).
3. Add a provider entry in `policies/providers.yml` using the adapter’s `kind`.

### Change Routing Strategy

Routing is policy-driven. To change which providers participate:

- Edit `policies/providers.yml` to update provider entries and strategy selection rules.

### Evolve the API

The API is explicitly schema-versioned via `x_schema_version`. When response fields change:

- Bump the FastAPI app version and `x_schema_version`
- Update `schemas/verify-response.json`
- Update [API docs](api.md) and related tests
