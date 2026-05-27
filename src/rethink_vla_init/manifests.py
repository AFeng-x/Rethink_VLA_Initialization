from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import ConfigError, load_json_compatible_yaml


ALLOWED_DOMAINS = {
    "spatial",
    "grounding",
    "plan_reasoning",
    "camera_prediction",
    "egocentric_understanding",
    "temporal_understanding",
    "action_ntp",
}


class ManifestError(ValueError):
    """Raised when a data manifest is malformed."""


@dataclass(frozen=True)
class ManifestEntry:
    domain: str
    name: str
    path: Path
    format: str
    samples: int
    weight: float | None = None
    license: str | None = None
    resolved_path: Path | None = None


@dataclass(frozen=True)
class Manifest:
    entries: list[ManifestEntry]
    path: Path


def _require_string(entry: dict[str, Any], field: str, index: int) -> str:
    value = entry.get(field)
    if not isinstance(value, str) or not value:
        raise ManifestError(f"entry {index} must define non-empty string field '{field}'")
    return value


def load_manifest(
    path: str | Path,
    *,
    data_root: str | Path | None = None,
    require_paths: bool = False,
) -> Manifest:
    try:
        payload = load_json_compatible_yaml(path)
    except ConfigError as exc:
        raise ManifestError(str(exc)) from exc

    raw_entries = payload.get("entries")
    if not isinstance(raw_entries, list):
        raise ManifestError("manifest must define list field 'entries'")

    root = Path(data_root) if data_root is not None else None
    entries: list[ManifestEntry] = []
    seen: set[tuple[str, str]] = set()

    for index, raw in enumerate(raw_entries):
        if not isinstance(raw, dict):
            raise ManifestError(f"entry {index} must be an object")

        domain = _require_string(raw, "domain", index)
        if domain not in ALLOWED_DOMAINS:
            raise ManifestError(f"entry {index} has unknown domain '{domain}'")

        name = _require_string(raw, "name", index)
        key = (domain, name)
        if key in seen:
            raise ManifestError(f"duplicate manifest entry '{name}' in domain '{domain}'")
        seen.add(key)

        rel_path = Path(_require_string(raw, "path", index))
        resolved_path = rel_path if rel_path.is_absolute() else (root / rel_path if root else rel_path)

        fmt = _require_string(raw, "format", index)
        samples = raw.get("samples")
        if not isinstance(samples, int) or samples < 0:
            raise ManifestError(f"entry {index} field 'samples' must be a non-negative integer")

        weight = raw.get("weight")
        if weight is not None and not isinstance(weight, (int, float)):
            raise ManifestError(f"entry {index} field 'weight' must be numeric when provided")

        license_note = raw.get("license")
        if license_note is not None and not isinstance(license_note, str):
            raise ManifestError(f"entry {index} field 'license' must be a string when provided")

        if require_paths and not resolved_path.exists():
            raise ManifestError(f"entry {index} path does not exist: {resolved_path}")

        entries.append(
            ManifestEntry(
                domain=domain,
                name=name,
                path=rel_path,
                format=fmt,
                samples=samples,
                weight=float(weight) if weight is not None else None,
                license=license_note,
                resolved_path=resolved_path,
            )
        )

    return Manifest(entries=entries, path=Path(path))

