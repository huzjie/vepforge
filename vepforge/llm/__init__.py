# -*- coding: utf-8 -*-
"""llm 包：LLM 后端抽象与多 provider 适配。"""
from .base import LLMBackend
from .mock import MockLLM
from .openai_compat import OpenAICompatLLM
from .anthropic_compat import AnthropicCompatLLM
from .registry import LLMRegistry

__all__ = ["LLMBackend", "MockLLM", "OpenAICompatLLM",
           "AnthropicCompatLLM", "LLMRegistry"]
