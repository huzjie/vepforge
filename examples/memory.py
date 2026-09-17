# -*- coding: utf-8 -*-
"""展示经验存储与检索。"""
import tempfile
import os

from vepforge import Task, VerifiableExperiencePipeline
from vepforge.memory import MemoryStore, Retrieval

with tempfile.TemporaryDirectory() as d:
    store = MemoryStore(path=os.path.join(d, "exp.json"))
    pipe = VerifiableExperiencePipeline()
    exp = pipe.run(Task(goal="aggregate CSV and summarize"))
    store.save(exp)

    ret = Retrieval(store)
    hits = ret.search("aggregate CSV")
    for h in hits:
        print(h["experience_id"], round(h["score"], 3), h["goal"])
