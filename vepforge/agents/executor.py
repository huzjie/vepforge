# -*- coding: utf-8 -*-
"""执行智能体：把代码产物送入沙箱真实执行，产出证据。"""
from __future__ import annotations

from typing import Any, Dict, Optional

from ..core.evidence import Evidence, EvidenceKind
from .base import Agent


class ExecutorAgent(Agent):
    name = "executor"

    def __init__(self, llm=None, runtime=None):
        super().__init__(llm)
        self.runtime = runtime

    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        code = context.get("code", "")
        if self.runtime is None:
            return {"role": "execute", "evidence": None,
                    "note": "no runtime bound; simulated success"}
        result = self.runtime.execute(code)
        evidence = Evidence(
            kind=EvidenceKind.EXIT_CODE,
            value=result.get("exit_code", 0),
            tool="sandbox",
            verifiable=True,
            meta={"stdout": result.get("stdout", ""), "stderr": result.get("stderr", "")},
        )
        return {"role": "execute", "evidence": evidence, "result": result}
