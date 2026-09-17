# -*- coding: utf-8 -*-
"""LLM 后端抽象。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class LLMBackend(ABC):
    """LLM 后端接口，兼容 OpenAI/Anthropic 风格。"""

    name: str = "llm"

    @abstractmethod
    def complete(self, prompt: str, **kwargs: Any) -> str:
        """单轮补全。"""

    def analyze(self, goal: str) -> str:
        return self.complete(f"Analyze this goal and produce a step-by-step plan:\n{goal}")

    def reflect(self, goal: str, passed: bool) -> str:
        verdict = "succeeded" if passed else "needs improvement"
        return self.complete(f"Task goal: {goal}\nOutcome: {verdict}. Provide reflection.")
