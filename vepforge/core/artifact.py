# -*- coding: utf-8 -*-
"""Artifact：可寻址的中间产物。"""
from __future__ import annotations

import hashlib
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class ArtifactKind(str, Enum):
    CODE = "code"
    DATA = "data"
    REPORT = "report"
    LOG = "log"
    IMAGE = "image"
    MODEL = "model"
    TEXT = "text"
    BINARY = "binary"


@dataclass
class Artifact:
    """一次任务产出的中间产物，内容可寻址（sha256）。"""

    name: str
    kind: ArtifactKind
    content: str
    sha256: str = ""
    artifact_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    created_at: float = field(default_factory=time.time)
    meta: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.sha256:
            self.sha256 = hashlib.sha256(self.content.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "name": self.name,
            "kind": self.kind.value,
            "content": self.content,
            "sha256": self.sha256,
            "created_at": self.created_at,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Artifact":
        a = cls(
            name=d["name"],
            kind=ArtifactKind(d["kind"]),
            content=d["content"],
            sha256=d.get("sha256", ""),
            artifact_id=d.get("artifact_id", uuid.uuid4().hex[:12]),
            created_at=d.get("created_at", time.time()),
            meta=d.get("meta", {}),
        )
        return a
