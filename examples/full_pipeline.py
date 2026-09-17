# -*- coding: utf-8 -*-
"""完整流水线示例：LLM + 工具 + 验证器 + 经验落库。"""
from vepforge import Task, VerifiableExperiencePipeline
from vepforge.llm import MockLLM
from vepforge.tools import ToolRegistry
from vepforge.verifier import VerifierRegistry

pipe = VerifiableExperiencePipeline(
    llm=MockLLM(),
    tools=ToolRegistry.instantiate_default(),
    verifiers=VerifierRegistry.default_instances(),
)
exp = pipe.run(Task(
    goal="aggregate three CSV files and write a summary",
    constraints=["runtime < 60s"],
    acceptance_criteria=["summary produced", "exit code 0"],
))
print(f"status={exp.status.value} score={exp.score}")
print(f"artifacts={len(exp.artifacts)} evidences={len(exp.evidences)} "
      f"verified={exp.verified_evidence_count()}")
