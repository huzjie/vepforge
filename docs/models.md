# 模型卡

| 模型 | 组织 | 参数量 | 许可 |
|---|---|---|---|
| atria-dawn-preview-744b | Shanghai AI Lab | 744B MoE | MIT |
| atria-dawn-preview-fp8 | Shanghai AI Lab | 744B (FP8) | MIT |
| glm-5-2-base | Z.ai | MoE 底座 | open-weights |

加载：

```python
from vepforge.catalog import ModelCatalog
cat = ModelCatalog()
models = cat.load()
print(cat.list())
```
