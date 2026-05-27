#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path


ENV_VARS = [
    ("QWEN3_VL_ROOT", "local Qwen3-VL checkout"),
    ("STARVLA_ROOT", "local StarVLA checkout"),
    ("RETHINK_DATA_ROOT", "prepared manifests and datasets"),
    ("RETHINK_OUTPUT_ROOT", "checkpoints, logs, and generated results"),
]


def describe_env_var(name: str, description: str) -> tuple[str, bool]:
    value = os.environ.get(name)
    if not value:
        return f"{name}: MISSING ({description})", False

    path = Path(value).expanduser()
    if path.exists():
        return f"{name}: {path} [exists]", True
    return f"{name}: {path} [missing path]", False


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local paths for Rethink VLA Initialization.")
    parser.add_argument("--dry-run", action="store_true", help="Report missing variables without failing.")
    args = parser.parse_args()

    all_ok = True
    for name, description in ENV_VARS:
        line, ok = describe_env_var(name, description)
        print(line)
        all_ok = all_ok and ok

    if args.dry_run:
        print("Dry run: environment report complete.")
        return 0

    if not all_ok:
        print("Environment check failed. Set missing variables or create missing paths.")
        return 1

    print("Environment check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

