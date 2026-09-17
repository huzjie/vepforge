# -*- coding: utf-8 -*-
"""搜索工具：本地语料检索（可注入外部搜索后端）。"""
from __future__ import annotations

from typing import Any, Dict, List

from .base import Tool, ToolResult


class SearchTool(Tool):
    name = "search"
    description = "Search a local corpus for a query; returns ranked snippets."

    def __init__(self, corpus: Any = None):
        self.corpus = corpus or []

    def run(self, inputs: Dict[str, Any]) -> ToolResult:
        query = inputs.get("query", "")
        if not query:
            return ToolResult(False, exit_code=2, stderr="empty query")
        hits = self._rank(query)
        return ToolResult(True, exit_code=0,
                          data={"query": query, "hits": hits})

    def _rank(self, query: str) -> List[Dict[str, Any]]:
        results = []
        for doc in self.corpus:
            text = doc.get("text", "")
            score = sum(1 for w in query.split() if w in text)
            if score > 0:
                results.append({"text": text[:200], "score": score})
        results.sort(key=lambda x: -x["score"])
        return results[:5]
