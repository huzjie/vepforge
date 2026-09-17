# -*- coding: utf-8 -*-
"""BrowseComp：网页浏览/检索基准。"""
from __future__ import annotations

from typing import Any, Dict, List

from .base import Benchmark


class BrowseComp(Benchmark):
    name = "browsecomp"

    def tasks(self) -> List[Dict[str, Any]]:
        return [
            {"id": "browse-1", "goal": "search and cite the source of a fact",
             "criteria": ["evidence linked"]},
            {"id": "browse-2", "goal": "compare two pages and summarize",
             "criteria": ["summary produced"]},
        ]

    def score(self, result: Dict[str, Any], task: Dict[str, Any]) -> float:
        ev = result.get("evidences", [])
        verified = sum(1 for e in ev if e.get("verified"))
        return min(100.0, verified * 50.0 + (50.0 if result.get("status") == "succeeded" else 0))
