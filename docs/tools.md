# 工具集

| 工具 | 模块 | 说明 |
|---|---|---|
| shell | `tools/shell.py` | 受控命令执行（allowlist） |
| python | `tools/python_exec.py` | 子进程执行 Python |
| http | `tools/http_tool.py` | HTTP 请求 + 状态码 |
| file | `tools/file_tool.py` | 读写文件 + sha256 |
| search | `tools/search_tool.py` | 本地语料检索 |
| json | `tools/json_tool.py` | JSON 解析校验 |
| csv | `tools/csv_tool.py` | CSV 解析 + 聚合 |
| regex | `tools/regex_tool.py` | 正则提取 |
| calc | `tools/calc_tool.py` | 安全算术求值 |
| time | `tools/time_tool.py` | 时间戳 |

## 自定义工具

```python
from vepforge.tools import Tool, ToolResult

class MyTool(Tool):
    name = "my"
    description = "..."
    def run(self, inputs):
        return ToolResult(True, exit_code=0, data={})
```
