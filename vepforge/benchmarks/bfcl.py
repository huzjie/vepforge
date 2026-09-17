# -*- coding: utf-8 -*-
"""BFCL：函数调用/工具使用基准。"""
from __future__ import annotations

from typing import Any, Dict, List

from .base import Benchmark


class BFCL(Benchmark):
    name = "bfcl"

    def tasks(self) -> List[Dict[str, Any]]:
        return [
            {"id": "bfcl-1", "goal": "call the correct tool for the query",
             "criteria": ["tool called"]},
            {"id": "bfcl-2", "goal": "chain two tools in correct order",
             "criteria": ["order correct"]},
        ]

    def score(self, result: Dict[str, Any], task: Dict[str, Any]) -> float:
        ev = result.get("evidences", [])
        return min(100.0, len(ev) * 50.0)
