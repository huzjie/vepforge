# -*- coding: utf-8 -*-
"""Task：任务目标定义。"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TaskStatus(str, Enum):
    """任务生命周期。"""
    PENDING = "pending"
    RUNNING = "running"
    ANALYZE = "analyze"
    CODE = "code"
    EXECUTE = "execute"
    REFLECT = "reflect"
    ANALYZING = "analyzing"
    CODING = "coding"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    RECOVERED = "recovered"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """一个可验证的长程任务目标。

    goal 必须是可执行的、有明确验收标准的自然语言目标。
    constraints 是可选的硬约束（资源、安全、格式等）。
    acceptance_criteria 是完成判据，供复盘阶段（reflect）评估。
    """

    goal: str
    constraints: Optional[List[str]] = field(default_factory=list)
    acceptance_criteria: Optional[List[str]] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    task_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    status: TaskStatus = TaskStatus.PENDING
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    max_steps: int = 32
    timeout_seconds: float = 600.0

    def mark(self, status: TaskStatus) -> "Task":
        self.status = status
        now = time.time()
        if status == TaskStatus.RUNNING and self.started_at is None:
            self.started_at = now
        if status in (TaskStatus.SUCCEEDED, TaskStatus.FAILED,
                      TaskStatus.RECOVERED, TaskStatus.CANCELLED):
            self.finished_at = now
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "goal": self.goal,
            "constraints": self.constraints,
            "acceptance_criteria": self.acceptance_criteria,
            "context": self.context,
            "metadata": self.metadata,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "max_steps": self.max_steps,
            "timeout_seconds": self.timeout_seconds,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Task":
        t = cls(
            goal=d["goal"],
            constraints=d.get("constraints", []),
            acceptance_criteria=d.get("acceptance_criteria", []),
            context=d.get("context", {}),
            metadata=d.get("metadata", {}),
            task_id=d.get("task_id", uuid.uuid4().hex[:16]),
            status=TaskStatus(d.get("status", "pending")),
            max_steps=d.get("max_steps", 32),
            timeout_seconds=d.get("timeout_seconds", 600.0),
        )
        t.created_at = d.get("created_at", t.created_at)
        t.started_at = d.get("started_at")
        t.finished_at = d.get("finished_at")
        return t
