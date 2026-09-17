# -*- coding: utf-8 -*-
"""展示所有内置工具。"""
from vepforge.tools import (ToolRegistry, JsonTool, CsvTool, RegexTool,
                            CalcTool, TimeTool)

print("registered tools:", ToolRegistry.list())

print(JsonTool().run({"text": '{"a": 1}'}).data)
print(CsvTool().run({"text": "name,value\\nfoo,1\\nbar,3"}).data)
print(RegexTool().run({"text": "a1 b2 c3", "pattern": r"\\d"}).data)
print(CalcTool().run({"expression": "2 + 3 * 4"}).data)
print(TimeTool().run({}).data)
