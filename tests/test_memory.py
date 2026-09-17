# -*- coding: utf-8 -*-
import os
import tempfile

from vepforge import Task, VerifiableExperiencePipeline
from vepforge.memory import MemoryStore, Retrieval


def test_store_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        store = MemoryStore(path=os.path.join(d, "e.json"))
        exp = VerifiableExperiencePipeline().run(Task(goal="hello"))
        store.save(exp)
        loaded = store.load(exp.experience_id)
        assert loaded is not None
        assert loaded.task.goal == "hello"
        assert len(store.list()) == 1


def test_retrieval():
    with tempfile.TemporaryDirectory() as d:
        store = MemoryStore(path=os.path.join(d, "e.json"))
        pipe = VerifiableExperiencePipeline()
        store.save(pipe.run(Task(goal="aggregate CSV data")))
        store.save(pipe.run(Task(goal="write a poem")))
        ret = Retrieval(store)
        hits = ret.search("aggregate CSV")
        assert hits and hits[0]["goal"] == "aggregate CSV data"
