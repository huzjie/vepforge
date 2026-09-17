# -*- coding: utf-8 -*-
"""计算工具：安全求值算术表达式。"""
from __future__ import annotations

import ast
import operator
from typing import Any, Dict

from .base import Tool, ToolResult

_ALLOWED = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


class CalcTool(Tool):
    name = "calc"
    description = "Safely evaluate a simple arithmetic expression."

    def run(self, inputs: Dict[str, Any]) -> ToolResult:
        expr = inputs.get("expression", "")
        try:
            value = self._eval(ast.parse(expr, mode="eval").body)
            return ToolResult(True, exit_code=0, data={"value": value})
        except Exception as e:  # noqa: BLE001
            return ToolResult(False, exit_code=1, stderr=str(e))

    def _eval(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
            return _ALLOWED[type(node.op)](self._eval(node.left), self._eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
            return _ALLOWED[type(node.op)](self._eval(node.operand))
        raise ValueError(f"unsupported expression: {ast.dump(node)}")
