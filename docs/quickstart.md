# 快速开始

## 安装

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -e .
```

## 三步上手

```bash
# 1. 自检（验证 verifiers/tools/agents/llm 全注册 + 端到端冒烟）
vepforge doctor

# 2. 跑一个长程任务
vepforge run --goal "parse and summarize three log files" \
  --criteria "summary produced" --criteria "exit code 0"

# 3. 启动 API
vepforge serve --port 8000
curl http://127.0.0.1:8000/health
```

## 用真实 LLM 后端

```python
from vepforge.llm import LLMRegistry
llm = LLMRegistry.build({
    "provider": "openai-compat",
    "base_url": "http://localhost:8001",   # vLLM / Atria 本地推理
    "model": "atria-dawn-preview-fp8",
})
from vepforge import VerifiableExperiencePipeline
pipe = VerifiableExperiencePipeline(llm=llm)
exp = pipe.run(Task(goal="..."))
```
