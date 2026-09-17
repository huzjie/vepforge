# -*- coding: utf-8 -*-
"""HTTP 状态验证器：2xx 视为通过。"""
from __future__ import annotations

from ..core.evidence import Evidence, EvidenceKind
from .base import Verifier


class HttpStatusVerifier(Verifier):
    name = "http_status"

    def verify(self, evidence: Evidence) -> Evidence:
        if evidence.kind != EvidenceKind.HTTP_STATUS:
            return evidence
        code = int(evidence.value)
        evidence.verified = 200 <= code < 300
        evidence.meta["verifier"] = self.name
        return evidence
