# -*- coding: utf-8 -*-
"""VepforgeClient：面向服务端的 Python SDK。"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from urllib import request


class VepforgeClient:
    """调用 vepforge HTTP 服务的轻量客户端（零第三方依赖）。"""

    def __init__(self, base_url: str = "http://127.0.0.1:8000",
                 api_key: Optional[str] = None, timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def run(self, goal: str, constraints: Optional[List[str]] = None,
            acceptance_criteria: Optional[List[str]] = None,
            max_steps: int = 32) -> Dict[str, Any]:
        payload = {
            "goal": goal,
            "constraints": constraints or [],
            "acceptance_criteria": acceptance_criteria or [],
            "max_steps": max_steps,
        }
        return self._post("/v1/run", payload)

    def health(self) -> Dict[str, Any]:
        return self._get("/health")

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = request.Request(f"{self.base_url}{path}",
                              data=json.dumps(payload).encode("utf-8"),
                              headers=headers)
        with request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _get(self, path: str) -> Dict[str, Any]:
        req = request.Request(f"{self.base_url}{path}")
        with request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
