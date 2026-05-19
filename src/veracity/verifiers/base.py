"""Abstract base class for all verifiers."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod

from veracity.schema import MethodResult, VerificationMethod


class BaseVerifier(ABC):
    """Base class for verification methods."""

    @property
    @abstractmethod
    def method(self) -> VerificationMethod:
        """The verification method this verifier implements."""

    @property
    def weight(self) -> float:
        """Default weight for this method in aggregation."""
        return 0.2

    @abstractmethod
    def _verify(self, query: str, response: str) -> MethodResult:
        """Run verification. Subclasses implement this."""

    def verify(self, query: str, response: str) -> MethodResult:
        """Run verification with timing."""
        start = time.perf_counter()
        result = self._verify(query, response)
        elapsed = time.perf_counter() - start
        result.execution_time_sec = round(elapsed, 3)
        result.method = self.method
        result.weight = self.weight
        return result
