# Veracity AI

## Project
Universal verification standard for AI outputs. Produces a verification graph for any AI response.

## Stack
- Python 3.11+, Pydantic v2, openai SDK
- GitHub Models API (`https://models.github.ai/inference`) via `GITHUB_TOKEN`
- Default model: `openai/gpt-4o` (override with `VERACITY_MODEL`)

## Commands
- Install: `uv venv && uv sync`
- Test: `uv run pytest`
- Run: `uv run python -m veracity.cli`

## Structure
- `src/veracity/schema.py` — Verification graph Pydantic models (the standard)
- `src/veracity/verifiers/` — verification method implementations
- `src/veracity/pipeline.py` — orchestrator
- `src/veracity/llm.py` — GitHub Models API wrapper
- `src/veracity/rendering.py` — CLI report display
- `src/veracity/cli.py` — chat loop entry point
- `schemas/` — exported JSON Schema
