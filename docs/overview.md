# Overview

The **Epistemic Confidence Layer (ECL)** is a model-agnostic trust protocol:
1) Extract **atomic claims** from model outputs
2) Compare across models (agreement/contradiction + diversity)
3) Score **evidence**, **recency**, **stability**, **language integrity**
4) Calibrate to produce an **ECS** that matches real-world accuracy
5) Return JSON/Markdown with audit-ready provenance

Why now:
- General LLMs are fluent but not epistemically honest
- Enterprises & regulators require **calibrated** confidence
- Developers need a simple, open standard