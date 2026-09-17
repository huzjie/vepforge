# -*- coding: utf-8 -*-
"""时间工具：返回当前时间戳（可验证）。"""
from __future__ import annotations

import time
from typing import Any, Dict

from .base import Tool, ToolResult


class TimeTool(Tool):
    name = "time"
    description = "Return current epoch / ISO time."

    def run(self, inputs: Dict[str, Any]) -> ToolResult:
        fmt = inputs.get("format", "iso")
        t = time.time()
        if fmt == "epoch":
            value = t
        else:
            value = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(t))
        return ToolResult(True, exit_code=0, data={"time": value, "epoch": t})
