# -*- coding: utf-8 -*-
"""本地沙箱：子进程执行 Python 代码。"""
from __future__ import annotations

import subprocess
import sys
from typing import Any, Dict

from .base import Runtime


class LocalRuntime(Runtime):
    name = "local"

    def __init__(self, python: str = "python", timeout: int = 30):
        self.python = python
        self.timeout = timeout

    def execute(self, code: str) -> Dict[str, Any]:
        try:
            proc = subprocess.run([self.python, "-c", code],
                                  capture_output=True, text=True,
                                  timeout=self.timeout)
            return {"exit_code": proc.returncode,
                    "stdout": proc.stdout, "stderr": proc.stderr}
        except subprocess.TimeoutExpired:
            return {"exit_code": -1, "stdout": "", "stderr": "timeout"}
        except FileNotFoundError as e:
            return {"exit_code": -2, "stdout": "", "stderr": str(e)}
