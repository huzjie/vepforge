# -*- coding: utf-8 -*-
"""Experience：一次完整任务的可验证经验记录。"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .artifact import Artifact
from .evidence import Evidence
from .task import Task, TaskStatus
from .trajectory import Trajectory


class ExperienceStatus(str, Enum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    RECOVERED = "recovered"
    VERIFIED = "verified"


@dataclass
class Experience:
    """一次任务执行的完整经验：目标 + 轨迹 + 产物 + 证据 四者连接。

    这是 VEP（Verifiable Experience Pipeline）的核心数据结构——
    把任务目标、智能体轨迹、中间产物、外部证据连接成一个可审计、
    可回放、可验证的整体。
    """

    task: Task
    trajectory: Trajectory
    artifacts: List[Artifact] = field(default_factory=list)
    evidences: List[Evidence] = field(default_factory=list)
    status: ExperienceStatus = ExperienceStatus.RUNNING
    experience_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    created_at: float = field(default_factory=time.time)
    finished_at: Optional[float] = None
    score: Optional[float] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def add_artifact(self, a: Artifact) -> None:
        self.artifacts.append(a)

    def add_evidence(self, e: Evidence) -> None:
        self.evidences.append(e)

    def verified_evidence_count(self) -> int:
        return sum(1 for e in self.evidences if e.verified)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experience_id": self.experience_id,
            "task": self.task.to_dict(),
            "trajectory": self.trajectory.to_dict(),
            "artifacts": [a.to_dict() for a in self.artifacts],
            "evidences": [e.to_dict() for e in self.evidences],
            "status": self.status.value,
            "created_at": self.created_at,
            "finished_at": self.finished_at,
            "score": self.score,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Experience":
        exp = cls(
            task=Task.from_dict(d["task"]),
            trajectory=Trajectory.from_dict(d["trajectory"]),
            status=ExperienceStatus(d.get("status", "running")),
            experience_id=d.get("experience_id", uuid.uuid4().hex[:16]),
            created_at=d.get("created_at", time.time()),
            finished_at=d.get("finished_at"),
            score=d.get("score"),
            meta=d.get("meta", {}),
        )
        exp.artifacts = [Artifact.from_dict(a) for a in d.get("artifacts", [])]
        exp.evidences = [Evidence.from_dict(e) for e in d.get("evidences", [])]
        return exp
