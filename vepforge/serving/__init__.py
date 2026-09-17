# -*- coding: utf-8 -*-
"""serving 包：FastAPI 服务 + OpenAI/Anthropic 兼容接口。"""
from .app import create_app

__all__ = ["create_app"]
