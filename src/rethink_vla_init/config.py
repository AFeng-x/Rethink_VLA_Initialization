from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


SUPPORTED_RECIPE_KINDS = {
    "stage1_qwen3vl",
    "stage2_starvla",
    "robot_pretraining",
}


class ConfigError(ValueError):
    """Raised when a recipe config is malformed."""


@dataclass(frozen=True)
class Recipe:
    kind: str
    name: str
    payload: dict[str, Any]
    path: Path | None = None


def load_json_compatible_yaml(path: str | Path) -> dict[str, Any]:
    """Load a JSON-compatible YAML file with the Python standard library."""

    config_path = Path(path)
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(
            f"{config_path} must use JSON-compatible YAML syntax: {exc.msg}"
        ) from exc
    except OSError as exc:
        raise ConfigError(f"could not read config {config_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigError(f"{config_path} must contain a top-level object")
    return data


def load_recipe(path: str | Path) -> Recipe:
    payload = load_json_compatible_yaml(path)
    kind = payload.get("kind")
    if not isinstance(kind, str) or not kind:
        raise ConfigError("recipe config must define string field 'kind'")
    if kind not in SUPPORTED_RECIPE_KINDS:
        raise ConfigError(f"unsupported recipe kind '{kind}'")

    name = payload.get("name")
    if not isinstance(name, str) or not name:
        raise ConfigError("recipe config must define string field 'name'")

    return Recipe(kind=kind, name=name, payload=payload, path=Path(path))

