# -*- coding: utf-8 -*-
"""追踪器：记录嵌套 span。"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Trace:
    name: str
    start: float
    end: Optional[float] = None
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    attrs: Dict[str, Any] = field(default_factory=dict)
    children: List["Trace"] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        end = self.end or time.time()
        return (end - self.start) * 1000.0

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "trace_id": self.trace_id,
                "duration_ms": self.duration_ms, "attrs": self.attrs,
                "children": [c.to_dict() for c in self.children]}


class Tracer:
    """简单 span 追踪器。"""

    def __init__(self):
        self._stack: List[Trace] = []
        self._roots: List[Trace] = []

    def start(self, name: str, **attrs) -> Trace:
        t = Trace(name=name, start=time.time(), attrs=attrs)
        if self._stack:
            self._stack[-1].children.append(t)
        else:
            self._roots.append(t)
        self._stack.append(t)
        return t

    def end(self) -> Optional[Trace]:
        if not self._stack:
            return None
        t = self._stack.pop()
        t.end = time.time()
        return t

    def to_dict(self) -> Dict[str, Any]:
        return {"traces": [r.to_dict() for r in self._roots]}
