# API 文档

## REST 端点

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 健康检查 |
| POST | `/v1/run` | 执行一个任务 |
| POST | `/v1/chat/completions` | OpenAI 兼容 chat |
| POST | `/v1/messages` | Anthropic 兼容 messages |

## POST /v1/run

```json
{
  "goal": "aggregate three CSV files and write a summary",
  "constraints": ["keep it under 100 lines"],
  "acceptance_criteria": ["summary produced"],
  "max_steps": 32,
  "timeout_seconds": 600
}
```

响应为 `Experience` 完整 JSON（task + trajectory + artifacts + evidences + status + score）。

## Python SDK

```python
from vepforge.sdk import VepforgeClient
client = VepforgeClient("http://127.0.0.1:8000")
print(client.health())
exp = client.run("verify the pipeline", acceptance_criteria=["artifact"])
```
