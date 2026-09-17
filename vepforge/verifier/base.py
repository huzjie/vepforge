# -*- coding: utf-8 -*-
"""验证器基类。"""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..core.evidence import Evidence


class Verifier(ABC):
    """验证器接口：对一条 Evidence 做校验，返回标记 verified 后的 Evidence。"""

    name: str = "base"

    @abstractmethod
    def verify(self, evidence: Evidence) -> Evidence:
        """校验证据，返回更新 verified 标志后的同一证据。"""
