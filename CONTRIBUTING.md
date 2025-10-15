# Contributing to ECL

Thanks for helping build a universal trust protocol for AI. ✨

## Ground rules
- Be kind. Assume good intent. Bias toward clarity.
- Small, reviewable PRs > giant changes.
- Include/refresh tests and docs with any behavior change.
- Never commit secrets. Use `.env.example`.

## How to contribute
1. **Pick an issue** (good-first-issue are tagged) or open one with context.
2. **Create a branch**: `feat/<short-name>` or `fix/<short-name>`.
3. **Dev setup**:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt -r requirements-dev.txt
   pre-commit install
   ```
4. **Run checks**:
   ```bash
   ruff check .
   mypy src
   pytest -q
   ```
5. **Submit a PR** with a clear title and checklist of changes.

## Commit style
- Conventional commits are preferred: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `perf:`, `build:`, `ci:`.
- We use **SemVer**: breaking changes require `BREAKING CHANGE:` in commit body.

## Sign-off (DCO)
All commits must be signed off to certify you have the right to submit the code:
```bash
git commit -s -m "feat: add new calibration method"
```

## Code of conduct
See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security
Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).
