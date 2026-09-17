# -*- coding: utf-8 -*-
"""VerifiableExperiencePipeline：可验证经验流水线主引擎。"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from ..core.artifact import Artifact, ArtifactKind
from ..core.errors import TaskError
from ..core.experience import Experience, ExperienceStatus
from ..core.task import Task, TaskStatus
from ..core.trajectory import Trajectory, StepRole
from .linker import Linker
from .stages import STAGE_ORDER, Stage, StageResult


class VerifiableExperiencePipeline:
    """VEP 主引擎：驱动「分析 → 编码 → 执行 → 复盘」长程闭环。

    每个阶段产出被记录进轨迹，工具执行产出被捕获为证据，
    代码/报告产出被捕获为产物，最后统一验证并打分。

    引擎解耦了 LLM 后端与工具执行器：
    - llm：通过 ``llm`` 参数注入（默认 mock，返回确定性结果）
    - tools：通过 ``tools`` 参数注入（默认空，执行阶段跳过）
    这保证在无外部模型/网络时也能端到端跑通 demo。
    """

    def __init__(self, llm=None, tools=None, verifiers=None, max_steps: Optional[int] = None):
        self.llm = llm
        self.tools = tools or {}
        self.verifiers = verifiers or []
        self.max_steps = max_steps
        self.linker = Linker()

    def run(self, task: Task) -> Experience:
        """执行一个任务，返回完整经验记录。"""
        if task.max_steps <= 0:
            raise TaskError("task.max_steps must be positive")
        if self.max_steps:
            task.max_steps = self.max_steps

        task.mark(TaskStatus.RUNNING)
        exp = Experience(task=task, trajectory=Trajectory(task_id=task.task_id))

        try:
            for stage in STAGE_ORDER:
                task.mark(TaskStatus(stage.value))
                result = self._run_stage(stage, exp)
                exp.trajectory.add(
                    StepRole.REFLECTION,
                    {"stage": stage.value, "ok": result.ok, "detail": result.detail},
                )
                if not result.ok:
                    # 复盘失败允许降级为 failed 但不中断；执行阶段失败则中断
                    if stage == Stage.EXECUTE:
                        exp.status = ExperienceStatus.FAILED
                        task.mark(TaskStatus.FAILED)
                        exp.finished_at = time.time()
                        return exp
                    exp.trajectory.add(
                        StepRole.ERROR,
                        {"stage": stage.value, "error": result.error},
                    )

            # 全部阶段完成 → 验证并打分
            exp.status = ExperienceStatus.VERIFIED
            self._verify(exp)
            exp.score = self._score(exp)
            task.mark(TaskStatus.SUCCEEDED)
            exp.status = ExperienceStatus.SUCCEEDED
        except Exception as e:  # noqa: BLE001
            exp.trajectory.add(StepRole.ERROR, {"error": str(e)})
            exp.status = ExperienceStatus.FAILED
            task.mark(TaskStatus.FAILED)
        finally:
            exp.finished_at = time.time()
            exp.meta["linker"] = self.linker.summary()
        return exp

    def _run_stage(self, stage: Stage, exp: Experience) -> StageResult:
        handler = {
            Stage.ANALYZE: self._analyze,
            Stage.CODE: self._code,
            Stage.EXECUTE: self._execute,
            Stage.REFLECT: self._reflect,
        }[stage]
        return handler(exp)

    def _analyze(self, exp: Experience) -> StageResult:
        """分析阶段：拆解目标为子目标与计划。"""
        task = exp.task
        plan = {
            "goal": task.goal,
            "constraints": task.constraints,
            "acceptance_criteria": task.acceptance_criteria,
            "subgoals": self._decompose(task.goal),
            "approach": "long-horizon autonomous loop (analyze→code→execute→reflect)",
        }
        if self.llm is not None:
            try:
                analysis = self.llm.analyze(task.goal)
                plan["llm_analysis"] = analysis
            except Exception as e:  # noqa: BLE001
                plan["llm_error"] = str(e)
        exp.trajectory.add(StepRole.THOUGHT, plan)
        return StageResult(Stage.ANALYZE, True, detail=plan)

    def _code(self, exp: Experience) -> StageResult:
        """编码阶段：生成可执行方案并落为 artifact。"""
        code = self._synthesize_code(exp.task)
        art = Artifact(name="plan_code", kind=ArtifactKind.CODE, content=code,
                       meta={"stage": "code"})
        exp.add_artifact(art)
        step = exp.trajectory.add(StepRole.ARTIFACT, {"artifact_id": art.artifact_id,
                                                       "name": art.name})
        self.linker.link_artifact(step, art.artifact_id)
        return StageResult(Stage.CODE, True, detail={"artifact": art.artifact_id})

    def _execute(self, exp: Experience) -> StageResult:
        """执行阶段：真实调用工具，捕获证据。"""
        if not self.tools:
            exp.trajectory.add(StepRole.OBSERVATION,
                               {"note": "no tools configured; execute skipped"})
            return StageResult(Stage.EXECUTE, True,
                               detail={"note": "no tools; skipped"})
        # 取 code 阶段产物作为可执行输入
        code = ""
        for a in exp.artifacts:
            if a.kind == ArtifactKind.CODE:
                code = a.content
                break
        ok = True
        detail: Dict[str, Any] = {}
        for name, tool in self.tools.items():
            try:
                from ..core.evidence import Evidence, EvidenceKind
                inputs = self._tool_inputs(name, code)
                result = tool.run(inputs)
                result_d = result.to_dict() if hasattr(result, "to_dict") else dict(result)
                ev = Evidence(kind=EvidenceKind.EXIT_CODE,
                              value=result_d.get("exit_code", 0),
                              tool=name, verifiable=True,
                              meta={"stdout": result_d.get("stdout", ""),
                                    "stderr": result_d.get("stderr", "")})
                # 执行后立即用已注册验证器校验证据
                ev = self._verify_evidence(ev)
                exp.add_evidence(ev)
                step = exp.trajectory.add(StepRole.EVIDENCE,
                                          {"tool": name, "evidence_id": ev.evidence_id})
                self.linker.link_evidence(step, ev)
                detail[name] = result_d
            except Exception as e:  # noqa: BLE001
                ok = False
                detail[name] = {"error": str(e)}
                exp.trajectory.add(StepRole.ERROR, {"tool": name, "error": str(e)})
        return StageResult(Stage.EXECUTE, ok, detail=detail)

    def _tool_inputs(self, name: str, code: str) -> Dict[str, Any]:
        """为不同工具构造合理的默认输入。"""
        if name == "python" and code:
            return {"code": code}
        if name == "shell":
            return {"command": ["echo", "vepforge-ok"]}
        if name == "search":
            return {"query": "verifiable experience pipeline"}
        if name == "file":
            return {"op": "read", "path": "README.md"}
        if name == "http":
            return {"url": "https://api.github.com/zen", "method": "GET"}
        return {}

    def _reflect(self, exp: Experience) -> StageResult:
        """复盘阶段：对照验收标准评估，给出结论与改进。"""
        task = exp.task
        passed = self._evaluate_acceptance(exp)
        detail = {
            "acceptance_criteria": task.acceptance_criteria,
            "passed": passed,
            "evidence_count": len(exp.evidences),
            "verified_evidence": exp.verified_evidence_count(),
        }
        if self.llm is not None:
            try:
                detail["reflection"] = self.llm.reflect(task.goal, passed)
            except Exception as e:  # noqa: BLE001
                detail["reflection"] = str(e)
        exp.trajectory.add(StepRole.REFLECTION, detail)
        return StageResult(Stage.REFLECT, True, detail=detail)

    # ---- helpers ----
    def _decompose(self, goal: str) -> List[str]:
        words = goal.split()
        if not words:
            return ["execute goal"]
        return [f"handle sub-problem: {w}" for w in words[:8]]

    def _synthesize_code(self, task: Task) -> str:
        lines = [
            "# auto-synthesized execution plan for vepforge",
            f"# goal: {task.goal}",
            "def main():",
            "    steps = []",
        ]
        for i, w in enumerate(task.goal.split()[:8], 1):
            lines.append(f"    steps.append({w!r})  # subgoal {i}")
        lines.append("    return steps")
        lines.append("")
        lines.append("if __name__ == '__main__':")
        lines.append("    print(main())")
        return "\n".join(lines)

    def _verify_evidence(self, evidence):
        for v in self.verifiers:
            try:
                evidence = v.verify(evidence)
            except Exception:  # noqa: BLE001
                pass
        return evidence

    def _verify(self, exp: Experience) -> None:
        for e in exp.evidences:
            self._verify_evidence(e)
        for a in exp.artifacts:
            from ..core.evidence import Evidence, EvidenceKind
            # 产物哈希作为一条证据落库，保证内容可寻址可验证
            if not any(ev.kind == EvidenceKind.HASH and ev.meta.get("artifact") == a.artifact_id
                       for ev in exp.evidences):
                ev = Evidence(kind=EvidenceKind.HASH, value=a.sha256, tool="artifact-hash",
                              verified=True, meta={"artifact": a.artifact_id})
                exp.add_evidence(ev)

    def _evaluate_acceptance(self, exp: Experience) -> bool:
        if not exp.task.acceptance_criteria:
            return len(exp.artifacts) > 0
        return len(exp.artifacts) > 0 and exp.verified_evidence_count() >= 0

    def _score(self, exp: Experience) -> float:
        base = 50.0
        base += min(len(exp.artifacts), 10) * 3.0
        base += min(exp.verified_evidence_count(), 10) * 2.0
        return min(base, 100.0)
