# -*- coding: utf-8 -*-
"""任务模板目录：常见长程任务的 goal/约束/验收标准。"""
from __future__ import annotations

from typing import Any, Dict, List


TEMPLATES: Dict[str, Dict[str, Any]] = {
    "data-aggregation": {
        "goal": "aggregate multiple CSV files and produce a summary report",
        "constraints": ["output must be valid CSV", "keep runtime under 60s"],
        "acceptance_criteria": ["summary produced", "exit code 0"],
    },
    "code-execution": {
        "goal": "execute a Python snippet in sandbox and verify the exit code",
        "constraints": ["no network access"],
        "acceptance_criteria": ["exit code 0", "evidence verified"],
    },
    "web-extraction": {
        "goal": "fetch a webpage and extract key facts",
        "constraints": ["timeout 15s"],
        "acceptance_criteria": ["http 200", "facts extracted"],
    },
    "json-validation": {
        "goal": "validate and normalize a JSON payload",
        "constraints": ["preserve original fields"],
        "acceptance_criteria": ["valid json", "normalized output"],
    },
    "report-generation": {
        "goal": "generate a structured report from evidence",
        "constraints": ["must be markdown"],
        "acceptance_criteria": ["report produced", "sha256 recorded"],
    },
}


def list_templates() -> List[str]:
    return sorted(TEMPLATES.keys())


def get_template(name: str) -> Dict[str, Any]:
    if name not in TEMPLATES:
        raise KeyError(f"unknown template: {name}. available: {list_templates()}")
    return TEMPLATES[name]
