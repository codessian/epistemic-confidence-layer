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

Notes:
- `models` supports real adapters later; for now `stub:*` ensures deterministic demo.
- `hash` is a stable ID (text + span + timestamp + adapter).