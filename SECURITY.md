# Security Policy

## Reporting a Vulnerability
Please email **security@codessian.org** with:
- Description, impact, and steps to reproduce
- Any logs, configs, or proof-of-concept (no secrets)

We will acknowledge within 72 hours and coordinate a fix & disclosure window.

## Secrets
- Never commit API keys or credentials. Use `.env` (see `.env.example`).

## Supply chain
- Pinned dependencies and SBOM recommended (CycloneDX).
- Dependabot enabled via GitHub settings.