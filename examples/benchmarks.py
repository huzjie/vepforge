# -*- coding: utf-8 -*-
"""跑五类基准。"""
from vepforge import VerifiableExperiencePipeline
from vepforge.llm import MockLLM
from vepforge.benchmarks import (BenchmarkRunner, AutomationBench,
                                 BrowseComp, DeepSearchQA, BFCL, CyberGym)

pipe = VerifiableExperiencePipeline(llm=MockLLM())
runner = BenchmarkRunner(pipe, [AutomationBench(), BrowseComp(),
                                DeepSearchQA(), BFCL(), CyberGym()])
report = runner.run()
print("overall:", report["overall"])
for name, score in report["benchmarks"].items():
    print(f"  {name}: {score}")
