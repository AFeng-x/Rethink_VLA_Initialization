from rethink_vla_init.config import Recipe
from rethink_vla_init.recipes import (
    render_robot_pretraining_command,
    render_stage1_command,
    render_stage2_command,
)


def test_render_stage1_command_uses_qwen_root_and_recipe_fields():
    recipe = Recipe(
        kind="stage1_qwen3vl",
        name="grounding_lora",
        payload={
            "kind": "stage1_qwen3vl",
            "name": "grounding_lora",
            "model": "Qwen/Qwen3-VL-4B-Instruct",
            "data_manifest": "examples/manifests/embodied_vqa_manifest.example.yaml",
            "output_dir": "stage1/grounding_lora",
            "entrypoint": "qwenvl/train/train_qwen.py",
            "training": {"update": "lora", "lora_rank": 16, "lora_alpha": 32},
            "args": {"num_train_epochs": 1, "learning_rate": "5e-5"},
        },
    )

    command = render_stage1_command(recipe, qwen_root="/opt/qwen3-vl")
    text = " ".join(command)

    assert command[0] == "python"
    assert "/opt/qwen3-vl/qwenvl/train/train_qwen.py" in text
    assert "--model_name_or_path Qwen/Qwen3-VL-4B-Instruct" in text
    assert "--lora_rank 16" in text
    assert "--learning_rate 5e-5" in text


def test_render_stage2_command_uses_starvla_root_and_overrides():
    recipe = Recipe(
        kind="stage2_starvla",
        name="libero10_oft",
        payload={
            "kind": "stage2_starvla",
            "name": "libero10_oft",
            "entrypoint": "starVLA/training/train_starvla.py",
            "config_name": "libero10_oft",
            "benchmark": "libero10",
            "action_head": "oft_mlp",
            "init_checkpoint": "stage1/grounding_lora",
            "overrides": {"training_steps": 50000, "batch_size": 128},
        },
    )

    command = render_stage2_command(recipe, starvla_root="/opt/starvla")
    text = " ".join(command)

    assert "/opt/starvla/starVLA/training/train_starvla.py" in text
    assert "--config-name libero10_oft" in text
    assert "benchmark=libero10" in text
    assert "training_steps=50000" in text


def test_render_robot_pretraining_command_includes_robot_recipe_fields():
    recipe = Recipe(
        kind="robot_pretraining",
        name="agibot_robot_only_lora_r64",
        payload={
            "kind": "robot_pretraining",
            "name": "agibot_robot_only_lora_r64",
            "entrypoint": "starVLA/training/train_starvla.py",
            "config_name": "agibot_pretrain",
            "pretrain_data": "agibot",
            "init_checkpoint": "base",
            "output_dir": "robot_pretraining/agibot_robot_only_lora_r64",
            "overrides": {"lora_rank": 64, "lora_alpha": 128, "training_steps": 100000},
        },
    )

    command = render_robot_pretraining_command(recipe, starvla_root="/opt/starvla")
    text = " ".join(command)

    assert "--config-name agibot_pretrain" in text
    assert "pretrain_data=agibot" in text
    assert "lora_rank=64" in text
    assert "training_steps=100000" in text

