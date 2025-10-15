---
title: "How to get your first green PR ✅"
labels: []
---

Welcome! This playbook gets you from **clone → green PR** fast:

**1) Read this first:** [Tutorial: cURL → reliability curve](https://codessian.github.io/epistemic-confidence-layer/tutorial/)

**2) Bots & Gates**
- PR Verify bot runs: lint, type, tests, toy eval, ECE regression guard (+0.02 max)
- Triage bot auto-labels by area; add context for routing
- DCO sign-off required (`git commit -s -m "feat: …"`)

**3) Good-first issues**
Pick any issue labeled `good first issue` or `help wanted`. We love PRs that include a failing test first.

**4) Run locally**
```bash
pip install -r requirements.txt -r requirements-dev.txt
uvicorn src.ecl.server.app:app --reload
make evaluate
```

**5) Open a PR**
Follow the PR template, keep commit messages Conventional Commit style, and link to the issue.

Questions? Comment here. We’ll help you ship. 🚀