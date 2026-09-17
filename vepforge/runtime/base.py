# -*- coding: utf-8 -*-
"""沙箱运行时基类。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class Runtime(ABC):
    """沙箱执行环境接口：execute(code) -> {exit_code, stdout, stderr}。"""

    name: str = "runtime"

    @abstractmethod
    def execute(self, code: str) -> Dict[str, Any]:
        """在沙箱中执行代码，返回结构化结果。"""
