"""Verification graph schema — the verification standard."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SchemaVersion(str, Enum):
    V0_1_0 = "0.1.0"


class ClaimType(str, Enum):
    HEALTH = "health"
    FINANCIAL = "financial"
    LEGAL = "legal"
    TECHNICAL = "technical"
    SCIENTIFIC = "scientific"
    RECIPE = "recipe"
    GENERAL = "general"


class VerificationMethod(str, Enum):
    STRUCTURE_VALIDATION = "structure_validation"
    COMPUTE_VERIFICATION = "compute_verification"
    SEARCH_CROSS_REFERENCE = "search_cross_reference"
    COT_REASONING = "cot_reasoning"
    HUMAN_IN_THE_LOOP = "human_in_the_loop"


class VerificationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    SKIP = "skip"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MethodResult(BaseModel):
    """Result from a single verification method."""

    method: VerificationMethod
    status: VerificationStatus
    certainty_contribution: int = Field(ge=0, le=100)
    weight: float = Field(ge=0.0, le=1.0)
    execution_time_sec: float = Field(ge=0.0)
    details: str = ""
    sources: list[str] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)


class VerificationSummary(BaseModel):
    """Aggregated verification result."""

    overall_certainty: int = Field(ge=0, le=100)
    risk_level: RiskLevel
    conflicts: list[str] = Field(default_factory=list)
    hitl_required: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class VeracityReport(BaseModel):
    """Top-level verification graph document."""

    schema_version: SchemaVersion = SchemaVersion.V0_1_0
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    original_query: str
    ai_response: str
    claim_type: ClaimType
    methods_graph: list[MethodResult] = Field(default_factory=list)
    summary: VerificationSummary
    visual_text: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
