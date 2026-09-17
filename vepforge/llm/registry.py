# -*- coding: utf-8 -*-
"""LLM 后端注册表与工厂。"""
from __future__ import annotations

from typing import Any, Dict, Type

from .base import LLMBackend
from .mock import MockLLM
from .openai_compat import OpenAICompatLLM
from .anthropic_compat import AnthropicCompatLLM


class LLMRegistry:
    _registry: Dict[str, Type[LLMBackend]] = {}

    @classmethod
    def register(cls, name: str, backend: Type[LLMBackend]) -> Type[LLMBackend]:
        cls._registry[name] = backend
        return backend

    @classmethod
    def get(cls, name: str) -> Type[LLMBackend]:
        from ..core.errors import RegistryError
        if name not in cls._registry:
            raise RegistryError(f"llm backend not registered: {name}")
        return cls._registry[name]

    @classmethod
    def list(cls):
        return sorted(cls._registry.keys())

    @classmethod
    def build(cls, cfg: Dict[str, Any]) -> LLMBackend:
        """从配置字典构造后端。cfg: {provider, model, base_url, api_key}。"""
        provider = cfg.get("provider", "mock")
        if provider == "mock":
            return MockLLM()
        if provider in ("openai", "openai-compat"):
            return OpenAICompatLLM(cfg.get("base_url", ""), cfg.get("model", ""),
                                   cfg.get("api_key"))
        if provider in ("anthropic", "anthropic-compat"):
            return AnthropicCompatLLM(cfg.get("base_url", ""), cfg.get("model", ""),
                                      cfg.get("api_key"))
        raise ValueError(f"unknown provider: {provider}")


LLMRegistry.register("mock", MockLLM)
LLMRegistry.register("openai-compat", OpenAICompatLLM)
LLMRegistry.register("anthropic-compat", AnthropicCompatLLM)
