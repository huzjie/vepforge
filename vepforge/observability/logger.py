# -*- coding: utf-8 -*-
"""日志工具。"""
from __future__ import annotations

import logging
import sys
from typing import Optional

_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def get_logger(name: str = "vepforge", level: int = logging.INFO,
               stream=None) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(stream or sys.stderr)
        handler.setFormatter(logging.Formatter(_FORMAT))
        logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger
