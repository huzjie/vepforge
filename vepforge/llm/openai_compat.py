# -*- coding: utf-8 -*-
"""OpenAI 兼容后端：走 /v1/chat/completions（支持本地 vLLM 等）。"""
from __future__ import annotations

import json
from typing import Any, Optional
from urllib import request

from .base import LLMBackend


class OpenAICompatLLM(LLMBackend):
    name = "openai-compat"

    def __init__(self, base_url: str, model: str, api_key: Optional[str] = None,
                 timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout

    def complete(self, prompt: str, **kwargs: Any) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.2),
            "max_tokens": kwargs.get("max_tokens", 1024),
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"), headers=headers)
        with request.urlopen(req, timeout=self.timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"]
