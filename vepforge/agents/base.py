# -*- coding: utf-8 -*-
"""智能体基类。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Agent(ABC):
    """所有智能体的基类，共享 llm 引用与 name 标识。"""

    name: str = "agent"

    def __init__(self, llm=None):
        self.llm = llm

    @abstractmethod
    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行一次动作，返回结构化结果。"""

    def _llm_call(self, prompt: str, default: Any = None) -> Any:
        if self.llm is None:
            return default
        try:
            return self.llm.complete(prompt)
        except Exception:  # noqa: BLE001
            return default
