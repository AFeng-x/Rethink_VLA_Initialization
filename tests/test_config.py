import json

import pytest

from rethink_vla_init.config import ConfigError, load_recipe


def write_recipe(tmp_path, payload):
    path = tmp_path / "recipe.yaml"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_load_recipe_accepts_stage1_recipe(tmp_path):
    path = write_recipe(
        tmp_path,
        {
            "kind": "stage1_qwen3vl",
            "name": "qwen3vl_4b_grounding_lora",
            "model": "Qwen/Qwen3-VL-4B-Instruct",
            "data_manifest": "examples/manifests/embodied_vqa_manifest.example.yaml",
            "output_dir": "stage1/qwen3vl_4b_grounding_lora",
            "entrypoint": "qwenvl/train/train_qwen.py",
            "training": {"update": "lora", "lora_rank": 16, "lora_alpha": 32},
        },
    )

    recipe = load_recipe(path)

    assert recipe.kind == "stage1_qwen3vl"
    assert recipe.name == "qwen3vl_4b_grounding_lora"
    assert recipe.payload["training"]["update"] == "lora"


def test_load_recipe_rejects_missing_kind(tmp_path):
    path = write_recipe(tmp_path, {"name": "missing_kind"})

    with pytest.raises(ConfigError, match="kind"):
        load_recipe(path)


def test_load_recipe_rejects_unsupported_kind(tmp_path):
    path = write_recipe(tmp_path, {"kind": "unsupported", "name": "bad"})

    with pytest.raises(ConfigError, match="unsupported"):
        load_recipe(path)

