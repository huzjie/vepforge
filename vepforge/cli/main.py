# -*- coding: utf-8 -*-
"""命令行入口：doctor / run / models / tools。"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional


def _demo_pipeline():
    from ..pipeline.vep import VerifiableExperiencePipeline
    from ..llm.mock import MockLLM
    from ..verifier.registry import VerifierRegistry
    return VerifiableExperiencePipeline(
        llm=MockLLM(),
        verifiers=VerifierRegistry.default_instances(),
    )


def _cmd_doctor(cfg: Dict[str, Any], args: argparse.Namespace) -> int:
    print("[doctor] vepforge self-check")
    from .. import __version__
    print(f"  version: {__version__}")
    from ..verifier.registry import VerifierRegistry
    print(f"  verifiers: {VerifierRegistry.list()}")
    from ..tools.registry import ToolRegistry
    print(f"  tools: {ToolRegistry.list()}")
    from ..agents.registry import AgentRegistry
    print(f"  agents: {AgentRegistry.list()}")
    from ..llm.registry import LLMRegistry
    print(f"  llm backends: {LLMRegistry.list()}")
    # 冒烟：跑一个最小任务
    pipe = _demo_pipeline()
    from ..core.task import Task
    exp = pipe.run(Task(goal="verify the pipeline works",
                        acceptance_criteria=["at least one artifact"]))
    print(f"  smoke: status={exp.status.value} artifacts={len(exp.artifacts)} "
          f"evidences={len(exp.evidences)} score={exp.score}")
    return 0 if exp.status.value == "succeeded" else 1


def _cmd_run(cfg: Dict[str, Any], args: argparse.Namespace) -> int:
    goal = args.goal
    if not goal:
        print("error: --goal required", file=sys.stderr)
        return 2
    from ..core.task import Task
    pipe = _demo_pipeline()
    exp = pipe.run(Task(goal=goal, acceptance_criteria=args.criteria or []))
    print(json.dumps(exp.to_dict(), ensure_ascii=False, indent=2))
    return 0 if exp.status.value == "succeeded" else 1


def _cmd_models(cfg: Dict[str, Any], args: argparse.Namespace) -> int:
    from ..catalog.loader import ModelCatalog
    cat = ModelCatalog()
    models = cat.load()
    for name in cat.list():
        m = models.get(name, {})
        print(f"- {name}  ({m.get('organization', '?')})  "
              f"{m.get('total_parameters', m.get('role', ''))}")
    return 0


def _cmd_tools(cfg: Dict[str, Any], args: argparse.Namespace) -> int:
    from ..tools.registry import ToolRegistry
    for name in ToolRegistry.list():
        cls = ToolRegistry.get(name)
        print(f"- {name}: {cls.description}")
    return 0


def _cmd_serve(cfg: Dict[str, Any], args: argparse.Namespace) -> int:
    import uvicorn
    from ..serving.app import create_app
    from ..llm.mock import MockLLM
    app = create_app(pipeline=_demo_pipeline(), llm=MockLLM())
    uvicorn.run(app, host=args.host, port=args.port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vepforge", description="vepforge CLI")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("doctor", help="run self-check")

    run_p = sub.add_parser("run", help="run a task")
    run_p.add_argument("--goal", type=str, default="")
    run_p.add_argument("--criteria", type=str, action="append", default=[])

    sub.add_parser("models", help="list model cards")
    sub.add_parser("tools", help="list tools")

    serve_p = sub.add_parser("serve", help="start FastAPI server")
    serve_p.add_argument("--host", default="127.0.0.1")
    serve_p.add_argument("--port", type=int, default=8000)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0
    dispatch = {
        "doctor": _cmd_doctor,
        "run": _cmd_run,
        "models": _cmd_models,
        "tools": _cmd_tools,
        "serve": _cmd_serve,
    }
    handler = dispatch[args.command]
    return handler({}, args)


if __name__ == "__main__":
    sys.exit(main())
