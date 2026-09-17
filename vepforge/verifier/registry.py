# -*- coding: utf-8 -*-
"""验证器注册表。"""
from __future__ import annotations

from typing import Dict, List, Type

from .base import Verifier
from .exit_code import ExitCodeVerifier
from .hash import HashVerifier
from .http import HttpStatusVerifier
from .schema import SchemaVerifier
from .test_result import TestResultVerifier
from .nonempty import NonEmptyVerifier


class VerifierRegistry:
    """集中管理验证器，支持按名称获取与按顺序批量校验。"""

    _registry: Dict[str, Type[Verifier]] = {}

    @classmethod
    def register(cls, name: str, verifier: Type[Verifier]) -> Type[Verifier]:
        cls._registry[name] = verifier
        return verifier

    @classmethod
    def get(cls, name: str) -> Type[Verifier]:
        if name not in cls._registry:
            from ..core.errors import RegistryError
            raise RegistryError(f"verifier not registered: {name}")
        return cls._registry[name]

    @classmethod
    def list(cls) -> List[str]:
        return sorted(cls._registry.keys())

    @classmethod
    def default_instances(cls) -> List[Verifier]:
        return [ExitCodeVerifier(), HashVerifier(), HttpStatusVerifier(),
                SchemaVerifier(), TestResultVerifier(), NonEmptyVerifier()]


VerifierRegistry.register("exit_code", ExitCodeVerifier)
VerifierRegistry.register("hash", HashVerifier)
VerifierRegistry.register("http_status", HttpStatusVerifier)
VerifierRegistry.register("schema", SchemaVerifier)
VerifierRegistry.register("test_result", TestResultVerifier)
VerifierRegistry.register("nonempty", NonEmptyVerifier)
