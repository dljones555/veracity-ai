"""Structural validation verifier — checks response structure and extracts claims."""

from __future__ import annotations

import re

from veracity.schema import MethodResult, VerificationMethod, VerificationStatus
from veracity.verifiers.base import BaseVerifier


class StructureVerifier(BaseVerifier):
    @property
    def method(self) -> VerificationMethod:
        return VerificationMethod.STRUCTURE_VALIDATION

    @property
    def weight(self) -> float:
        return 0.15

    def _verify(self, query: str, response: str) -> MethodResult:
        issues: list[str] = []
        details_parts: list[str] = []

        # Check response is non-empty
        if not response or not response.strip():
            return MethodResult(
                method=self.method,
                status=VerificationStatus.FAIL,
                certainty_contribution=0,
                weight=self.weight,
                execution_time_sec=0,
                details="Empty response",
            )

        # Check response length is reasonable
        word_count = len(response.split())
        details_parts.append(f"{word_count} words")

        if word_count < 3:
            issues.append("Response too short to verify")

        # Extract and count claims (sentences with factual assertions)
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]
        claim_count = 0
        for s in sentences:
            # Heuristic: sentences with numbers, percentages, or assertive language
            if re.search(r'\d|percent|always|never|every|all |most |causes?|prevents?|reduces?|increases?', s, re.IGNORECASE):
                claim_count += 1

        details_parts.append(f"{claim_count} claims detected")

        # Check for hedging language (good sign of honest AI)
        hedges = re.findall(r'\b(may|might|could|possibly|likely|approximately|about|roughly|generally)\b', response, re.IGNORECASE)
        if hedges:
            details_parts.append(f"{len(hedges)} hedge words")

        # Determine status
        if issues:
            status = VerificationStatus.WARN
            certainty = 40
        elif claim_count == 0:
            status = VerificationStatus.PASS
            certainty = 80
            details_parts.append("No factual claims to verify")
        else:
            status = VerificationStatus.PASS
            certainty = 70

        return MethodResult(
            method=self.method,
            status=status,
            certainty_contribution=certainty,
            weight=self.weight,
            execution_time_sec=0,
            details="; ".join(details_parts),
            conflicts=issues,
        )
