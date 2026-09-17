# -*- coding: utf-8 -*-
"""路由：任务执行 + OpenAI/Anthropic 兼容 chat。"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..core.task import Task
from ..pipeline.vep import VerifiableExperiencePipeline
from .schemas import (ChatCompletionRequest, ChatCompletionResponse,
                      MessagesRequest, TaskRequest)


def build_router(pipeline=None, llm=None, store=None):
    router = APIRouter()
    pipe = pipeline or VerifiableExperiencePipeline(llm=llm)

    @router.post("/run")
    def run_task(req: TaskRequest) -> Dict[str, Any]:
        task = Task(goal=req.goal, constraints=req.constraints,
                    acceptance_criteria=req.acceptance_criteria,
                    max_steps=req.max_steps,
                    timeout_seconds=req.timeout_seconds)
        exp = pipe.run(task)
        if store is not None:
            store.save(exp)
        return exp.to_dict()

    @router.post("/chat/completions", response_model=ChatCompletionResponse)
    def chat_completions(req: ChatCompletionRequest):
        if llm is None:
            raise HTTPException(503, "no llm backend configured")
        last = req.messages[-1].content if req.messages else ""
        try:
            reply = llm.complete(last, temperature=req.temperature,
                                 max_tokens=req.max_tokens)
        except Exception as e:  # noqa: BLE001
            raise HTTPException(500, f"llm error: {e}")
        return ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
            choices=[{"index": 0, "message": {"role": "assistant", "content": reply},
                      "finish_reason": "stop"}],
        )

    @router.post("/messages")
    def anthropic_messages(req: MessagesRequest):
        if llm is None:
            raise HTTPException(503, "no llm backend configured")
        last = req.messages[-1].content if req.messages else ""
        try:
            reply = llm.complete(last, max_tokens=req.max_tokens)
        except Exception as e:  # noqa: BLE001
            raise HTTPException(500, f"llm error: {e}")
        return {"id": f"msg_{uuid.uuid4().hex[:12]}", "type": "message",
                "content": [{"type": "text", "text": reply}]}

    return router
