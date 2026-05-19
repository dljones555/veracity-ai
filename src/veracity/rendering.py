"""CLI report rendering — displays verification results in the terminal."""

from __future__ import annotations

from veracity.schema import RiskLevel, VeracityReport, VerificationStatus


# Status symbols (ASCII-safe)
STATUS_SYMBOLS: dict[VerificationStatus, str] = {
    VerificationStatus.PASS: "[PASS]",
    VerificationStatus.FAIL: "[FAIL]",
    VerificationStatus.WARN: "[WARN]",
    VerificationStatus.SKIP: "[SKIP]",
}

RISK_LABELS: dict[RiskLevel, str] = {
    RiskLevel.LOW: "LOW",
    RiskLevel.MEDIUM: "MEDIUM",
    RiskLevel.HIGH: "HIGH",
    RiskLevel.CRITICAL: "CRITICAL",
}

METHOD_NAMES: dict[str, str] = {
    "structure_validation": "Structure",
    "compute_verification": "Compute",
    "search_cross_reference": "Search",
    "cot_reasoning": "Reasoning",
    "human_in_the_loop": "HITL",
}


def render_report(report: VeracityReport) -> str:
    """Render a VeracityReport as a CLI-friendly string."""
    lines: list[str] = []
    sep = "-" * 50

    lines.append(sep)
    lines.append("VERACITY REPORT")
    lines.append(sep)
    lines.append(f"Claim type: {report.claim_type.value}")
    lines.append(f"Certainty:  {report.summary.overall_certainty}%")
    lines.append(f"Risk level: {RISK_LABELS[report.summary.risk_level]}")
    lines.append("")

    # Methods graph
    lines.append("Verification Methods:")
    for m in report.methods_graph:
        name = METHOD_NAMES.get(m.method.value, m.method.value)
        sym = STATUS_SYMBOLS[m.status]
        line = f"  {sym} {name:<12} {m.certainty_contribution:>3}% ({m.execution_time_sec:.2f}s)"
        if m.details:
            line += f" - {m.details}"
        lines.append(line)

    # Conflicts
    if report.summary.conflicts:
        lines.append("")
        lines.append("Conflicts:")
        for c in report.summary.conflicts:
            lines.append(f"  ! {c}")

    # HITL
    if report.summary.hitl_required:
        lines.append("")
        lines.append(">> Human review recommended <<")

    # Visual summary
    lines.append("")
    lines.append(report.visual_text)
    lines.append(sep)

    return "\n".join(lines)
