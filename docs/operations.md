# Operations & Hygiene

## Nightly Reliability
We run a nightly evaluation at 02:00 UTC:
- Produces `benchmarks/results/metrics.json`
- Appends trend data to `benchmarks/trends/ece_trend.csv`
- Renders `benchmarks/trends/ece_trend.png`
- Uploads artifacts to the workflow run
- (If Discussions are enabled) posts a summary to Discussions

> Enable Discussions: **Settings → General → Discussions**.

## Release Notes
Release Drafter builds a draft from Conventional Commits. On tag, edit & publish the draft.

## Security Posture
OSSF Scorecard runs weekly and uploads SARIF results (visible in Security tab).