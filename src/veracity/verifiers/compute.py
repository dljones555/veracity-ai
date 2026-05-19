"""Compute verifier — checks numerical claims for consistency."""

from __future__ import annotations

import re

from veracity.schema import MethodResult, VerificationMethod, VerificationStatus
from veracity.verifiers.base import BaseVerifier


class ComputeVerifier(BaseVerifier):
    @property
    def method(self) -> VerificationMethod:
        return VerificationMethod.COMPUTE_VERIFICATION

    @property
    def weight(self) -> float:
        return 0.25

    def _verify(self, query: str, response: str) -> MethodResult:
        # Extract numbers from the response
        numbers = re.findall(r'-?\d+\.?\d*', response)
        numbers = [float(n) for n in numbers]

        if not numbers:
            return MethodResult(
                method=self.method,
                status=VerificationStatus.SKIP,
                certainty_contribution=0,
                weight=0.0,  # No weight if skipped
                execution_time_sec=0,
                details="No numerical claims found",
            )

        issues: list[str] = []

        # Check for obviously wrong numbers
        for n in numbers:
            if n < 0 and re.search(r'calorie|price|cost|weight|height|age|temperature', response, re.IGNORECASE):
                issues.append(f"Suspicious negative value: {n}")

        # Check percentage claims are in valid range
        pct_matches = re.findall(r'(\d+\.?\d*)\s*%', response)
        for p in pct_matches:
            val = float(p)
            if val > 100:
                issues.append(f"Percentage exceeds 100%: {val}%")

        # Check if numbers that should sum up actually do
        # Look for patterns like "X + Y = Z" or listing with a total
        sum_pattern = re.findall(r'(\d+\.?\d*)\s*\+\s*(\d+\.?\d*)\s*=\s*(\d+\.?\d*)', response)
        for a, b, c in sum_pattern:
            expected = float(a) + float(b)
            actual = float(c)
            if abs(expected - actual) > 0.01:
                issues.append(f"Arithmetic error: {a} + {b} = {c} (expected {expected})")

        details = f"{len(numbers)} numbers found"
        if issues:
            status = VerificationStatus.FAIL
            certainty = max(20, 80 - len(issues) * 20)
            details += "; " + "; ".join(issues)
        else:
            status = VerificationStatus.PASS
            certainty = 85
            details += "; no inconsistencies detected"

        return MethodResult(
            method=self.method,
            status=status,
            certainty_contribution=certainty,
            weight=self.weight,
            execution_time_sec=0,
            details=details,
            conflicts=issues,
        )
