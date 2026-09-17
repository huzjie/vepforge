# -*- coding: utf-8 -*-
"""编码智能体：把计划转成可执行代码产物。"""
from __future__ import annotations

from typing import Any, Dict, List

from ..core.artifact import Artifact, ArtifactKind
from .base import Agent


class CoderAgent(Agent):
    name = "coder"

    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        plan = context.get("plan", [])
        code = self.synthesize(plan)
        art = Artifact(name="generated_solution", kind=ArtifactKind.CODE,
                       content=code, meta={"role": "code"})
        return {"role": "code", "artifact": art, "language": "python"}

    def synthesize(self, plan: List[Dict[str, Any]]) -> str:
        lines = ["# vepforge generated solution", "def run():", "    results = []"]
        for item in plan:
            lines.append(f"    results.append({item.get('desc', 'step')!r})")
        lines.append("    return results")
        lines.append("")
        lines.append("if __name__ == '__main__':")
        lines.append("    print(run())")
        return "\n".join(lines)
