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
uvicorn src.ecl.server.app:app --reload
```

The server starts at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` for interactive Swagger UI.

## 3. Make Your First Verification Request

### Using cURL
```bash
curl -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Is Knysna in the Western Cape of South Africa?",
    "models": ["stub:gpt", "stub:claude"]
  }'
```

### Expected Response
```json
{
  "claims": [
    {
      "id": "c_03911a33",
      "text": "Is Knysna in the Western Cape of South Africa?",
      "hash": "a8ed9f08c25a5811",
      "provenance": {
        "source": "extraction:heuristic"
      }
    }
  ],
  "consensus": [
    {
      "claim_id": "c_03911a33",
      "agreement_score": 0.8,
      "diversity_score": 0.6,
      "evidence": [],
      "recency": 1.0,
      "stability": 0.9,
      "language_integrity": 0.95,
      "ecs": 0.88
    }
  ]
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

### Using Real Providers (Optional)
```bash
# Set API keys in .env
ECL_OPENAI_API_KEY=your_key_here
ECL_ANTHROPIC_API_KEY=your_key_here

# Test with real models
curl -X POST http://127.0.0.1:8000/verify \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the capital of France?",
    "models": ["openai:gpt-3.5-turbo", "anthropic:claude-3-sonnet"]
  }'
```

### Batch Processing
Use the Python client for multiple requests:
```python
import requests

def verify_claim(prompt, models=["stub:gpt", "stub:claude"]):
    response = requests.post(
        "http://127.0.0.1:8000/verify",
        json={"prompt": prompt, "models": models}
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
    ecs = result["consensus"][0]["ecs"]
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