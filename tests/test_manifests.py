import json

import pytest

from rethink_vla_init.manifests import ManifestError, load_manifest


def write_manifest(tmp_path, payload):
    path = tmp_path / "manifest.yaml"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_load_manifest_accepts_valid_entries(tmp_path):
    manifest_path = write_manifest(
        tmp_path,
        {
            "entries": [
                {
                    "domain": "grounding",
                    "name": "robopoint_sample",
                    "path": "grounding/robopoint_sample.jsonl",
                    "format": "qwen_vl_json",
                    "samples": 1000,
                    "weight": 1.0,
                    "license": "dataset-specific",
                }
            ]
        },
    )

    manifest = load_manifest(manifest_path, data_root=tmp_path / "data")

    assert len(manifest.entries) == 1
    entry = manifest.entries[0]
    assert entry.domain == "grounding"
    assert entry.name == "robopoint_sample"
    assert entry.resolved_path == tmp_path / "data" / "grounding/robopoint_sample.jsonl"


def test_load_manifest_rejects_unknown_domain(tmp_path):
    manifest_path = write_manifest(
        tmp_path,
        {
            "entries": [
                {
                    "domain": "unknown_domain",
                    "name": "bad",
                    "path": "bad.jsonl",
                    "format": "jsonl",
                    "samples": 1,
                }
            ]
        },
    )

    with pytest.raises(ManifestError, match="unknown domain"):
        load_manifest(manifest_path)


def test_load_manifest_rejects_negative_samples(tmp_path):
    manifest_path = write_manifest(
        tmp_path,
        {
            "entries": [
                {
                    "domain": "spatial",
                    "name": "bad_samples",
                    "path": "spatial/bad.jsonl",
                    "format": "jsonl",
                    "samples": -1,
                }
            ]
        },
    )

    with pytest.raises(ManifestError, match="non-negative"):
        load_manifest(manifest_path)


def test_load_manifest_rejects_duplicate_names_within_domain(tmp_path):
    manifest_path = write_manifest(
        tmp_path,
        {
            "entries": [
                {
                    "domain": "temporal_understanding",
                    "name": "video_sample",
                    "path": "temporal/a.jsonl",
                    "format": "jsonl",
                    "samples": 10,
                },
                {
                    "domain": "temporal_understanding",
                    "name": "video_sample",
                    "path": "temporal/b.jsonl",
                    "format": "jsonl",
                    "samples": 20,
                },
            ]
        },
    )

    with pytest.raises(ManifestError, match="duplicate"):
        load_manifest(manifest_path)

