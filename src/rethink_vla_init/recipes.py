from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import ConfigError, Recipe


def _entrypoint(root: str | Path, relative_path: str) -> str:
    return str(Path(root) / relative_path)


def _append_mapping_args(command: list[str], values: dict[str, Any], *, prefix: str = "--") -> None:
    for key, value in values.items():
        command.extend([f"{prefix}{key}", str(value)])


def _append_override_args(command: list[str], overrides: dict[str, Any]) -> None:
    for key, value in overrides.items():
        command.append(f"{key}={value}")


def _require_kind(recipe: Recipe, expected: str) -> None:
    if recipe.kind != expected:
        raise ConfigError(f"expected recipe kind '{expected}', got '{recipe.kind}'")


def _payload_string(recipe: Recipe, key: str, default: str | None = None) -> str:
    value = recipe.payload.get(key, default)
    if not isinstance(value, str) or not value:
        raise ConfigError(f"recipe '{recipe.name}' must define string field '{key}'")
    return value


def render_stage1_command(recipe: Recipe, *, qwen_root: str | Path) -> list[str]:
    _require_kind(recipe, "stage1_qwen3vl")
    entrypoint = _payload_string(recipe, "entrypoint", "qwenvl/train/train_qwen.py")
    training = recipe.payload.get("training", {})
    if not isinstance(training, dict):
        raise ConfigError(f"recipe '{recipe.name}' field 'training' must be an object")

    command = [
        "python",
        _entrypoint(qwen_root, entrypoint),
        "--model_name_or_path",
        _payload_string(recipe, "model"),
        "--data_path",
        _payload_string(recipe, "data_manifest"),
        "--output_dir",
        _payload_string(recipe, "output_dir"),
        "--update_strategy",
        str(training.get("update", "lora")),
    ]

    if "lora_rank" in training:
        command.extend(["--lora_rank", str(training["lora_rank"])])
    if "lora_alpha" in training:
        command.extend(["--lora_alpha", str(training["lora_alpha"])])

    args = recipe.payload.get("args", {})
    if args:
        if not isinstance(args, dict):
            raise ConfigError(f"recipe '{recipe.name}' field 'args' must be an object")
        _append_mapping_args(command, args)

    return command


def render_stage2_command(recipe: Recipe, *, starvla_root: str | Path) -> list[str]:
    _require_kind(recipe, "stage2_starvla")
    entrypoint = _payload_string(recipe, "entrypoint", "starVLA/training/train_starvla.py")

    command = [
        "python",
        _entrypoint(starvla_root, entrypoint),
        "--config-name",
        _payload_string(recipe, "config_name"),
        f"benchmark={_payload_string(recipe, 'benchmark')}",
        f"action_head={_payload_string(recipe, 'action_head')}",
        f"init_checkpoint={_payload_string(recipe, 'init_checkpoint')}",
    ]

    overrides = recipe.payload.get("overrides", {})
    if overrides:
        if not isinstance(overrides, dict):
            raise ConfigError(f"recipe '{recipe.name}' field 'overrides' must be an object")
        _append_override_args(command, overrides)

    return command


def render_robot_pretraining_command(recipe: Recipe, *, starvla_root: str | Path) -> list[str]:
    _require_kind(recipe, "robot_pretraining")
    entrypoint = _payload_string(recipe, "entrypoint", "starVLA/training/train_starvla.py")

    command = [
        "python",
        _entrypoint(starvla_root, entrypoint),
        "--config-name",
        _payload_string(recipe, "config_name"),
        f"pretrain_data={_payload_string(recipe, 'pretrain_data')}",
        f"init_checkpoint={_payload_string(recipe, 'init_checkpoint')}",
        f"output_dir={_payload_string(recipe, 'output_dir')}",
    ]

    overrides = recipe.payload.get("overrides", {})
    if overrides:
        if not isinstance(overrides, dict):
            raise ConfigError(f"recipe '{recipe.name}' field 'overrides' must be an object")
        _append_override_args(command, overrides)

    return command


def render_command(recipe: Recipe, *, qwen_root: str | Path = "", starvla_root: str | Path = "") -> list[str]:
    if recipe.kind == "stage1_qwen3vl":
        return render_stage1_command(recipe, qwen_root=qwen_root)
    if recipe.kind == "stage2_starvla":
        return render_stage2_command(recipe, starvla_root=starvla_root)
    if recipe.kind == "robot_pretraining":
        return render_robot_pretraining_command(recipe, starvla_root=starvla_root)
    raise ConfigError(f"unsupported recipe kind '{recipe.kind}'")

