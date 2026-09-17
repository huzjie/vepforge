# -*- coding: utf-8 -*-
"""展示配置预设。"""
from vepforge.config import load_preset, PRESETS

for name in PRESETS:
    print(name, "->", load_preset(name)["llm"]["provider"])
