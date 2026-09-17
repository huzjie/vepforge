# -*- coding: utf-8 -*-
"""指标收集器：计数器/计时器/直方图。"""
from __future__ import annotations

import threading
import time
from typing import Any, Dict, List


class MetricsCollector:
    """线程安全的轻量指标收集器，无外部依赖。"""

    def __init__(self):
        self._lock = threading.Lock()
        self._counters: Dict[str, int] = {}
        self._timings: Dict[str, List[float]] = {}
        self._gauges: Dict[str, float] = {}

    def incr(self, name: str, n: int = 1) -> None:
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + n

    def time(self, name: str):
        return _Timer(self, name)

    def gauge(self, name: str, value: float) -> None:
        with self._lock:
            self._gauges[name] = value

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            timings = {k: (sum(v) / len(v) if v else 0.0) for k, v in self._timings.items()}
            return {"counters": dict(self._counters),
                    "timings_avg": timings,
                    "gauges": dict(self._gauges)}

    def _record_timing(self, name: str, seconds: float) -> None:
        with self._lock:
            self._timings.setdefault(name, []).append(seconds)


class _Timer:
    def __init__(self, collector: MetricsCollector, name: str):
        self.collector = collector
        self.name = name
        self._start = 0.0

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.collector._record_timing(self.name, time.perf_counter() - self._start)
