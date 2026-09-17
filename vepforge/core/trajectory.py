# -*- coding: utf-8 -*-
"""Trajectory：智能体轨迹。"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class StepRole(str, Enum):
    """轨迹步骤角色。"""
    THOUGHT = "thought"
    ACTION = "action"
    OBSERVATION = "observation"
    ARTIFACT = "artifact"
    EVIDENCE = "evidence"
    REFLECTION = "reflection"
    ERROR = "error"


@dataclass
class Step:
    """轨迹中的单步记录，任何动作/观察/产物/证据都落一条。"""

    role: StepRole
    content: Any
    step_index: int = 0
    timestamp: float = field(default_factory=time.time)
    step_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "role": self.role.value,
            "content": self.content,
            "step_index": self.step_index,
            "timestamp": self.timestamp,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Step":
        return cls(
            role=StepRole(d["role"]),
            content=d["content"],
            step_index=d.get("step_index", 0),
            timestamp=d.get("timestamp", time.time()),
            step_id=d.get("step_id", uuid.uuid4().hex[:12]),
            meta=d.get("meta", {}),
        )


@dataclass
class Trajectory:
    """一个任务的完整轨迹序列，支持回溯、切片、按角色过滤。"""

    task_id: str
    steps: List[Step] = field(default_factory=list)

    def add(self, role: StepRole, content: Any, meta: Optional[Dict[str, Any]] = None) -> Step:
        step = Step(
            role=role,
            content=content,
            step_index=len(self.steps),
            meta=meta or {},
        )
        self.steps.append(step)
        return step

    def by_role(self, role: StepRole) -> List[Step]:
        return [s for s in self.steps if s.role == role]

    def last(self) -> Optional[Step]:
        return self.steps[-1] if self.steps else None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "steps": [s.to_dict() for s in self.steps],
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Trajectory":
        return cls(
            task_id=d["task_id"],
            steps=[Step.from_dict(s) for s in d.get("steps", [])],
        )

    def __len__(self) -> int:
        return len(self.steps)
