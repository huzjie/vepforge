# -*- coding: utf-8 -*-
"""Schema 验证器：校验证据 value 为合法 JSON 结构。"""
from __future__ import annotations

import json

from ..core.evidence import Evidence, EvidenceKind
from .base import Verifier


class SchemaVerifier(Verifier):
    name = "schema"

    def verify(self, evidence: Evidence) -> Evidence:
        if evidence.kind != EvidenceKind.FILE:
            return evidence
        value = evidence.value
        if isinstance(value, str):
            try:
                json.loads(value)
                evidence.verified = True
            except json.JSONDecodeError:
                evidence.verified = False
        else:
            evidence.verified = isinstance(value, (dict, list))
        evidence.meta["verifier"] = self.name
        return evidence
