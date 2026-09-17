# -*- coding: utf-8 -*-
from vepforge import Task, VerifiableExperiencePipeline
from vepforge.llm import MockLLM
from vepforge.verifier import VerifierRegistry


def test_pipeline_end_to_end():
    pipe = VerifiableExperiencePipeline(
        llm=MockLLM(),
        verifiers=VerifierRegistry.default_instances(),
    )
    exp = pipe.run(Task(goal="verify the pipeline",
                        acceptance_criteria=["artifact"]))
    assert exp.status.value == "succeeded"
    assert len(exp.artifacts) >= 1
    assert exp.score is not None


def test_pipeline_no_llm():
    pipe = VerifiableExperiencePipeline()
    exp = pipe.run(Task(goal="minimal run"))
    assert exp.status.value == "succeeded"


def test_pipeline_with_tools():
    from vepforge.tools import PythonExecTool
    pipe = VerifiableExperiencePipeline(
        tools={"python": PythonExecTool()},
        verifiers=VerifierRegistry.default_instances(),
    )
    exp = pipe.run(Task(goal="execute python"))
    assert exp.status.value == "succeeded"
    assert len(exp.evidences) >= 1
