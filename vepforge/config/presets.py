# -*- coding: utf-8 -*-
"""运行配置预设：本地演示 / 生产 LLM / Docker 沙箱。"""
from __future__ import annotations

from typing import Any, Dict


PRESETS: Dict[str, Dict[str, Any]] = {
    "demo": {
        "name": "demo",
        "llm": {"provider": "mock"},
        "runtime": "local",
        "verifiers": ["exit_code", "hash", "http_status", "test_result", "nonempty"],
        "tools": ["python", "shell", "json", "csv", "regex", "calc", "time", "file", "search"],
    },
    "local-llm": {
        "name": "local-llm",
        "llm": {
            "provider": "openai-compat",
            "base_url": "http://localhost:8001",
            "model": "atria-dawn-preview-fp8",
            "api_key": "",
        },
        "runtime": "local",
        "verifiers": ["exit_code", "hash", "http_status", "test_result", "nonempty"],
        "tools": ["python", "shell", "json", "csv", "regex", "calc", "time", "file", "search"],
    },
    "docker": {
        "name": "docker",
        "llm": {"provider": "mock"},
        "runtime": "docker",
        "verifiers": ["exit_code", "hash", "http_status", "test_result", "nonempty"],
        "tools": ["python", "shell"],
    },
}


def load_preset(name: str) -> Dict[str, Any]:
    if name not in PRESETS:
        raise KeyError(f"unknown preset: {name}. available: {sorted(PRESETS)}")
    return PRESETS[name]
