# -*- coding: utf-8 -*-
"""ModelCatalog：加载 models/*.yaml 模型卡。"""
from __future__ import annotations

import glob
import os
from typing import Any, Dict, List, Optional


class ModelCatalog:
    """模型卡目录，加载并索引包内 models 目录的 YAML。"""

    def __init__(self, models_dir: Optional[str] = None):
        if models_dir is None:
            models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
        self.models_dir = os.path.abspath(models_dir)
        self._models: Dict[str, Dict[str, Any]] = {}

    def load(self) -> Dict[str, Dict[str, Any]]:
        try:
            import yaml  # noqa: F401
        except ImportError:
            return {}
        self._models = {}
        for path in glob.glob(os.path.join(self.models_dir, "*.yaml")):
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data and "name" in data:
                self._models[data["name"]] = data
        return self._models

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        if not self._models:
            self.load()
        return self._models.get(name)

    def list(self) -> List[str]:
        if not self._models:
            self.load()
        return sorted(self._models.keys())
