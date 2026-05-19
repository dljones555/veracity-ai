# Veracity AI Backlog

This backlog breaks the next improvements into small, incremental steps.

## Goal
Build a sharable, agent-friendly verification graph with JSON export, system prompt guidance, and clear docs.

## Priority tasks

1. Fix GitHub status and docs
   - Update README badges to the correct repo and workflow path
   - Add a concise badge-driven status section
   - Make the README example less abstract and more visual

2. Add external system prompt support
   - Create `system_prompt.md`
   - Load prompt text from disk in `src/veracity/cli.py`
   - Use the loaded prompt as the system instruction for the LLM
   - Provide a concrete recipe example plus 1-2 other verification cases

3. Make the LLM client more generic
   - Support `VERACITY_BASE_URL` and generic `OPENAI_API_KEY` in addition to `GITHUB_TOKEN`
   - Keep GitHub Models API compatibility but avoid GitHub-only hardcoding

4. Export VeracityReport as JSON
   - Use Pydantic JSON serialization for reports
   - Add an optional CLI flag or env var to write JSON to disk
   - Document the JSON export format in README

5. Improve docs with spec-derived examples
   - Add a quick start example from the spec
   - Highlight recipe verification and web/source verification
   - Add a compact, visual verification graph example

6. Add tests for the new behavior
   - Test system prompt loading
   - Test JSON export output shape
   - Verify LLM client initialization with generic env vars

## Later improvements

- Add export to Markdown for reports
- Add richer agent planning examples for unit tests/lint/evals
- Add hooks for tool execution provenance
- Add a `veracity report serve` or `verify --json` command
