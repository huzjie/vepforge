# -*- coding: utf-8 -*-
"""CSV 工具：解析 CSV 并做基础聚合。"""
from __future__ import annotations

import csv
import io
from typing import Any, Dict, List

from .base import Tool, ToolResult


class CsvTool(Tool):
    name = "csv"
    description = "Parse CSV text and compute basic aggregate statistics."

    def run(self, inputs: Dict[str, Any]) -> ToolResult:
        text = inputs.get("text", "")
        try:
            reader = csv.DictReader(io.StringIO(text))
            rows = list(reader)
            cols = reader.fieldnames or []
            agg = {"rows": len(rows), "columns": cols}
            # 对数值列求均值
            for c in cols:
                nums = [float(r[c]) for r in rows if c in r and _is_num(r[c])]
                if nums:
                    agg[f"avg_{c}"] = round(sum(nums) / len(nums), 4)
            return ToolResult(True, exit_code=0, data=agg)
        except Exception as e:  # noqa: BLE001
            return ToolResult(False, exit_code=1, stderr=str(e))


def _is_num(s: str) -> bool:
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False
