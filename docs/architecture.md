# Architecture

```
                 +-------------------------+
  Prompt  ───▶   |  Claim Extraction       |  ───▶ claims[]
                 +-------------------------+
                            │
                            ▼
                 +-------------------------+
                 | Cross-Model Comparison |  ───▶ agreement/contradiction
                 +-------------------------+
                            │
                            ▼
                 +-------------------------+
                 |   Calibration Layer     |  ───▶ ECS (calibrated)
                 |   (ECE/Brier/Isotonic)  |
                 +-------------------------+
                            │
                            ▼
                 +-------------------------+
                 |  Synthesis & Reporting  |  ───▶ JSON/Markdown
                 +-------------------------+
```

Key ideas:
- **Atomic claims** reduce surface area for error.
- **Consensus** ≠ truth; we also score **diversity**, **evidence**, **recency**, **stability**, **language integrity**.
- **Calibration** is a contract with the user.