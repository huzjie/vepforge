# -*- coding: utf-8 -*-
"""哈希验证器：期望 sha256 与实际值匹配则通过。"""
from __future__ import annotations

import hashlib
from typing import Any

from ..core.evidence import Evidence, EvidenceKind
from .base import Verifier


class HashVerifier(Verifier):
    name = "hash"

    def verify(self, evidence: Evidence) -> Evidence:
        if evidence.kind != EvidenceKind.HASH:
            return evidence
        expected = evidence.meta.get("expected")
        if expected is None:
            # 无期望值时，仅校验格式合法（64 位 hex）
            evidence.verified = len(str(evidence.value)) == 64
        else:
            evidence.verified = str(evidence.value) == str(expected)
        evidence.meta["verifier"] = self.name
        return evidence


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
