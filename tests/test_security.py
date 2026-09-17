# -*- coding: utf-8 -*-
from vepforge.security import SandboxPolicy, sanitize_command


def test_policy():
    p = SandboxPolicy()
    assert p.allows_command("echo")
    assert not p.allows_command("rm")


def test_sanitize():
    assert "rm" in sanitize_command("rm -rf /")
    assert ";" not in sanitize_command("a;b")
