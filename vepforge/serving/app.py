# -*- coding: utf-8 -*-
"""FastAPI 应用工厂。"""
from __future__ import annotations

import uuid
from typing import Optional

from fastapi import FastAPI

from .routes import build_router


def create_app(pipeline=None, llm=None, store=None) -> FastAPI:
    app = FastAPI(
        title="vepforge",
        description="Verifiable Experience Pipeline — long-horizon autonomous agent platform",
        version="0.1.0",
    )
    router = build_router(pipeline, llm, store)
    app.include_router(router, prefix="/v1")

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "vepforge"}

    return app
