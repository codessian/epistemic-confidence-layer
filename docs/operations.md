# Operations & Hygiene

## Running in Production

Recommended baseline:

- Run behind TLS termination (reverse proxy / load balancer).
- Enable API key auth (`ECL_AUTH_MODE=apikey`) for `/verify`.
- Set conservative timeouts and retry budgets to avoid request pileups.
- Configure rate limits appropriate for your traffic shape.

Operational endpoints:

- `GET /livez`: liveness
- `GET /readyz`: readiness + runtime validation
- `GET /health`: alias for liveness

## Logging and Correlation

- Every response includes `X-Request-ID`.
- `/verify` returns `request_id` in the response body.
- Use the request ID to correlate application logs and client errors.

## CI/CD Overview

Continuous integration runs on pull requests and main branch pushes. Key workflows include:

- `ci.yml`: tests and quality gates
- `schema-validate.yml`: schema checks for machine contracts in `schemas/`
- `providers-smoke.yml`: provider routing smoke tests
- `nightly-reliability.yml`: scheduled reliability evaluation and trending
- `ossf-scorecard.yml`: security posture scoring and SARIF publication

## Local Quality Gates

Typical developer commands (see `README.md`):

```bash
ruff check .
mypy src
pytest -q
```

## Nightly Reliability
We run a nightly evaluation at 02:00 UTC:
- Produces `benchmarks/results/metrics.json`
- Appends trend data to `benchmarks/trends/ece_trend.csv`
- Renders `benchmarks/trends/ece_trend.png`
- Uploads artifacts to the workflow run
- (If Discussions are enabled) posts a summary to Discussions

> Enable Discussions: **Settings → General → Discussions**.

## Release Notes
Release Drafter builds a draft from Conventional Commits. On tag, edit & publish the draft.

## Security Posture
OSSF Scorecard runs weekly and uploads SARIF results (visible in Security tab).

## Backup and Reproducibility

- Keep `policies/providers.yml` and `.env.example` consistent with production settings.
- Treat `.env` as a secret (never commit it).
- Capture benchmark artifacts (`benchmarks/results/`) for release comparisons.
