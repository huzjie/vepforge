# -*- coding: utf-8 -*-
"""复盘智能体：对照验收标准评估结果，产出结论与改进建议。"""
from __future__ import annotations

from typing import Any, Dict, List

from .base import Agent


class ReflectorAgent(Agent):
    name = "reflector"

    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        criteria = context.get("acceptance_criteria", [])
        evidences = context.get("evidences", [])
        passed = self.evaluate(criteria, evidences)
        return {
            "role": "reflect",
            "passed": passed,
            "conclusion": "success" if passed else "needs improvement",
            "suggestions": self.suggest(criteria, evidences, passed),
        }

    def evaluate(self, criteria: List[str], evidences: List[Any]) -> bool:
        if not criteria:
            return True
        verified = [e for e in evidences if getattr(e, "verified", False)]
        return len(verified) >= 1

    def suggest(self, criteria: List[str], evidences: List[Any], passed: bool) -> List[str]:
        if passed:
            return ["experience verified; no further action"]
        return ["add more verifiable evidence", "re-check acceptance criteria",
                "bind tools to real executable environment"]
