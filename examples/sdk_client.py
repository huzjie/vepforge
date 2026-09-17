# -*- coding: utf-8 -*-
"""展示 SDK 客户端（需先启动 serve）。"""
from vepforge.sdk import VepforgeClient

client = VepforgeClient("http://127.0.0.1:8000")
print(client.health())
exp = client.run("verify the pipeline via SDK",
                 acceptance_criteria=["artifact"])
print(exp["status"], exp["score"])
