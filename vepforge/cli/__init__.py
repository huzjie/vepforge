# -*- coding: utf-8 -*-
"""cli 包：命令行入口。"""


def main():
    from .main import main as _run
    return _run()
