"""CLI chat loop with verification reports."""

from __future__ import annotations

import os
import sys

from veracity.llm import LLMClient
from veracity.pipeline import VerificationPipeline
from veracity.rendering import render_report


def main() -> None:
    """Run the interactive chat loop with verification."""
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("Warning: GITHUB_TOKEN not set. LLM features will be limited.")
        print("Set it with: export GITHUB_TOKEN=your_token")
        print()

    try:
        llm = LLMClient() if token else None
    except Exception as e:
        print(f"Failed to initialize LLM client: {e}")
        llm = None

    pipeline = VerificationPipeline(llm_client=llm)

    print("Veracity AI - Chat with Verification")
    print("Type 'quit' or 'exit' to stop.\n")

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
                response = llm.chat(
                    query,
                    system="You are a helpful assistant. Provide accurate, detailed answers.",
                )
            except Exception as e:
                print(f"LLM error: {e}")
                continue
        else:
            response = f"[No LLM available] Echo: {query}"

        print(f"\nAI: {response}\n")

        # Run verification pipeline
        report = pipeline.run(query, response)
        print(render_report(report))
        print()


if __name__ == "__main__":
    main()
