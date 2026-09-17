# 任务模板

内置模板（`vepforge.templates`）：

| 模板 | 场景 |
|---|---|
| data-aggregation | 多 CSV 聚合汇总 |
| code-execution | 沙箱代码执行 |
| web-extraction | 网页抓取 |
| json-validation | JSON 校验 |
| report-generation | 报告生成 |

```python
from vepforge.templates import get_template
t = get_template("data-aggregation")
```
