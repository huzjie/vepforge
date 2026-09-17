# -*- coding: utf-8 -*-
"""vepforge — Verifiable Experience Pipeline 驱动的长程自主智能体执行平台。

基于上海 AI Lab 开源 Atria Dawn Preview（744B MoE agentic 模型）的核心理念：
将「分析 → 编码 → 执行 → 复盘」长程闭环 grounding 到真实可执行环境，
把任务目标、智能体轨迹、中间产物、外部证据四者用可验证的方式连接起来。

四大可验证实体：
- Task       任务目标（goal, constraints, acceptance criteria）
- Trajectory 智能体轨迹（每一步 action/observation/thought）
- Artifact   中间产物（代码、数据、报告等可寻址产物）
- Evidence   外部证据（工具真实执行结果、哈希、退出码）

用法：
    from vepforge import VerifiableExperiencePipeline, Task
    task = Task(goal="...")
    pipe = VerifiableExperiencePipeline()
    exp = pipe.run(task)
"""

__version__ = "0.1.0"
__author__ = "vepforge contributors"
__license__ = "MIT"

from .core.task import Task, TaskStatus
from .core.trajectory import Trajectory, Step, StepRole
from .core.artifact import Artifact, ArtifactKind
from .core.evidence import Evidence, EvidenceKind
from .core.experience import Experience, ExperienceStatus
from .pipeline.vep import VerifiableExperiencePipeline
from .verifier.registry import VerifierRegistry

__all__ = [
    "Task", "TaskStatus",
    "Trajectory", "Step", "StepRole",
    "Artifact", "ArtifactKind",
    "Evidence", "EvidenceKind",
    "Experience", "ExperienceStatus",
    "VerifiableExperiencePipeline",
    "VerifierRegistry",
    "__version__",
]
