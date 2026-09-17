# -*- coding: utf-8 -*-
"""正则工具：对文本做正则提取。"""
from __future__ import annotations

import re
from typing import Any, Dict

from .base import Tool, ToolResult


class RegexTool(Tool):
    name = "regex"
    description = "Extract matches from text using a regex pattern."

    def run(self, inputs: Dict[str, Any]) -> ToolResult:
        text = inputs.get("text", "")
        pattern = inputs.get("pattern", "")
        try:
            matches = re.findall(pattern, text)
            return ToolResult(True, exit_code=0,
                              data={"matches": matches[:100], "count": len(matches)})
        except re.error as e:
            return ToolResult(False, exit_code=1, stderr=str(e))
