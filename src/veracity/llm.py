"""GitHub Models API wrapper using the openai SDK."""

from __future__ import annotations

import os

from openai import OpenAI


class LLMClient:
    """Thin wrapper around GitHub Models API (OpenAI-compatible)."""

    def __init__(
        self,
        model: str | None = None,
        base_url: str = "https://models.github.ai/inference",
        api_key: str | None = None,
    ):
        self.model = model or os.environ.get("VERACITY_MODEL", "openai/gpt-4o")
        token = api_key or os.environ.get("GITHUB_TOKEN", "")
        self._client = OpenAI(base_url=base_url, api_key=token)

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
