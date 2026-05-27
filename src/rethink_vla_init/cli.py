from __future__ import annotations

import argparse
import shlex
from pathlib import Path
from typing import Sequence

from .analysis import render_table_from_csv
from .config import load_recipe
from .recipes import (
    render_robot_pretraining_command,
    render_stage1_command,
    render_stage2_command,
)


def command_to_text(command: Sequence[str]) -> str:
    return shlex.join(list(command))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rethink-vla-init")
    subparsers = parser.add_subparsers(dest="command", required=True)

    stage1 = subparsers.add_parser("render-stage1")
    stage1.add_argument("recipe")
    stage1.add_argument("--qwen-root", required=True)

    stage2 = subparsers.add_parser("render-stage2")
    stage2.add_argument("recipe")
    stage2.add_argument("--starvla-root", required=True)

    robot = subparsers.add_parser("render-robot")
    robot.add_argument("recipe")
    robot.add_argument("--starvla-root", required=True)

    table = subparsers.add_parser("make-table")
    table.add_argument("--input", required=True)
    table.add_argument("--table", required=True)

    args = parser.parse_args(argv)

    if args.command == "render-stage1":
        recipe = load_recipe(args.recipe)
        print(command_to_text(render_stage1_command(recipe, qwen_root=args.qwen_root)))
        return 0

    if args.command == "render-stage2":
        recipe = load_recipe(args.recipe)
        print(command_to_text(render_stage2_command(recipe, starvla_root=args.starvla_root)))
        return 0

    if args.command == "render-robot":
        recipe = load_recipe(args.recipe)
        print(command_to_text(render_robot_pretraining_command(recipe, starvla_root=args.starvla_root)))
        return 0

    if args.command == "make-table":
        print(render_table_from_csv(Path(args.input), table_name=args.table), end="")
        return 0

    parser.error(f"unsupported command {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

