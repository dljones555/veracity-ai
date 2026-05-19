"""Verification pipeline — orchestrates verifiers and aggregates results."""

from __future__ import annotations

from veracity.schema import (
    ClaimType,
    MethodResult,
    RiskLevel,
    VeracityReport,
    VerificationStatus,
    VerificationSummary,
)
from veracity.verifiers.base import BaseVerifier
from veracity.verifiers.compute import ComputeVerifier
from veracity.verifiers.hitl import HITLVerifier
from veracity.verifiers.reasoning import ReasoningVerifier
from veracity.verifiers.search import SearchVerifier
from veracity.verifiers.structure import StructureVerifier


# Icons for visual_text rendering
METHOD_ICONS: dict[str, str] = {
    "structure_validation": "S",
    "compute_verification": "#",
    "search_cross_reference": "?",
    "cot_reasoning": "*",
    "human_in_the_loop": "@",
}


def classify_claim(query: str) -> ClaimType:
    """Simple keyword-based claim classification."""
    q = query.lower()
    if any(w in q for w in ("recipe", "cook", "ingredient", "meal", "food", "eat")):
        return ClaimType.RECIPE
    if any(w in q for w in ("health", "medical", "symptom", "disease", "drug", "medicine")):
        return ClaimType.HEALTH
    if any(w in q for w in ("invest", "stock", "money", "finance", "tax", "budget")):
        return ClaimType.FINANCIAL
    if any(w in q for w in ("law", "legal", "court", "rights", "regulation")):
        return ClaimType.LEGAL
    if any(w in q for w in ("code", "programming", "software", "api", "bug", "deploy")):
        return ClaimType.TECHNICAL
    if any(w in q for w in ("study", "research", "hypothesis", "experiment", "peer")):
        return ClaimType.SCIENTIFIC
    return ClaimType.GENERAL


def compute_certainty(results: list[MethodResult]) -> int:
    """Compute weighted certainty score from method results."""
    active = [r for r in results if r.status != VerificationStatus.SKIP and r.weight > 0]
    if not active:
        return 50  # Default when no verifiers ran

    total_weight = sum(r.weight for r in active)
    if total_weight == 0:
        return 50

    weighted = sum(r.certainty_contribution * r.weight for r in active) / total_weight
    return round(weighted)


def determine_risk(certainty: int, results: list[MethodResult]) -> RiskLevel:
    """Determine risk level from certainty and results."""
    has_failures = any(r.status == VerificationStatus.FAIL for r in results)
    all_conflicts = []
    for r in results:
        all_conflicts.extend(r.conflicts)

    if has_failures or certainty < 40:
        return RiskLevel.CRITICAL
    if certainty < 60 or len(all_conflicts) > 2:
        return RiskLevel.HIGH
    if certainty < 80 or all_conflicts:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def build_visual_text(results: list[MethodResult], certainty: int) -> str:
    """Build the ASCII visual summary line."""
    parts = []
    for r in results:
        if r.status == VerificationStatus.SKIP:
            continue
        icon = METHOD_ICONS.get(r.method.value, "?")
        status_char = {
            VerificationStatus.PASS: "+",
            VerificationStatus.FAIL: "!",
            VerificationStatus.WARN: "~",
        }.get(r.status, "?")
        parts.append(f"[{icon} {r.execution_time_sec:.1f}s {r.certainty_contribution}%{status_char}]")

    check = "OK" if certainty >= 70 else "!!"
    arrow = " -> " if parts else ""
    return f"{' -> '.join(parts)}{arrow}{certainty}% {check}"


class VerificationPipeline:
    """Runs all verifiers and produces a VeracityReport."""

    def __init__(self, verifiers: list[BaseVerifier] | None = None, llm_client=None):
        if verifiers is not None:
            self._verifiers = verifiers
        else:
            self._verifiers = [
                StructureVerifier(),
                ComputeVerifier(),
                SearchVerifier(),
                ReasoningVerifier(llm_client=llm_client),
                HITLVerifier(),
            ]

    def run(self, query: str, response: str) -> VeracityReport:
        """Execute the full verification pipeline."""
        claim_type = classify_claim(query)
        results: list[MethodResult] = []

        for verifier in self._verifiers:
            # HITL verifier needs prior results
            if isinstance(verifier, HITLVerifier):
                verifier.set_prior_results(results)
            result = verifier.verify(query, response)
            results.append(result)

        certainty = compute_certainty(results)
        risk = determine_risk(certainty, results)

        all_conflicts = []
        for r in results:
            all_conflicts.extend(r.conflicts)

        hitl_result = next(
            (r for r in results if r.method.value == "human_in_the_loop"), None
        )
        hitl_required = hitl_result is not None and hitl_result.status == VerificationStatus.WARN

        summary = VerificationSummary(
            overall_certainty=certainty,
            risk_level=risk,
            conflicts=all_conflicts,
            hitl_required=hitl_required,
        )

        visual = build_visual_text(results, certainty)

        return VeracityReport(
            original_query=query,
            ai_response=response,
            claim_type=claim_type,
            methods_graph=results,
            summary=summary,
            visual_text=visual,
        )
