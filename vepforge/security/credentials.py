# -*- coding: utf-8 -*-
"""凭证管理：从环境变量读取，禁止硬编码。"""
from __future__ import annotations

import os
from typing import Optional


class CredentialStore:
    """统一从环境变量读取 API key，永不落盘明文。"""

    @staticmethod
    def get(name: str, env_var: str) -> Optional[str]:
        return os.environ.get(env_var)

    @staticmethod
    def llm_api_key() -> Optional[str]:
        return os.environ.get("LLM_API_KEY")

    @staticmethod
    def has_secret(value: str) -> bool:
        return any(marker in value for marker in
                   ("ghp_", "sk-", "Bearer", "api_key"))
