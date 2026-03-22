# Tutorial: From cURL to Reliability Curve

This tutorial walks you through ECL's complete workflow: setting up the API, making verification requests, and generating reliability analysis.

## Prerequisites

- Python 3.11+
- Git
- Optional: API keys for OpenAI/Anthropic (for real providers)

## 1. Setup (5 minutes)

### Clone and Install
```bash
git clone https://github.com/codessian/epistemic-confidence-layer.git
cd epistemic-confidence-layer
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
```

### Environment Configuration
```bash
cp .env.example .env
# Edit .env with your API keys (optional for stub mode)
```

## 2. Start the API Server

```bash
uvicorn src.server.app:app --reload
```

The server starts at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` for interactive Swagger UI.

## 3. Make Your First Verification Request

### Using cURL
```bash
curl -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Is Knysna in the Western Cape of South Africa?",
    "contains_pii": false
  }'
```

### Expected Response
```json
{
  "x_schema_version": "1.2",
  "request_id": "…",
  "route_id": "…",
  "ecs": 0.88,
  "claims": [{ "text": "…" }],
  "consensus": { "score": 0.7, "details": {}, "models": ["…", null] },
  "provenance": { "prov_json": {}, "hash_version": "…" },
  "errors": [],
  "timing_ms": { "total": 1234 }
}
```

## 4. Understanding the Response

- **Claims**: Atomic statements extracted from your prompt
- **Consensus**: Agreement analysis across models with calibrated confidence
- **ECS**: Epistemic Confidence Score (0-1, where 1 = highest confidence)

## 5. Generate Reliability Analysis

### Run Evaluation
```bash
python benchmarks/scripts/plot_reliability.py \
  --input benchmarks/tasks/toy.jsonl \
  --output benchmarks/results/reliability.png
```

This generates a reliability curve showing how well confidence scores match actual accuracy.

### View Results
The plot shows:
- **Perfect calibration line** (diagonal): ideal confidence-accuracy relationship
- **Actual performance points**: how ECL performs on test data
- **ECE score**: Expected Calibration Error (lower is better)

## 6. Advanced Usage

### Using the CLI (User-Friendly)

ECL ships a small CLI wrapper around `POST /verify`.

Run it from the repository root:

```bash
python -m src.cli "What is the capital of France?"
```

If your server is running on a different host/port:

```bash
python -m src.cli "Test prompt" --host http://127.0.0.1:8000
```

If API key auth is enabled:

```bash
python -m src.cli "Test prompt" --api-key your_key_here
```

### Using Real Providers (Optional)
```bash
# Set API keys in .env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Test with real models
Provider selection is configured by policy (not per-request). To choose which providers/models participate, edit `policies/providers.yml` and adjust:

- provider entries (`id`, `kind`, `model`, `allow_pii`)
- strategy selection (`k` and `providers`)
### Batch Processing
Use the Python client for multiple requests:
```python
import requests
import requests

def verify_claim(prompt):
    response = requests.post(
        "http://127.0.0.1:8000/verify",
        json={"prompt": prompt, "contains_pii": False}
    )
    return response.json()

# Process multiple claims
claims = [
    "The Earth is round.",
    "Python was created in 1991.",
    "The speed of light is constant."
]

for claim in claims:
    result = verify_claim(claim)
    ecs = result["ecs"]
    print(f"Claim: {claim}")
    print(f"Confidence: {ecs:.2f}")
    print("---")
```

## 7. Next Steps

- **Contribute**: Check out [good first issues](https://github.com/codessian/epistemic-confidence-layer/labels/good%20first%20issue)
- **Integrate**: Use ECL in your applications via the REST API
- **Extend**: Add new model providers or calibration methods
- **Research**: Experiment with different confidence metrics

## Troubleshooting

### Server Won't Start
- Check Python version: `python --version` (should be 3.11+)
- Verify dependencies: `pip list | grep fastapi`
- Check port availability: `netstat -an | grep 8000`

### API Errors
- **429 Rate Limited**: Wait and retry
- **Provider timeout**: Check API keys and network connection
- **Invalid JSON**: Validate request format against schema

### Need Help?
- [GitHub Discussions](https://github.com/codessian/epistemic-confidence-layer/discussions)
- [API Documentation](api.md)
- [Contributing Guide](../CONTRIBUTING.md)

---

**Congratulations!** You've successfully run ECL end-to-end. You're now ready to integrate calibrated confidence into your AI applications.

### Optional: enable semantic similarity
By default, ECL uses `sentence-transformers` for embeddings. To switch to OpenAI embeddings:

```bash
export ECL_EMBED_BACKEND=openai
export OPENAI_API_KEY=your_openai_key
export ECL_OPENAI_EMBED_MODEL=text-embedding-3-small
```

You can also configure the Sentence-Transformers model:

```bash
export ECL_EMBED_BACKEND=sentence-transformers
export ECL_ST_MODEL=all-MiniLM-L6-v2
```

Similarity thresholds:
- `equivalent` if cosine ≥ 0.95
- `related` if 0.85–0.95
- `different` if < 0.85
