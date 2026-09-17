# -*- coding: utf-8 -*-
"""Docker 沙箱：容器内执行（可选，需 docker 可用）。"""
from __future__ import annotations

import subprocess
import tempfile
import os
from typing import Any, Dict

from .base import Runtime


class DockerRuntime(Runtime):
    name = "docker"

    def __init__(self, image: str = "python:3.12-slim", timeout: int = 60):
        self.image = image
        self.timeout = timeout

    def execute(self, code: str) -> Dict[str, Any]:
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                             encoding="utf-8") as f:
                f.write(code)
                path = f.name
            cmd = ["docker", "run", "--rm", "-v", f"{path}:/tmp/code.py",
                   self.image, "python", "/tmp/code.py"]
            proc = subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=self.timeout)
            return {"exit_code": proc.returncode,
                    "stdout": proc.stdout, "stderr": proc.stderr}
        except FileNotFoundError:
            return {"exit_code": -2, "stdout": "", "stderr": "docker not found"}
        except subprocess.TimeoutExpired:
            return {"exit_code": -1, "stdout": "", "stderr": "timeout"}
        finally:
            if "path" in locals() and os.path.exists(path):
                os.unlink(path)
