"""Reasoning verifier — LLM chain-of-thought self-critique."""

from __future__ import annotations

from veracity.schema import MethodResult, VerificationMethod, VerificationStatus
from veracity.verifiers.base import BaseVerifier


class ReasoningVerifier(BaseVerifier):
    """Uses a second LLM call to critique the original response.

    Requires an LLM client to be injected. If no client is provided,
    the verifier is skipped.
    """

    def __init__(self, llm_client=None):
        self._llm = llm_client

    @property
    def method(self) -> VerificationMethod:
        return VerificationMethod.COT_REASONING

    @property
    def weight(self) -> float:
        return 0.20

    def _verify(self, query: str, response: str) -> MethodResult:
        if self._llm is None:
            return MethodResult(
                method=self.method,
                status=VerificationStatus.SKIP,
                certainty_contribution=0,
                weight=0.0,
                execution_time_sec=0,
                details="No LLM client available for reasoning verification",
            )

        critique_prompt = (
            "You are a fact-checking assistant. Analyze the following AI response "
            "for accuracy, logical consistency, and potential issues.\n\n"
            f"User question: {query}\n\n"
            f"AI response: {response}\n\n"
            "Provide a brief critique. Start with PASS, WARN, or FAIL followed by "
            "your analysis. Focus on factual accuracy and logical consistency."
        )

        try:
            critique = self._llm.chat(critique_prompt)
        except Exception as e:
            return MethodResult(
                method=self.method,
                status=VerificationStatus.SKIP,
                certainty_contribution=0,
                weight=0.0,
                execution_time_sec=0,
                details=f"LLM critique failed: {e}",
            )

        # Parse the critique response
        critique_lower = critique.lower().strip()
        conflicts: list[str] = []

        if critique_lower.startswith("fail"):
            status = VerificationStatus.FAIL
            certainty = 30
            conflicts.append(critique)
        elif critique_lower.startswith("warn"):
            status = VerificationStatus.WARN
            certainty = 60
            conflicts.append(critique)
        else:
            status = VerificationStatus.PASS
            certainty = 80

        return MethodResult(
            method=self.method,
            status=status,
            certainty_contribution=certainty,
            weight=self.weight,
            execution_time_sec=0,
            details=critique[:200],
            conflicts=conflicts,
        )
