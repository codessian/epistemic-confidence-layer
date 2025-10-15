# Contributing to Epistemic Confidence Layer

Thank you for your interest in contributing! This project aims to build a robust, principled foundation for confidence measurement and communication in AI systems. Thoughtful collaboration is essential.

We strive for a welcoming, respectful environment. Please be constructive, cite sources where relevant, and prefer clarity over cleverness.

## Ways to Contribute
- Report bugs and edge cases
- Propose features and improvements
- Discuss research and validation approaches
- Improve docs, examples, and tutorials
- Implement metrics, adapters, and visualizations

## Development Setup
1. Fork the repository and clone your fork.
2. Create a Python virtual environment.
   - Windows: `python -m venv .venv && .venv\Scripts\activate`
3. Install in editable mode:
   - `pip install -e .`
4. Run examples to validate local setup:
   - `python examples/hello.py`

Optional tooling (to be added later): formatter, linter, and pre-commit hooks.
## Issues
- Use clear, actionable titles
- Provide reproduction steps and environment details
- Link related discussions or PRs

## Pull Requests
- Start from a fresh branch per change
- Keep PRs focused and reasonably small
- Include tests or validation notes when applicable
- Update documentation if behavior or APIs change
- Reference related issues in the description (e.g., `Fixes #123`)

## Commit Messages
- Use imperative mood and concise summaries
- Include context for non-obvious changes
- Example: `Add reliability diagram helper and unit tests`

## Code Style and Testing
- Prefer readability and maintainability
- Add unit tests near new logic
- Keep examples runnable across common Windows setups

## License
By contributing, you agree that your contributions will be licensed under the Apache License, Version 2.0.
