# -*- coding: utf-8 -*-
"""Anthropic 兼容后端：走 /v1/messages。"""
from __future__ import annotations

import json
from typing import Any, Optional
from urllib import request

from .base import LLMBackend


class AnthropicCompatLLM(LLMBackend):
    name = "anthropic-compat"

    def __init__(self, base_url: str, model: str, api_key: Optional[str] = None,
                 timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout

    def complete(self, prompt: str, **kwargs: Any) -> str:
        payload = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 1024),
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {"Content-Type": "application/json",
                   "anthropic-version": "2023-06-01"}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        req = request.Request(
            f"{self.base_url}/v1/messages",
            data=json.dumps(payload).encode("utf-8"), headers=headers)
        with request.urlopen(req, timeout=self.timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return "".join(part.get("text", "") for part in body.get("content", []))
