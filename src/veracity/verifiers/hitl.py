"""Human-in-the-loop verifier — flags responses that need human review."""

from __future__ import annotations

from veracity.schema import (
    MethodResult,
    VerificationMethod,
    VerificationStatus,
)
from veracity.verifiers.base import BaseVerifier


class HITLVerifier(BaseVerifier):
    """Flags responses for human review based on prior verification results.

    This verifier runs last and examines the results from other verifiers
    to determine if human review is needed.
    """

    CERTAINTY_THRESHOLD = 70

    def __init__(self, prior_results: list[MethodResult] | None = None):
        self._prior_results = prior_results or []

    @property
    def method(self) -> VerificationMethod:
        return VerificationMethod.HUMAN_IN_THE_LOOP

    @property
    def weight(self) -> float:
        return 0.10

    def set_prior_results(self, results: list[MethodResult]) -> None:
        self._prior_results = results

    def _verify(self, query: str, response: str) -> MethodResult:
        reasons: list[str] = []

        # Check if any prior method failed
        failed = [r for r in self._prior_results if r.status == VerificationStatus.FAIL]
        if failed:
            methods = [r.method.value for r in failed]
            reasons.append(f"Failed checks: {', '.join(methods)}")

        # Check if any prior method has conflicts
        all_conflicts = []
        for r in self._prior_results:
            all_conflicts.extend(r.conflicts)
        if all_conflicts:
            reasons.append(f"{len(all_conflicts)} conflict(s) detected")

        # Check weighted certainty from prior results
        if self._prior_results:
            active = [r for r in self._prior_results if r.status != VerificationStatus.SKIP]
            if active:
                total_weight = sum(r.weight for r in active)
                if total_weight > 0:
                    weighted_cert = sum(
                        r.certainty_contribution * r.weight for r in active
                    ) / total_weight
                    if weighted_cert < self.CERTAINTY_THRESHOLD:
                        reasons.append(
                            f"Weighted certainty {weighted_cert:.0f}% below threshold {self.CERTAINTY_THRESHOLD}%"
                        )

        hitl_needed = len(reasons) > 0

        if hitl_needed:
            status = VerificationStatus.WARN
            certainty = 0  # HITL doesn't contribute to certainty itself
            details = "Human review recommended: " + "; ".join(reasons)
        else:
            status = VerificationStatus.PASS
            certainty = 0
            details = "No human review needed"

        return MethodResult(
            method=self.method,
            status=status,
            certainty_contribution=certainty,
            weight=0.0,  # HITL doesn't contribute to certainty score
            execution_time_sec=0,
            details=details,
            conflicts=reasons if hitl_needed else [],
        )
