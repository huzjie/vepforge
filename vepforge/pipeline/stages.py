# -*- coding: utf-8 -*-
"""四阶段闭环：分析 → 编码 → 执行 → 复盘。"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class Stage(str, Enum):
    ANALYZE = "analyze"
    CODE = "code"
    EXECUTE = "execute"
    REFLECT = "reflect"


@dataclass
class StageResult:
    """阶段执行结果。"""

    stage: Stage
    ok: bool
    detail: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


STAGE_ORDER = [Stage.ANALYZE, Stage.CODE, Stage.EXECUTE, Stage.REFLECT]
