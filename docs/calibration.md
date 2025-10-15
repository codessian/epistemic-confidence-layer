# Calibration

**Target:** ECE ≤ 0.10

Metrics:
- **ECE** (Expected Calibration Error)
- **Brier score**
- **NLL**

Baselines:
- **Platt scaling** (logistic)
- **Isotonic regression** (monotonic, non-parametric)

CI:
- Toy suite must render a reliability curve; regressions fail the build.