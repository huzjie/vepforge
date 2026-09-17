# -*- coding: utf-8 -*-
"""CyberGym：可执行环境下的任务基准。"""
from __future__ import annotations

from typing import Any, Dict, List

from .base import Benchmark


class CyberGym(Benchmark):
    name = "cybergym"

    def tasks(self) -> List[Dict[str, Any]]:
        return [
            {"id": "cyber-1", "goal": "run code in sandbox and verify exit code",
             "criteria": ["exit code 0"]},
            {"id": "cyber-2", "goal": "recover from a failing step",
             "criteria": ["recovered"]},
        ]

    def score(self, result: Dict[str, Any], task: Dict[str, Any]) -> float:
        status = result.get("status", "failed")
        if status in ("succeeded", "recovered"):
            return 100.0
        return 0.0
