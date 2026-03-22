# Overview

The **Epistemic Confidence Layer (ECL)** is a model-agnostic verification and calibration layer that turns LLM outputs into **calibrated**, **auditable** results. ECL is designed to be used as:

- A lightweight **REST API** you can place in front of one or more model providers
- A local **developer tool** (stub providers supported when keys are absent)
- A reproducible **evaluation harness** for reliability tracking (see `benchmarks/`)

## What ECL Produces

Given a prompt and runtime constraints, ECL returns:

- **ECS (Epistemic Confidence Score)**: a 0–1 calibrated confidence score
- **Claims**: extracted atomic statements (currently returned as text items)
- **Consensus details**: agreement/contradiction signals and scoring metadata
- **Provenance**: a structured provenance artifact suitable for audits
- **Errors**: partial-failure reporting when one or more providers fail

## Core Workflow (Conceptual)

1. **Route** the request to a selected set of providers based on policy.
2. **Generate** outputs (or stubs) with retries, timeouts, and caching.
3. **Score consensus** from returned texts (agreement + diversity and related metrics).
4. **Calibrate** the raw consensus signal into ECS.
5. **Return** an API response with provenance and error details.

## Project Layout (High-Level)

- `src/server/`: FastAPI application and middleware (`src/server/app.py`)
- `src/router.py`: provider selection policy and partial-failure routing
- `src/adapters/`: provider integrations (OpenAI, Anthropic, Gemini, etc.)
- `src/config.py`: settings and policy loading via environment variables and YAML
- `src/calibration/`: calibration methods and metrics
- `src/provenance/`: provenance artifacts (W3C-PROV style JSON)
- `schemas/`: machine-checkable JSON schema for API responses
- `docs/`: documentation pages rendered via MkDocs

## Who This Documentation Is For

- **API consumers**: integrate `/verify` into your systems.
- **Operators**: deploy ECL, configure auth/rate limits, and monitor reliability.
- **Contributors**: add providers, improve calibration methods, or extend scoring.

## Terminology (Glossary)

- **Provider**: a concrete model endpoint (e.g., “OpenAI GPT-4o-mini”) described in `policies/providers.yml`.
- **Adapter**: code that calls a provider (or returns a stub) in `src/adapters/`.
- **Policy**: routing configuration that selects which providers to query.
- **Route**: a single execution of provider selection + generation.
- **ECS**: Epistemic Confidence Score (0–1), returned as `ecs` in responses.
- **Request ID**: correlation identifier returned as `request_id` and echoed in `X-Request-ID`.

## Getting Started

- Installation and configuration: [Installation](installation.md)
- End-to-end walkthrough: [Tutorial](tutorial.md)
- API request/response details: [API](api.md)
- System design details: [Architecture](architecture.md)
- Operational guidance: [Operations](operations.md)
