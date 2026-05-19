"""LLM client wrapper supporting OpenAI-compatible endpoints."""

from __future__ import annotations

import os

from openai import OpenAI


class LLMClient:
    """Thin wrapper around OpenAI-compatible LLM endpoints."""

    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
    ):
        self.model = model or os.environ.get("VERACITY_MODEL", "openai/gpt-4o")
        self.base_url = (
            base_url
            or os.environ.get("VERACITY_BASE_URL")
            or "https://models.github.ai/inference"
        )
        self.api_key = api_key or os.environ.get("VERACITY_API_KEY")
        if not self.api_key:
            self.api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GITHUB_TOKEN")

        if not self.api_key:
            raise ValueError(
                "No API key found. Set OPENAI_API_KEY, VERACITY_API_KEY, or GITHUB_TOKEN."
            )

        self._client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def chat(self, prompt: str, system: str | None = None) -> str:
        """Send a single chat message and return the response text."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content or ""
