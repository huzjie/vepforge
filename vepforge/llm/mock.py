# -*- coding: utf-8 -*-
"""MockLLM：确定性假后端，无外部依赖。"""
from __future__ import annotations

from typing import Any

from .base import LLMBackend


class MockLLM(LLMBackend):
    name = "mock"

    def __init__(self, response_template: str = "mock response: {prompt}"):
        self.response_template = response_template

    def complete(self, prompt: str, **kwargs: Any) -> str:
        return self.response_template.format(prompt=prompt[:60])
