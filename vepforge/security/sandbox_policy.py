# -*- coding: utf-8 -*-
"""沙箱策略：约束可执行命令与网络。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class SandboxPolicy:
    """定义沙箱白名单与能力开关。"""

    allowed_commands: Set[str] = field(default_factory=lambda: {"echo", "python", "ls", "cat", "pwd"})
    allow_network: bool = False
    max_runtime_seconds: int = 60
    max_output_bytes: int = 65536

    def allows_command(self, cmd: str) -> bool:
        return cmd in self.allowed_commands

    def to_dict(self):
        return {
            "allowed_commands": sorted(self.allowed_commands),
            "allow_network": self.allow_network,
            "max_runtime_seconds": self.max_runtime_seconds,
            "max_output_bytes": self.max_output_bytes,
        }
