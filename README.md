# Veracity AI

[![Tests](https://github.com/dljones555/veracity-ai/actions/workflows/tests.yml/badge.svg)](https://github.com/dljones555/veracity-ai/actions/workflows/tests.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)

**Veracity Bill of Materials (VBOM)** — A universal verification standard for AI outputs. Automatically generates transparent reports showing which verification methods were used, confidence levels, and evidence sources for any AI response.

## Quick Start

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended package manager)

### Installation with uv

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Sync dependencies
uv sync

# Run the chat interface
uv run python -m veracity.cli

# Run tests
uv run pytest
```

### Installation with pip (legacy)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run the chat interface
python -m veracity.cli

# Run tests
pytest
```

## What is VBOM?

Veracity AI produces a structured Veracity Bill of Materials for AI outputs, similar to nutritional labels for food. Each response includes:

- **Verification Methods**: Which techniques were applied (search, reasoning, computation, HITL, etc.)
- **Confidence Score**: Evidence-based certainty (0-100%)
- **Evidence Sources**: Retrieved facts, executed code, reasoning chains
- **Trace Data**: Timestamps, tool calls, and audit logs

This enables users to understand *why* they should trust an AI response.

## Verification Methods

- **Structure Verification**: JSON Schema and Pydantic validation
- **Computation**: Execute code to verify claims mathematically
- **Search**: Retrieve and cross-reference external sources
- **Reasoning**: Chain-of-thought analysis and self-critique
- **HITL**: Human-in-the-loop review for sensitive claims

## Example

A `VeracityReport` captures a verification graph for a response, including method results, sources, and a final certainty score.

Example verification flow for a recipe claim:

- User asks: "Is bacon avocado toast healthy for breakfast?"
- System verifies:
  - `compute_verification` checks calories and saturated fat
  - `search_cross_reference` cites USDA and WHO sources
  - `cot_reasoning` flags the processed meat claim
  - `human_in_the_loop` may recommend review if confidence is low

Minimal example output:

```json
{
  "claim_type": "recipe",
  "methods_graph": [
    {"method": "compute_verification", "status": "pass", "sources": ["USDA"]},
    {"method": "search_cross_reference", "status": "warn", "sources": ["WHO", "Mayo Clinic"]},
    {"method": "cot_reasoning", "status": "warn"}
  ],
  "summary": {"overall_certainty": 68, "risk_level": "high"}
}
```

Another example is fact verification:

- User asks: "What is the 2025 inflation rate?"
- System verifies with source-backed web retrieval and returns a confidence score plus citations.

## Architecture

```
src/veracity/
├── schema.py      # VBOM Pydantic models (the standard)
├── verifiers/     # Verification implementations
├── pipeline.py    # Orchestrates verification workflow
├── llm.py         # GitHub Models API integration
├── rendering.py   # CLI report formatting
└── cli.py         # Interactive chat interface
```

## Features

- 🔗 **LLM-agnostic verification** with OpenAI-compatible endpoints
- 📦 **External system prompt support** via `system_prompt.md`
- 📊 **Structured Verification** with Pydantic v2
- 🔍 **Multi-method Verification** (search, compute, reason, HITL)
- 🧾 **JSON export** for shareable `VeracityReport` artifacts
- 🧪 **GitHub Actions CI** with `uv` support

## Configuration

Set environment variables:

```bash
export VERACITY_MODEL=openai/gpt-4o
export VERACITY_BASE_URL=https://models.github.ai/inference
export OPENAI_API_KEY=your_key_here
```

`OPENAI_API_KEY` and `VERACITY_API_KEY` are supported, and `GITHUB_TOKEN` will still work for GitHub Models API.

### Run the CLI

```bash
python -m veracity.cli
```

### Export JSON report

```bash
python -m veracity.cli --export-json report.json
```

### Use an external system prompt

```bash
python -m veracity.cli --system-prompt system_prompt.md
```

## Contributing

Contributions welcome! Tests and coverage required.

```bash
pytest --cov=src/veracity
```

## License

MIT

---

**Status**: Early development (v0.1.0)  
**Python**: 3.11+  
**Dependencies**: Pydantic v2, OpenAI SDK
