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
