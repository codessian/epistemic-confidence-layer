# ECL Roadmap

## v0.1 ✅ (Completed)
- API stub: `POST /verify` end-to-end with stubs
- Deterministic claim extraction & consensus mock
- Toy eval & reliability plot in CI
- Docs: overview, architecture, API, calibration, governance

## v0.2 🚧 (In Progress - 10-14 days)

**Goal:** One real, auditable verification path with calibrated confidence.

### Core Features
- **Real Provider Adapters**: OpenAI, Anthropic + local model (Ollama)
- **Semantic Equivalence**: sentence-transformers with configurable thresholds
- **Calibration v1**: Isotonic regression + Platt scaling comparison
- **W3C PROV**: Provenance graph with stable claim hashing
- **Performance**: Caching + rate limiting with metrics

### Success Criteria (Measurable)
- ✅ ECE improves ≥25% post-calibration on toy set
- ✅ End-to-end `/verify` returns PROV graph + ECS in <4s (2 providers, cold)
- ✅ 80%+ unit test coverage on core modules

### Timeline
- **Days 1-2**: Issues, secrets setup, local model path
- **Days 3-6**: Real adapters + backoff/circuit-breaker + similarity
- **Days 7-9**: Calibration + PROV-JSON + OpenAPI schema updates
- **Days 10-14**: Cache + rate-limit + `/health` + tutorial + v0.2.0 release

## v0.3 (Planned)
- Caching, rate limiting, tracing
- "Diversity" signals (model family, data vintage, decoding)
- First external pilot & evaluation on public tasks
- Minimal dashboard (reliability curve, dissent map)

## Success metric
- ECE ≤ 0.10 on internal suite; no regression allowed by CI.