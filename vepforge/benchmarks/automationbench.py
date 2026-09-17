# -*- coding: utf-8 -*-
"""AutomationBench：长程任务自动化基准。"""
from __future__ import annotations

from typing import Any, Dict, List

from .base import Benchmark


class AutomationBench(Benchmark):
    name = "automationbench"

    def tasks(self) -> List[Dict[str, Any]]:
        return [
            {"id": "auto-1", "goal": "aggregate three CSV files and write a summary",
             "criteria": ["summary file produced", "exit code 0"]},
            {"id": "auto-2", "goal": "run a batch job and verify outputs",
             "criteria": ["job finished", "evidence verified"]},
            {"id": "auto-3", "goal": "fetch a page and extract key facts",
             "criteria": ["http 200", "facts extracted"]},
        ]

    def score(self, result: Dict[str, Any], task: Dict[str, Any]) -> float:
        status = result.get("status", "failed")
        if status == "succeeded":
            return 100.0
        if status == "recovered":
            return 75.0
        return 0.0
