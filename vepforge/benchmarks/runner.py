# -*- coding: utf-8 -*-
"""BenchmarkRunner：统一跑基准并汇总。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..core.task import Task
from .base import Benchmark


class BenchmarkRunner:
    """对一组基准跑完整 pipeline，输出逐任务分数与总分。"""

    def __init__(self, pipeline, benchmarks: Optional[List[Benchmark]] = None):
        self.pipeline = pipeline
        self.benchmarks = benchmarks or []

    def run(self) -> Dict[str, Any]:
        report = {"benchmarks": {}, "overall": 0.0, "tasks": []}
        total = 0.0
        count = 0
        for bench in self.benchmarks:
            scores = []
            for t in bench.tasks():
                task = Task(goal=t["goal"],
                            acceptance_criteria=t.get("criteria", []))
                exp = self.pipeline.run(task)
                s = bench.score(exp.to_dict(), t)
                scores.append(s)
                report["tasks"].append({"benchmark": bench.name, "task_id": t["id"],
                                        "score": s, "status": exp.status.value})
                total += s
                count += 1
            avg = sum(scores) / len(scores) if scores else 0.0
            report["benchmarks"][bench.name] = avg
        report["overall"] = total / count if count else 0.0
        return report
