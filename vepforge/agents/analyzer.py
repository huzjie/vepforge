# -*- coding: utf-8 -*-
"""分析智能体：把长程目标拆解为可执行子计划。"""
from __future__ import annotations

from typing import Any, Dict, List

from .base import Agent


class AnalyzerAgent(Agent):
    name = "analyzer"

    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        goal = context.get("goal", "")
        plan = self.decompose(goal)
        return {"role": "analyze", "plan": plan, "goal": goal}

    def decompose(self, goal: str, max_items: int = 12) -> List[Dict[str, Any]]:
        words = goal.split()
        subgoals = []
        for i, w in enumerate(words[:max_items], 1):
            subgoals.append({"id": i, "desc": f"resolve '{w}'", "depends_on": []})
        if not subgoals:
            subgoals = [{"id": 1, "desc": "execute goal", "depends_on": []}]
        return subgoals
