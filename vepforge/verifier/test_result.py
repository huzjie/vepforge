# -*- coding: utf-8 -*-
"""测试结果验证器：passed 数 >= 0 且 failed == 0 视为通过。"""
from __future__ import annotations

from ..core.evidence import Evidence, EvidenceKind
from .base import Verifier


class TestResultVerifier(Verifier):
    name = "test_result"

    def verify(self, evidence: Evidence) -> Evidence:
        if evidence.kind != EvidenceKind.TEST_RESULT:
            return evidence
        v = evidence.value
        if isinstance(v, dict):
            failed = int(v.get("failed", 0))
            evidence.verified = failed == 0
        else:
            evidence.verified = False
        evidence.meta["verifier"] = self.name
        return evidence
