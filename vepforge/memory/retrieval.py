# -*- coding: utf-8 -*-
"""Retrieval：基于嵌入的经验检索。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .embedding import TextEmbedder


class Retrieval:
    """经验检索器：给目标 query 找最相似的历史经验。"""

    def __init__(self, store, embedder: Optional[TextEmbedder] = None):
        self.store = store
        self.embedder = embedder or TextEmbedder()

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        q_vec = self.embedder.embed(query)
        scored = []
        for meta in self.store.list():
            exp = self.store.load(meta["experience_id"])
            if exp is None:
                continue
            text = exp.task.goal + " " + " ".join(exp.task.acceptance_criteria)
            score = self.embedder.cosine(q_vec, self.embedder.embed(text))
            scored.append({"experience_id": meta["experience_id"],
                           "score": score, "goal": exp.task.goal,
                           "status": meta.get("status")})
        scored.sort(key=lambda x: -x["score"])
        return scored[:top_k]
