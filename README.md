# Epistemic Confidence Layer (ECL)

[![CI](https://github.com/codessian/epistemic-confidence-layer/actions/workflows/ci.yml/badge.svg)](https://github.com/codessian/epistemic-confidence-layer/actions/workflows/ci.yml)
[![Docs](https://github.com/codessian/epistemic-confidence-layer/actions/workflows/docs.yml/badge.svg)](https://codessian.github.io/epistemic-confidence-layer/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](#)

> **TLS for Knowledge.** A model-agnostic trust protocol that turns fluent AI into **calibrated**, **auditable** systems.

**Goal:** When an AI says "80% confident," it's correct ~80% of the time (ECE ≤ 0.10).

## Why ECL
- **Hallucinations happen.** ECL decomposes outputs into **atomic claims**, checks **cross-model agreement**, scores **evidence**, **recency**, **stability**, and **language integrity**, then returns a calibrated **Epistemic Confidence Score (ECS)**.
- **Model-agnostic.** Works across GPT/Claude/Gemini/local LLMs; includes a **stub mode** for offline dev.
- **Auditable provenance.** W3C-PROV style graph with hashes & timestamps.

## Quickstart (60 seconds)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn src.ecl.server.app:app --reload
```

▶️ **Try the API:** Open http://127.0.0.1:8000/docs for interactive Swagger UI

Then test with curl:
```bash
curl -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Is Knysna in the Western Cape of South Africa?", "models":["stub:gpt","stub:claude"]}'
```

## Real Providers Setup

For production use with actual model providers:

```bash
# Copy environment template
cp .env.example .env

# Add your API keys
ECL_OPENAI_API_KEY=your_openai_key
ECL_ANTHROPIC_API_KEY=your_anthropic_key
ECL_EMBED_BACKEND=sentence-transformers  # or "openai"
```

**Local Models:** ECL supports Ollama for offline development:
```bash
# Install Ollama, then:
ECL_LOCAL_MODEL=ollama:llama3.1:8b
ECL_OLLAMA_BASE_URL=http://localhost:11434
```

**Response (stubbed):**
```json
{
  "claims": [
    {"id":"c_1","text":"Knysna is in the Western Cape of South Africa.","hash":"...","provenance":{"source":"extraction:heuristic"}}
  ],
  "consensus": [
    {"claim_id":"c_1","agreement_score":0.95,"diversity_score":0.60,"evidence":[],"recency":1.0,"stability":0.9,"language_integrity":0.95,"ecs":0.88}
  ]
}
```

## Architecture
```
Prompt → Claim Extraction → Cross-Model Comparison → Contradiction Detection
      → Calibration (ECE/Brier) → Guardrailed Synthesis → API/Dashboard
```

- More: [`docs/overview.md`](docs/overview.md), [`docs/architecture.md`](docs/architecture.md), [`docs/api.md`](docs/api.md), [`docs/calibration.md`](docs/calibration.md)
- **📚 Full Documentation:** https://codessian.github.io/epistemic-confidence-layer/

## Calibration Target
- **ECE ≤ 0.10** on the project's evaluation harness (see `benchmarks/`).
- CI fails if calibration regresses on toy suite.

## Development
```bash
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
ruff check .
mypy src
pytest -q
```

Shortcuts:
```bash
make demo      # run server & minimal example
make evaluate  # run toy benchmark & plot reliability
```

## Governance & Security
- License: Apache-2.0
- See: [`docs/governance.md`](docs/governance.md), [`SECURITY.md`](SECURITY.md), [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Roadmap
See [`ROADMAP.md`](ROADMAP.md).

## Bots
Automated assistants keep quality high:
- **ECL-Verify Bot** runs tests/eval on PRs and posts ECE results.
- **ECL-Triage Bot** labels issues and welcomes new contributors.
See [`docs/bots.md`](docs/bots.md).

## Community
- Ask questions in **Discussions**.
- Issues welcome—start with `good first issue`.
