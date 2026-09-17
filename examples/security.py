# -*- coding: utf-8 -*-
"""展示安全模块。"""
from vepforge.security import SandboxPolicy, sanitize_command

p = SandboxPolicy()
print(p.allows_command("echo"), p.allows_command("rm"))
print(sanitize_command("echo hi; rm -rf /"))
