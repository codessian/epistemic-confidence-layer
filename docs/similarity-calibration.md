# Similarity & Calibration

## Semantic Equivalence
ECL classifies claim pairs using cosine similarity over text embeddings.

- equivalent: cosine ≥ 0.95
- related: 0.85–0.95
- different: < 0.85

Backends:
- sentence-transformers (default) configurable via `ECL_ST_MODEL` (e.g. `all-MiniLM-L6-v2`)
- OpenAI embeddings via `ECL_OPENAI_EMBED_MODEL` (e.g. `text-embedding-3-small`)

Select backend with `ECL_EMBED_BACKEND=sentence-transformers|openai`.

## Calibration Baselines
- Isotonic Regression (`src/ecl/calibration/isotonic.py`)
- Platt Scaling (`src/ecl/calibration/platt.py`)

Use these to transform raw agreement/confidence scores into better-calibrated probabilities.

## Example
```python
from src.ecl.similarity import EmbeddingBackend, classify_pair
be = EmbeddingBackend()
label, sim = classify_pair("The sky is blue.", "The sky can appear azure.", backend=be)
print(label, sim)
```

```python
import numpy as np
from src.ecl.calibration.isotonic import IsotonicCalibrator
scores = np.linspace(0.0, 1.0, 20)
labels = (scores > 0.6).astype(int)
iso = IsotonicCalibrator().fit(scores, labels)
calibrated = iso.predict(scores)
```