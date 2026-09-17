# -*- coding: utf-8 -*-
from vepforge.tools import PythonExecTool, FileTool, SearchTool


def test_python_exec():
    t = PythonExecTool(python="python")
    r = t.run({"code": "print('hi')"})
    assert r.exit_code == 0 and "hi" in r.stdout


def test_search():
    t = SearchTool(corpus=[{"text": "the quick brown fox"}])
    r = t.run({"query": "quick fox"})
    assert r.ok and len(r.data["hits"]) == 1
