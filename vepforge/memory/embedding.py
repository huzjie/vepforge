# -*- coding: utf-8 -*-
"""TextEmbedder：文本向量化（哈希 bag-of-words，零依赖）。"""
from __future__ import annotations

import hashlib
import math
from typing import Dict, List


class TextEmbedder:
    """确定性文本向量化：哈希词袋 + L2 归一化。

    无外部依赖，同一文本恒得同一向量，适合做可验证的语义检索。
    维度默认 256。
    """

    def __init__(self, dim: int = 256):
        self.dim = dim

    def embed(self, text: str) -> List[float]:
        vec = [0.0] * self.dim
        for token in self._tokens(text):
            h = hashlib.md5(token.encode("utf-8")).digest()
            idx = int.from_bytes(h[:2], "little") % self.dim
            sign = 1.0 if h[2] % 2 == 0 else -1.0
            vec[idx] += sign
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    @staticmethod
    def _tokens(text: str) -> List[str]:
        return text.lower().replace(",", " ").split()

    def cosine(self, a: List[float], b: List[float]) -> float:
        return sum(x * y for x, y in zip(a, b))
