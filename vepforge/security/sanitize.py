# -*- coding: utf-8 -*-
"""输入清洗：移除危险字符，防止命令注入。"""
from __future__ import annotations

import re

_DANGEROUS = re.compile(r"[;&|`$<>\\]")


def sanitize_command(cmd: str) -> str:
    """移除 shell 元字符，返回安全命令。"""
    return _DANGEROUS.sub("", cmd).strip()
