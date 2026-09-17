# -*- coding: utf-8 -*-
"""智能体注册表。"""
from __future__ import annotations

from typing import Dict, List, Type

from .base import Agent
from .analyzer import AnalyzerAgent
from .coder import CoderAgent
from .executor import ExecutorAgent
from .reflector import ReflectorAgent


class AgentRegistry:
    _registry: Dict[str, Type[Agent]] = {}

    @classmethod
    def register(cls, name: str, agent: Type[Agent]) -> Type[Agent]:
        cls._registry[name] = agent
        return agent

    @classmethod
    def get(cls, name: str) -> Type[Agent]:
        from ..core.errors import RegistryError
        if name not in cls._registry:
            raise RegistryError(f"agent not registered: {name}")
        return cls._registry[name]

    @classmethod
    def list(cls) -> List[str]:
        return sorted(cls._registry.keys())


AgentRegistry.register("analyzer", AnalyzerAgent)
AgentRegistry.register("coder", CoderAgent)
AgentRegistry.register("executor", ExecutorAgent)
AgentRegistry.register("reflector", ReflectorAgent)
