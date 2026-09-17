# -*- coding: utf-8 -*-
"""MemoryStore：经验持久化（JSON 文件 + 可选 SQLite）。"""
from __future__ import annotations

import json
import os
import sqlite3
import threading
from typing import Any, Dict, List, Optional

from ..core.experience import Experience


class MemoryStore:
    """经验存储，默认 JSON 文件，可选 SQLite 后端做索引。

    JSON 后端零依赖、可审计；SQLite 后端用于大规模经验检索。
    """

    def __init__(self, path: str = "vepforge_experiences.json",
                 use_sqlite: bool = False, sqlite_path: str = "vepforge.db"):
        self.path = path
        self._lock = threading.Lock()
        self._use_sqlite = use_sqlite
        self._sqlite_path = sqlite_path
        if use_sqlite:
            self._init_sqlite()

    def _init_sqlite(self) -> None:
        conn = sqlite3.connect(self._sqlite_path)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS experiences ("
            "experience_id TEXT PRIMARY KEY, status TEXT, score REAL,"
            " payload TEXT)"
        )
        conn.commit()
        conn.close()

    def save(self, exp: Experience) -> None:
        data = exp.to_dict()
        with self._lock:
            if self._use_sqlite:
                conn = sqlite3.connect(self._sqlite_path)
                conn.execute(
                    "INSERT OR REPLACE INTO experiences "
                    "(experience_id, status, score, payload) VALUES (?,?,?,?)",
                    (exp.experience_id, exp.status.value, exp.score,
                     json.dumps(data, ensure_ascii=False)),
                )
                conn.commit()
                conn.close()
            else:
                all_data = self._load_all()
                all_data[exp.experience_id] = data
                self._write_all(all_data)

    def load(self, experience_id: str) -> Optional[Experience]:
        with self._lock:
            if self._use_sqlite:
                conn = sqlite3.connect(self._sqlite_path)
                cur = conn.execute(
                    "SELECT payload FROM experiences WHERE experience_id=?",
                    (experience_id,))
                row = cur.fetchone()
                conn.close()
                return Experience.from_dict(json.loads(row[0])) if row else None
            all_data = self._load_all()
            if experience_id in all_data:
                return Experience.from_dict(all_data[experience_id])
            return None

    def list(self) -> List[Dict[str, Any]]:
        with self._lock:
            if self._use_sqlite:
                conn = sqlite3.connect(self._sqlite_path)
                cur = conn.execute(
                    "SELECT experience_id, status, score FROM experiences")
                rows = [{"experience_id": r[0], "status": r[1], "score": r[2]}
                        for r in cur.fetchall()]
                conn.close()
                return rows
            return [{"experience_id": k, "status": v.get("status"),
                     "score": v.get("score")} for k, v in self._load_all().items()]

    def _load_all(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_all(self, data: Dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
