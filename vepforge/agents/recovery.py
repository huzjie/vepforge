# -*- coding: utf-8 -*-
"""失败恢复策略：重试 / 回退。"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional


class RecoveryPolicy(ABC):
    """恢复策略接口。"""

    name: str = "policy"

    @abstractmethod
    def run(self, fn: Callable[[], Any], *args, **kwargs) -> Any:
        """执行 fn，失败时按策略恢复。"""


class RetryRecovery(RecoveryPolicy):
    name = "retry"

    def __init__(self, max_retries: int = 3, backoff: float = 0.5):
        self.max_retries = max_retries
        self.backoff = backoff

    def run(self, fn: Callable[[], Any], *args, **kwargs) -> Any:
        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                return fn(*args, **kwargs)
            except Exception as e:  # noqa: BLE001
                last_exc = e
                if attempt < self.max_retries:
                    time.sleep(self.backoff * (2 ** attempt))
        raise RuntimeError(f"retry exhausted after {self.max_retries} retries") from last_exc


class FallbackRecovery(RecoveryPolicy):
    name = "fallback"

    def __init__(self, fallback: Callable[[], Any]):
        self.fallback = fallback

    def run(self, fn: Callable[[], Any], *args, **kwargs) -> Any:
        try:
            return fn(*args, **kwargs)
        except Exception:  # noqa: BLE001
            return self.fallback()
