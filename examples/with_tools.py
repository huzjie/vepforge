# -*- coding: utf-8 -*-
"""带工具 + 验证器的示例：真实执行并产生证据。"""
from vepforge import Task, VerifiableExperiencePipeline
from vepforge.tools import PythonExecTool
from vepforge.verifier import VerifierRegistry

pipe = VerifiableExperiencePipeline(
    tools={"python": PythonExecTool()},
    verifiers=VerifierRegistry.default_instances(),
)
exp = pipe.run(Task(goal="execute code in sandbox and verify exit code"))
for e in exp.evidences:
    print(f"evidence: {e.kind.value} tool={e.tool} verified={e.verified}")
