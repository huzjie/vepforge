# 基准评测

## 对齐 Atria Dawn

vepforge 内置五类基准，对应官方指标：

| 基准 | 官方分 | 说明 |
|---|---|---|
| AutomationBench | 53.8 | 长程任务自动化 |
| BrowseComp | 92.5 | 网页浏览检索 |
| DeepSearchQA | 96.0 | 深度检索问答 |
| BFCL v4 | 77.0 | 函数调用 |
| CyberGym | 86.5 | 可执行环境任务 |

## 运行

```python
from vepforge import VerifiableExperiencePipeline
from vepforge.benchmarks import (BenchmarkRunner, AutomationBench,
                                 BrowseComp, DeepSearchQA, BFCL, CyberGym)
from vepforge.llm import MockLLM

pipe = VerifiableExperiencePipeline(llm=MockLLM())
runner = BenchmarkRunner(pipe, [AutomationBench(), BrowseComp(),
                                DeepSearchQA(), BFCL(), CyberGym()])
report = runner.run()
print(report["overall"], report["benchmarks"])
```

> 注意：无真实 LLM/工具时，`MockLLM` 跑出的分数只验证「流水线可闭环」，
> 不代表模型能力。接入真实后端后分数才具备对标意义。
