# -*- coding: utf-8 -*-
"""最小示例：零依赖跑通一个任务。"""
from vepforge import Task, VerifiableExperiencePipeline

pipe = VerifiableExperiencePipeline()
exp = pipe.run(Task(
    goal="demonstrate the verifiable experience pipeline",
    acceptance_criteria=["at least one artifact"],
))
print(f"status={exp.status.value} artifacts={len(exp.artifacts)} "
      f"evidences={len(exp.evidences)} score={exp.score}")
