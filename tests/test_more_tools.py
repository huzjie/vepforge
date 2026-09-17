# -*- coding: utf-8 -*-
from vepforge.tools import JsonTool, CsvTool, RegexTool, CalcTool, TimeTool


def test_json():
    r = JsonTool().run({"text": '{"a": 1}'})
    assert r.ok and r.data["parsed"]["a"] == 1


def test_csv():
    r = CsvTool().run({"text": "name,value\nfoo,1\nbar,3"})
    assert r.ok and r.data["rows"] == 2


def test_regex():
    r = RegexTool().run({"text": "a1 b2 c3", "pattern": r"\d"})
    assert r.ok and r.data["count"] == 3


def test_calc():
    r = CalcTool().run({"expression": "2 + 3 * 4"})
    assert r.ok and r.data["value"] == 14


def test_time():
    r = TimeTool().run({})
    assert r.ok and "epoch" in r.data
