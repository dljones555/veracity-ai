"""Search verifier — cross-references claims against known facts (mocked for POC)."""

from __future__ import annotations

import re

from veracity.schema import MethodResult, VerificationMethod, VerificationStatus
from veracity.verifiers.base import BaseVerifier

# Mock knowledge base for POC — simulates web search results
KNOWN_FACTS: dict[str, dict[str, str | bool]] = {
    "bacon": {
        "fact": "Processed meat classified as Group 1 carcinogen by WHO/IARC",
        "healthy": False,
    },
    "avocado": {
        "fact": "Rich in monounsaturated fats, potassium, and fiber",
        "healthy": True,
    },
    "sourdough": {
        "fact": "Fermented bread with lower glycemic index than white bread",
        "healthy": True,
    },
    "keto": {
        "fact": "Low-carb high-fat diet; sourdough is not keto-friendly",
        "healthy": True,
    },
    "python": {
        "fact": "General-purpose programming language created by Guido van Rossum",
        "healthy": True,
    },
}


class SearchVerifier(BaseVerifier):
    """Cross-references response against a mock knowledge base.

    In production, this would call real search APIs.
    """

    def __init__(self, knowledge_base: dict | None = None):
        self._kb = knowledge_base if knowledge_base is not None else KNOWN_FACTS

    @property
    def method(self) -> VerificationMethod:
        return VerificationMethod.SEARCH_CROSS_REFERENCE

    @property
    def weight(self) -> float:
        return 0.30

    def _verify(self, query: str, response: str) -> MethodResult:
        text = (query + " " + response).lower()
        matches: list[str] = []
        conflicts: list[str] = []
        sources: list[str] = []

        for keyword, info in self._kb.items():
            if keyword in text:
                fact = str(info["fact"])
                matches.append(f"{keyword}: {fact}")
                sources.append(f"[mock] {fact}")

                # Check if response makes health claims that conflict
                if not info.get("healthy", True):
                    health_claims = re.findall(
                        rf'{keyword}[^.]*(?:healthy|nutritious|good for|beneficial)',
                        text,
                    )
                    if health_claims:
                        conflicts.append(
                            f"Response claims {keyword} is healthy, but: {fact}"
                        )

        if not matches:
            return MethodResult(
                method=self.method,
                status=VerificationStatus.SKIP,
                certainty_contribution=0,
                weight=0.0,
                execution_time_sec=0,
                details="No matching topics in knowledge base",
            )

        if conflicts:
            status = VerificationStatus.WARN
            certainty = max(30, 80 - len(conflicts) * 15)
        else:
            status = VerificationStatus.PASS
            certainty = 90

        return MethodResult(
            method=self.method,
            status=status,
            certainty_contribution=certainty,
            weight=self.weight,
            execution_time_sec=0,
            details=f"{len(matches)} topics cross-referenced",
            sources=sources,
            conflicts=conflicts,
        )
