"""Test suite for Veracity AI."""

import pytest


def test_schema_imports():
    """Test that schema module imports correctly."""
    from veracity.schema import ClaimType, VerificationMethod, VerificationStatus
    
    assert ClaimType.HEALTH.value == "health"
    assert VerificationMethod.STRUCTURE_VALIDATION.value == "structure_validation"
    assert VerificationStatus.PASS.value == "pass"


def test_version():
    """Test that version is accessible."""
    from veracity import __version__
    
    assert __version__ == "0.1.0"


def test_pipeline_initialization():
    """Test that pipeline can be initialized."""
    from veracity.pipeline import VerificationPipeline
    
    pipeline = VerificationPipeline(llm_client=None)
    assert pipeline is not None


def test_llm_client_import():
    """Test that LLM client can be imported."""
    from veracity.llm import LLMClient
    
    assert LLMClient is not None


def test_system_prompt_load():
    """Test that the external system prompt can be loaded."""
    from pathlib import Path
    from veracity.cli import load_system_prompt

    prompt_path = Path(__file__).resolve().parents[1] / "system_prompt.md"
    prompt = load_system_prompt(prompt_path)

    assert prompt is not None
    assert "verification agent" in prompt.lower()


def test_report_json_serialization():
    """Test that VeracityReport serializes to valid JSON."""
    from veracity.schema import VeracityReport, VerificationSummary, MethodResult, ClaimType, VerificationStatus, RiskLevel
    import json

    report = VeracityReport(
        original_query="Is bacon avocado toast healthy?",
        ai_response="It has both healthy fats and processed meat.",
        claim_type=ClaimType.RECIPE,
        methods_graph=[
            MethodResult(
                method="structure_validation",
                status=VerificationStatus.PASS,
                certainty_contribution=80,
                weight=0.5,
                execution_time_sec=0.1,
                details="Mocked verification",
            )
        ],
        summary=VerificationSummary(
            overall_certainty=80,
            risk_level=RiskLevel.MEDIUM,
        ),
        visual_text="[S 0.1s 80%+] -> 80% OK",
    )

    json_text = report.model_dump_json(indent=2)
    parsed = json.loads(json_text)

    assert parsed["claim_type"] == "recipe"
    assert parsed["summary"]["overall_certainty"] == 80
