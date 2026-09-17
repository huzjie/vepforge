# -*- coding: utf-8 -*-
"""工具基类与结果结构。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ToolResult:
    """工具执行结果，exit_code/stdout/stderr 均可作为证据。"""

    ok: bool
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok, "exit_code": self.exit_code,
            "stdout": self.stdout, "stderr": self.stderr, "data": self.data,
        }


class Tool(ABC):
    """可验证工具：run(inputs) 返回 ToolResult。"""

    name: str = "tool"
    description: str = ""

    @abstractmethod
    def run(self, inputs: Dict[str, Any]) -> ToolResult:
        """执行工具，返回结构化结果。"""
