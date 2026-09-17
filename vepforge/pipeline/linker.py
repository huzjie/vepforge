# -*- coding: utf-8 -*-
"""Linker：把任务目标、轨迹、产物、证据连接起来。"""
from __future__ import annotations

from typing import Any, Dict, List

from ..core.evidence import Evidence
from ..core.trajectory import Step, StepRole


class Linker:
    """在轨迹中维护步骤 → 产物/证据的关联，形成可追溯链路。

    每条 evidence 关联到产生它的 action step；每个 artifact 关联到
    生成它的 code/execute step。这样复盘时可以精确回溯「哪一步产出了
    哪个产物、有什么证据支撑」。
    """

    def __init__(self):
        self._evidence_links: Dict[str, List[str]] = {}   # step_id -> evidence_ids
        self._artifact_links: Dict[str, List[str]] = {}   # step_id -> artifact_ids

    def link_evidence(self, step: Step, evidence: Evidence) -> None:
        self._evidence_links.setdefault(step.step_id, []).append(evidence.evidence_id)

    def link_artifact(self, step: Step, artifact_id: str) -> None:
        self._artifact_links.setdefault(step.step_id, []).append(artifact_id)

    def evidence_ids_for(self, step: Step) -> List[str]:
        return self._evidence_links.get(step.step_id, [])

    def artifact_ids_for(self, step: Step) -> List[str]:
        return self._artifact_links.get(step.step_id, [])

    def summary(self) -> Dict[str, Any]:
        return {
            "evidence_links": self._evidence_links,
            "artifact_links": self._artifact_links,
        }
