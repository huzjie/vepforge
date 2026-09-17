# -*- coding: utf-8 -*-
"""Evidence：外部证据（工具真实执行结果）。"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class EvidenceKind(str, Enum):
    EXIT_CODE = "exit_code"
    STDOUT = "stdout"
    STDERR = "stderr"
    HASH = "hash"
    HTTP_STATUS = "http_status"
    FILE = "file"
    TEST_RESULT = "test_result"
    BENCH_SCORE = "bench_score"


@dataclass
class Evidence:
    """一条可验证的外部证据，来自工具在真实环境的执行结果。

    verified=True 表示证据已被验证器校验通过（如 exit_code==0、
    sha256 匹配、HTTP 200 等）。verifiable 表示该证据类型本身可校验。
    """

    kind: EvidenceKind
    value: Any
    tool: str
    verified: bool = False
    verifiable: bool = True
    evidence_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    created_at: float = field(default_factory=time.time)
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "kind": self.kind.value,
            "value": self.value,
            "tool": self.tool,
            "verified": self.verified,
            "verifiable": self.verifiable,
            "created_at": self.created_at,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Evidence":
        return cls(
            kind=EvidenceKind(d["kind"]),
            value=d["value"],
            tool=d["tool"],
            verified=d.get("verified", False),
            verifiable=d.get("verifiable", True),
            evidence_id=d.get("evidence_id", uuid.uuid4().hex[:12]),
            created_at=d.get("created_at", time.time()),
            meta=d.get("meta", {}),
        )
