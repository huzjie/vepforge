# -*- coding: utf-8 -*-
"""非空验证器：stdout 非空视为通过。"""
from __future__ import annotations

from ..core.evidence import Evidence, EvidenceKind
from .base import Verifier


class NonEmptyVerifier(Verifier):
    name = "nonempty"

    def verify(self, evidence: Evidence) -> Evidence:
        if evidence.kind != EvidenceKind.STDOUT:
            return evidence
        evidence.verified = bool(str(evidence.value).strip())
        evidence.meta["verifier"] = self.name
        return evidence
