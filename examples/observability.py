# -*- coding: utf-8 -*-
"""展示可观测性：指标 + 追踪。"""
from vepforge.observability import MetricsCollector, Tracer

m = MetricsCollector()
with m.time("task_total"):
    m.incr("task_count")
    m.gauge("queue_depth", 3.5)
print(m.snapshot())

t = Tracer()
span = t.start("pipeline", task="demo")
child = t.start("execute", tool="python")
t.end()
t.end()
print(t.to_dict())
