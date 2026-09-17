# -*- coding: utf-8 -*-
"""编排器：串联四类智能体完成一次长程闭环。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..core.task import Task
from .analyzer import AnalyzerAgent
from .coder import CoderAgent
from .executor import ExecutorAgent
from .reflector import ReflectorAgent


class Orchestrator:
    """轻量编排：analyze → code → execute → reflect。"""

    def __init__(self, llm=None, runtime=None):
        self.analyzer = AnalyzerAgent(llm)
        self.coder = CoderAgent(llm)
        self.executor = ExecutorAgent(llm, runtime)
        self.reflector = ReflectorAgent(llm)

    def run(self, task: Task) -> Dict[str, Any]:
        analysis = self.analyzer.act({"goal": task.goal})
        code = self.coder.act({"plan": analysis["plan"]})
        execute = self.executor.act({"code": code["artifact"].content})
        reflect = self.reflector.act({
            "acceptance_criteria": task.acceptance_criteria,
            "evidences": [execute.get("evidence")] if execute.get("evidence") else [],
        })
        return {
            "analysis": analysis,
            "code": code,
            "execute": execute,
            "reflect": reflect,
        }
