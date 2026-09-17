# 配置预设

| 预设 | LLM | 运行时 | 用途 |
|---|---|---|---|
| demo | mock | local | 本地演示 / 单测 |
| local-llm | openai-compat (vLLM) | local | 本地真实推理 |
| docker | mock | docker | 隔离沙箱 |

```python
from vepforge.config import load_preset
cfg = load_preset("demo")
```
