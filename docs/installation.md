# Installation & Configuration

This guide covers installation and configuration for both local development and production-like deployments.

## Prerequisites

- Python 3.11+
- Git
- Optional (recommended for containerized runs): Docker + Docker Compose
- Optional (for live providers): provider API keys (see `.env.example`)

## Option A: Local Python (Recommended for Development)

### 1) Clone the Repository

```bash
git clone https://github.com/codessian/epistemic-confidence-layer.git
cd epistemic-confidence-layer
```

### 2) Create a Virtual Environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Install Dependencies

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

### 4) Configure Environment Variables

Copy the template and edit values:

Linux/macOS:

```bash
cp .env.example .env
```

Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

Key settings:

- `ECL_POLICY_FILE` (default: `policies/providers.yml`)
- `ECL_DEFAULT_TIMEOUT_S` / `ECL_MAX_TIMEOUT_S`
- `ECL_AUTH_MODE` and `ECL_API_KEYS` (optional API key auth)
- Provider keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY` (optional; stubs used if missing)

### 5) Run the API Server

```bash
uvicorn src.server.app:app --reload
```

- Swagger UI: `http://127.0.0.1:8000/docs`
- Health endpoints: `/livez`, `/readyz`, `/health`

## Option B: Docker Compose (Recommended for Stakeholders / “It Just Runs”)

### 1) Configure `.env`

```bash
cp .env.example .env
```

### 2) Build and Run

```bash
docker compose up --build
```

- API is exposed on `http://127.0.0.1:8000`
- Health check hits `GET /livez`

### 3) Run Tests in Containers

```bash
docker compose run --rm tests
```

## Configuration Reference

### Server Settings (Environment Variables)

These environment variables are consumed by `src/config.py` and applied by `src/server/app.py`:

- `ECL_POLICY_FILE` (string, default: `policies/providers.yml`)
- `ECL_DEFAULT_TIMEOUT_S` (float, default: `8.0`)
- `ECL_MAX_TIMEOUT_S` (float, default: `60.0`)
- `ECL_MAX_PROMPT_LENGTH` (int, default: `10000`)
- `ECL_CACHE_TTL_HOURS` (int, default: `4`)
- `ECL_RATE_LIMIT_RPM` (int, default: `60`)
- `ECL_RATE_LIMIT_BURST` (int, default: `10`)
- `ECL_RATE_LIMIT_KEY_STRATEGY` (`ip` | `api_key`, default: `ip`)
- `ECL_AUTH_MODE` (`off` | `apikey`, default: `off`)
- `ECL_API_KEYS` (comma-separated list; used when `ECL_AUTH_MODE=apikey`)

### Provider Credentials (Environment Variables)

Adapters use standard provider key names:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY`

If a key is missing or the provider SDK is not installed, the adapter returns a deterministic **stub** generation (useful for offline development and CI).

### Routing Policy (`policies/providers.yml`)

The policy file defines:

- A list of **providers** (id, kind, model, allow_pii)
- A list of **strategies** (selection rules and constraints)

At runtime, ECL loads the policy and selects providers for each `/verify` request.

## Production Notes (Hardening Checklist)

- Enable API auth: set `ECL_AUTH_MODE=apikey` and configure `ECL_API_KEYS`.
- Configure rate limiting appropriate for your environment.
- Run behind a reverse proxy (TLS termination) and set request timeouts consistently end-to-end.
- Store secrets in a secret manager (avoid committing `.env`).
