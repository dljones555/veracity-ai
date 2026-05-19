"""CLI chat loop with verification reports."""

from __future__ import annotations

import argparse
from pathlib import Path
import os
import sys

from veracity.llm import LLMClient
from veracity.pipeline import VerificationPipeline
from veracity.rendering import render_report


SYSTEM_PROMPT_FILE = Path(__file__).resolve().parents[2] / "system_prompt.md"


def load_system_prompt(path: Path | None = None) -> str | None:
    """Load the system prompt text from an external file."""
    if path is None:
        path = SYSTEM_PROMPT_FILE
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Veracity AI chat with verification")
    parser.add_argument(
        "--system-prompt",
        type=Path,
        default=SYSTEM_PROMPT_FILE,
        help="Path to a system prompt file for the LLM.",
    )
    parser.add_argument(
        "--export-json",
        type=Path,
        help="Write the VeracityReport JSON to this file after each query.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the interactive chat loop with verification."""
    args = parse_args()
    system_prompt = load_system_prompt(args.system_prompt)

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token and not os.environ.get("OPENAI_API_KEY"):
        print("Warning: no API key found. LLM features will be limited.")
        print("Set OPENAI_API_KEY or GITHUB_TOKEN to enable model access.")
        print()

    try:
        llm = LLMClient() if token or os.environ.get("OPENAI_API_KEY") else None
    except Exception as e:
        print(f"Failed to initialize LLM client: {e}")
        llm = None

    pipeline = VerificationPipeline(llm_client=llm)

    print("Veracity AI - Chat with Verification")
    print("Type 'quit' or 'exit' to stop.\n")

    if system_prompt:
        print(f"Loaded system prompt from: {args.system_prompt}")
    else:
        print("No system prompt file found; using default model prompt.\n")

    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        # Get AI response
        if llm:
            try:
                response = llm.chat(query, system=system_prompt)
            except Exception as e:
                print(f"LLM error: {e}")
                continue
        else:
            response = f"[No LLM available] Echo: {query}"

        print(f"\nAI: {response}\n")

        # Run verification pipeline
        report = pipeline.run(query, response)
        print(render_report(report))

        if args.export_json:
            args.export_json.write_text(report.model_dump_json(indent=2), encoding="utf-8")
            print(f"JSON report saved to: {args.export_json}\n")

        print()


if __name__ == "__main__":
    main()
