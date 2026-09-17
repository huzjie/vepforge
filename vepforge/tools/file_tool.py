# -*- coding: utf-8 -*-
"""文件工具：读写文件并返回哈希证据。"""
from __future__ import annotations

import hashlib
import os
from typing import Any, Dict

from .base import Tool, ToolResult


class FileTool(Tool):
    name = "file"
    description = "Read/write a file under a sandbox root and return sha256."

    def __init__(self, root: str = ""):
        self.root = root or os.getcwd()

    def run(self, inputs: Dict[str, Any]) -> ToolResult:
        op = inputs.get("op", "read")
        path = inputs.get("path", "")
        full = os.path.join(self.root, path) if not os.path.isabs(path) else path
        try:
            if op == "read":
                with open(full, "r", encoding="utf-8") as f:
                    content = f.read()
                return ToolResult(True, exit_code=0, stdout=content[:8192],
                                  data={"sha256": hashlib.sha256(content.encode()).hexdigest()})
            if op == "write":
                content = inputs.get("content", "")
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "w", encoding="utf-8") as f:
                    f.write(content)
                return ToolResult(True, exit_code=0,
                                  data={"sha256": hashlib.sha256(content.encode()).hexdigest(),
                                        "path": full})
            return ToolResult(False, exit_code=2, stderr=f"unknown op: {op}")
        except OSError as e:
            return ToolResult(False, exit_code=1, stderr=str(e))
