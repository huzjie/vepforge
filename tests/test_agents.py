# -*- coding: utf-8 -*-
from vepforge.agents import AnalyzerAgent, CoderAgent, ReflectorAgent, Orchestrator
from vepforge.core.task import Task


def test_analyzer_decompose():
    a = AnalyzerAgent()
    plan = a.decompose("do three things well")
    assert len(plan) >= 1


def test_coder_synthesize():
    c = CoderAgent()
    art = c.act({"plan": [{"desc": "step1"}]})
    assert "run" in art["artifact"].content


def test_orchestrator_full_loop():
    o = Orchestrator()
    result = o.run(Task(goal="hello world"))
    assert "reflect" in result
