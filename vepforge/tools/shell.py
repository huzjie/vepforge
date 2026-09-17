# -*- coding: utf-8 -*-
"""Shell 工具：在受控沙箱执行命令。"""
from __future__ import annotations

import subprocess
from typing import Any, Dict

from .base import Tool, ToolResult


class ShellTool(Tool):
    name = "shell"
    description = "Execute a shell command in a sandbox and capture exit code."

    def __init__(self, timeout: int = 30, allowlist: Any = None):
        self.timeout = timeout
        self.allowlist = allowlist or ["echo", "python", "ls", "cat", "pwd"]

    def run(self, inputs: Dict[str, Any]) -> ToolResult:
        cmd = inputs.get("command", "")
        if isinstance(cmd, str):
            cmd = cmd.split()
        if not cmd:
            return ToolResult(False, exit_code=2, stderr="empty command")
        if cmd[0] not in self.allowlist:
            return ToolResult(False, exit_code=2,
                              stderr=f"command not allowed: {cmd[0]}")
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=self.timeout, shell=False)
            return ToolResult(proc.returncode == 0, exit_code=proc.returncode,
                              stdout=proc.stdout, stderr=proc.stderr)
        except subprocess.TimeoutExpired as e:
            return ToolResult(False, exit_code=-1, stderr=f"timeout: {e}")
        except FileNotFoundError as e:
            return ToolResult(False, exit_code=-2, stderr=str(e))
