# -*- coding: utf-8 -*-
"""HTTP 工具：发起请求并捕获状态码。"""
from __future__ import annotations

import json
from typing import Any, Dict
from urllib import error, request

from .base import Tool, ToolResult


class HttpTool(Tool):
    name = "http"
    description = "Issue an HTTP request and capture status code / body."

    def __init__(self, timeout: int = 15):
        self.timeout = timeout

    def run(self, inputs: Dict[str, Any]) -> ToolResult:
        url = inputs.get("url", "")
        method = inputs.get("method", "GET").upper()
        if not url:
            return ToolResult(False, exit_code=2, stderr="missing url")
        try:
            req = request.Request(url, method=method)
            with request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")[:4096]
                return ToolResult(True, exit_code=0, stdout=body,
                                  data={"status": resp.status})
        except error.HTTPError as e:
            return ToolResult(False, exit_code=1, stderr=str(e),
                              data={"status": e.code})
        except error.URLError as e:
            return ToolResult(False, exit_code=-1, stderr=str(e))
