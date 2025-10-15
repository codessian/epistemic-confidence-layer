# Bots

ECL uses lightweight bots to keep quality high and reduce maintainer toil.

## ECL-Verify Bot (PR gatekeeper)
- Runs lint/type/tests + toy evaluation on every PR.
- Uploads reliability artifacts and comments ECE before/after with a chart.
- Fails CI if ECE regresses beyond a threshold (default `+0.02`).

**Files**
- Workflow: `.github/workflows/pr-verify.yml`
- Scripts: `.github/scripts/comment_eval.py`, `.github/scripts/enforce_threshold.py`

## ECL-Triage Bot (community concierge)
- Auto-labels issues/PRs by area (`adapters`, `calibration`, `provenance`, `docs`, `api`, `eval`).
- Welcomes first-time contributors with links to tutorial and DCO instructions.

**Files**
- Workflow: `.github/workflows/triage.yml`
- Labels: `.github/labeler.yml`

## Disable / tweak
- You can disable any workflow via GitHub UI → *Actions* → select workflow → *Disable*.
- Edit thresholds or messages directly in the workflow/scripts.