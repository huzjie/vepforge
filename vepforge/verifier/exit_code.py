# -*- coding: utf-8 -*-
"""退出码验证器：exit_code == 0 视为通过。"""
from __future__ import annotations

from ..core.evidence import Evidence, EvidenceKind
from .base import Verifier


class ExitCodeVerifier(Verifier):
    name = "exit_code"

    def verify(self, evidence: Evidence) -> Evidence:
        if evidence.kind != EvidenceKind.EXIT_CODE:
            return evidence
        evidence.verified = int(evidence.value) == 0
        evidence.meta["verifier"] = self.name
        return evidence
