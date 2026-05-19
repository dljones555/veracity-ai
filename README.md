# Veracity AI

[![Tests](https://github.com/dljon/veracity-ai/actions/workflows/tests.yml/badge.svg)](https://github.com/dljon/veracity-ai/actions/workflows/tests.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)

**Veracity Bill of Materials (VBOM)** — A universal verification standard for AI outputs. Automatically generates transparency reports showing which verification methods were used, confidence levels, and evidence sources for any AI response.

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

- 🔗 **GitHub Models API** integration (`openai/gpt-4o` by default)
- 📊 **Structured Verification** with Pydantic v2
- 🔍 **Multi-method Verification** (search, compute, reason, HITL)
- 🎨 **Rich CLI Output** with formatted reports
- 🧪 **100% Test Coverage** target

## Configuration

Set environment variables:

```bash
export GITHUB_TOKEN=your_token_here
export VERACITY_MODEL=openai/gpt-4o  # Optional, defaults to gpt-4o
```

The CLI will prompt for missing credentials.

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
