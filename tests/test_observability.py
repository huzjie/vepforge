# -*- coding: utf-8 -*-
from vepforge.observability import MetricsCollector, Tracer


def test_metrics():
    m = MetricsCollector()
    m.incr("a", 2)
    m.gauge("g", 1.5)
    s = m.snapshot()
    assert s["counters"]["a"] == 2
    assert s["gauges"]["g"] == 1.5


def test_tracer():
    t = Tracer()
    t.start("root")
    t.start("child")
    t.end()
    t.end()
    d = t.to_dict()
    assert len(d["traces"]) == 1
    assert len(d["traces"][0]["children"]) == 1
