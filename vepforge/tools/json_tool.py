# -*- coding: utf-8 -*-
"""JSON 工具：解析/校验 JSON 并返回结构化证据。"""
from __future__ import annotations

import json
from typing import Any, Dict

from .base import Tool, ToolResult


class JsonTool(Tool):
    name = "json"
    description = "Parse and validate JSON, return normalized data."

    def run(self, inputs: Dict[str, Any]) -> ToolResult:
        text = inputs.get("text", "")
        try:
            data = json.loads(text)
            return ToolResult(True, exit_code=0, data={"parsed": data})
        except json.JSONDecodeError as e:
            return ToolResult(False, exit_code=1, stderr=str(e))
