# -*- coding: utf-8 -*-
"""DeepSearchQA：深度检索问答基准。"""
from __future__ import annotations

from typing import Any, Dict, List

from .base import Benchmark


class DeepSearchQA(Benchmark):
    name = "deepsearchqa"

    def tasks(self) -> List[Dict[str, Any]]:
        return [
            {"id": "dsq-1", "goal": "answer a multi-hop question with evidence",
             "criteria": ["answer produced", "evidence cited"]},
            {"id": "dsq-2", "goal": "verify a claim against retrieved sources",
             "criteria": ["verdict produced"]},
        ]

    def score(self, result: Dict[str, Any], task: Dict[str, Any]) -> float:
        artifacts = result.get("artifacts", [])
        return min(100.0, len(artifacts) * 40.0 + 20.0)
