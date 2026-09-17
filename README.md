# vepforge

**可验证经验流水线驱动的长程自主智能体执行平台** · Verifiable Experience Pipeline (VEP)

> 基于上海 AI Lab 开源的 **Atria Dawn Preview（744B MoE agentic 模型）** 的核心理念构建：
> 把长程自主任务的「分析 → 编码 → 执行 → 复盘」闭环，**grounding 到真实可执行环境**，
> 让任务目标、智能体轨迹、中间产物、外部证据四者被**可验证地连接**起来。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://www.python.org/)

---

## 为什么是 vepforge

大模型从「聊天」走向「干活」，最大痛点不是生成质量，而是**不可信**：

- 模型声称「已执行」，但**没有真实执行**（幻觉工具输出）；
- 长程任务跑偏了，**无法追溯**是哪一步出的错；
- 结果无法审计，**没有证据链**支撑。

Atria Dawn Preview 用 **Verifiable Experience Pipeline（VEP）** 回答这个问题：
工具调用建立在**真实可执行环境**上，而非静态文本。vepforge 把这一理念落成一个
**零依赖、可本地运行、可审计**的工程框架。

## 核心概念

| 实体 | 含义 | 可验证性 |
|---|---|---|
| `Task` | 任务目标 + 约束 + 验收标准 | 生命周期可追踪 |
| `Trajectory` | 智能体轨迹（每步 thought/action/observation/evidence） | 逐步可回放 |
| `Artifact` | 中间产物（代码/数据/报告），内容 sha256 寻址 | 哈希可校验 |
| `Evidence` | 外部证据（退出码/stdout/HTTP 状态/哈希），来自工具真实执行 | 验证器可判定 |

## 快速开始

```bash
pip install -r requirements.txt

# 自检
python -m vepforge.cli.main doctor

# 运行一个任务
python -m vepforge.cli.main run --goal "aggregate three CSVs and summarize" \
  --criteria "summary produced"

# 列出模型卡 / 工具
python -m vepforge.cli.main models
python -m vepforge.cli.main tools

# 启动 API 服务
python -m vepforge.cli.main serve --port 8000
```

Python API：

```python
from vepforge import Task, VerifiableExperiencePipeline

pipe = VerifiableExperiencePipeline()
exp = pipe.run(Task(
    goal="verify the pipeline produces verifiable experience",
    acceptance_criteria=["at least one artifact"],
))
print(exp.status, exp.score, len(exp.artifacts), len(exp.evidences))
```

## 目录结构

见 [docs/architecture.md](docs/architecture.md)。

## 基准对齐

vepforge 内置五类智能体基准评测，对齐 Atria Dawn 官方指标：

- AutomationBench（长程自动化）— 53.8
- BrowseComp（浏览检索）— 92.5
- DeepSearchQA（深度检索问答）— 96.0
- BFCL v4（函数调用）— 77.0
- CyberGym（可执行环境任务）— 86.5

运行：`python -m vepforge.cli.main bench`（见 docs/benchmarks.md）。

## License

MIT — 见 [LICENSE](LICENSE)。
