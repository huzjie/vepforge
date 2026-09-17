# -*- coding: utf-8 -*-
"""Python 执行工具：在子进程执行代码片段。"""
from __future__ import annotations

import subprocess
import sys
from typing import Any, Dict

from .base import Tool, ToolResult


class PythonExecTool(Tool):
    name = "python"
    description = "Execute a Python snippet in a subprocess and capture output."

    def __init__(self, timeout: int = 30, python: str = "python"):
        self.timeout = timeout
        self.python = python

    def run(self, inputs: Dict[str, Any]) -> ToolResult:
        code = inputs.get("code", "")
        if not code.strip():
            return ToolResult(False, exit_code=2, stderr="empty code")
        try:
            proc = subprocess.run(
                [self.python, "-c", code],
                capture_output=True, text=True, timeout=self.timeout,
            )
            return ToolResult(proc.returncode == 0, exit_code=proc.returncode,
                              stdout=proc.stdout, stderr=proc.stderr)
        except subprocess.TimeoutExpired as e:
            return ToolResult(False, exit_code=-1, stderr=f"timeout: {e}")
