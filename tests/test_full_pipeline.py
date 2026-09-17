# -*- coding: utf-8 -*-
from vepforge import Task, VerifiableExperiencePipeline
from vepforge.llm import MockLLM
from vepforge.tools import ToolRegistry
from vepforge.verifier import VerifierRegistry


def test_full_pipeline_with_all_tools():
    pipe = VerifiableExperiencePipeline(
        llm=MockLLM(),
        tools=ToolRegistry.instantiate_default(),
        verifiers=VerifierRegistry.default_instances(),
    )
    exp = pipe.run(Task(goal="aggregate and summarize",
                        acceptance_criteria=["summary produced"]))
    assert exp.status.value == "succeeded"
    assert len(exp.evidences) >= 1
    assert exp.score is not None
