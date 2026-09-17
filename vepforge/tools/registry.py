# -*- coding: utf-8 -*-
"""工具注册表。"""
from __future__ import annotations

from typing import Dict, List, Type

from .base import Tool
from .shell import ShellTool
from .python_exec import PythonExecTool
from .http_tool import HttpTool
from .file_tool import FileTool
from .search_tool import SearchTool
from .json_tool import JsonTool
from .csv_tool import CsvTool
from .regex_tool import RegexTool
from .calc_tool import CalcTool
from .time_tool import TimeTool


class ToolRegistry:
    _registry: Dict[str, Type[Tool]] = {}

    @classmethod
    def register(cls, name: str, tool: Type[Tool]) -> Type[Tool]:
        cls._registry[name] = tool
        return tool

    @classmethod
    def get(cls, name: str) -> Type[Tool]:
        from ..core.errors import RegistryError
        if name not in cls._registry:
            raise RegistryError(f"tool not registered: {name}")
        return cls._registry[name]

    @classmethod
    def list(cls) -> List[str]:
        return sorted(cls._registry.keys())

    @classmethod
    def instantiate_default(cls) -> Dict[str, Tool]:
        return {
            "shell": ShellTool(),
            "python": PythonExecTool(),
            "http": HttpTool(),
            "file": FileTool(),
            "search": SearchTool(),
            "json": JsonTool(),
            "csv": CsvTool(),
            "regex": RegexTool(),
            "calc": CalcTool(),
            "time": TimeTool(),
        }


ToolRegistry.register("shell", ShellTool)
ToolRegistry.register("python", PythonExecTool)
ToolRegistry.register("http", HttpTool)
ToolRegistry.register("file", FileTool)
ToolRegistry.register("search", SearchTool)
ToolRegistry.register("json", JsonTool)
ToolRegistry.register("csv", CsvTool)
ToolRegistry.register("regex", RegexTool)
ToolRegistry.register("calc", CalcTool)
ToolRegistry.register("time", TimeTool)
