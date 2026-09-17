# -*- coding: utf-8 -*-
"""基准基类。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Benchmark(ABC):
    name: str = "benchmark"

    @abstractmethod
    def tasks(self) -> List[Dict[str, Any]]:
        """返回任务列表。"""

    @abstractmethod
    def score(self, result: Dict[str, Any], task: Dict[str, Any]) -> float:
        """对单个任务结果打分。"""
