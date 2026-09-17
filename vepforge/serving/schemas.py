# -*- coding: utf-8 -*-
"""API 请求/响应模型（pydantic）。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    goal: str = Field(..., description="自然语言任务目标")
    constraints: List[str] = Field(default_factory=list)
    acceptance_criteria: List[str] = Field(default_factory=list)
    max_steps: int = 32
    timeout_seconds: float = 600.0


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: float = 0.2
    max_tokens: int = 1024


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    choices: List[Dict[str, Any]]


class MessagesRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    max_tokens: int = 1024
