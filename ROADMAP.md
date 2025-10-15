# ECL Roadmap

## v0.1 (this PR)
- API stub: `POST /verify` end-to-end with stubs
- Deterministic claim extraction & consensus mock
- Toy eval & reliability plot in CI
- Docs: overview, architecture, API, calibration, governance

## v0.2
- Pluggable adapters for providers (OpenAI, Anthropic, Google, LM Studio)
- Semantic equivalence via embeddings + thresholds (equivalent/related)
- Isotonic calibration baseline + logging of Platt
- Basic provenance graph (W3C PROV entities/agents/activities)

## v0.3
- Caching, rate limiting, tracing
- "Diversity" signals (model family, data vintage, decoding)
- First external pilot & evaluation on public tasks
- Minimal dashboard (reliability curve, dissent map)

## Success metric
- ECE ≤ 0.10 on internal suite; no regression allowed by CI.