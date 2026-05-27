# Rethink VLA Initialization Repository Design

Date: 2026-05-27

## Goal

Build an open-source reproduction and experiment-recipe repository for the paper
"Rethinking VLM Representation for VLA Initialization."

The repository exposes the paper's method layer:

- Stage-1 VLM adaptation recipes based on Qwen3-VL.
- Stage-2 VLA initialization and training recipes based on StarVLA.
- Robot-data pretraining recipes.
- Data manifest schemas for embodied VQA domains.
- Lightweight analysis tools for reproducing paper-style tables from result CSV files.

The repository must be useful to readers who want to understand, reproduce, or extend the study
without vendoring the full upstream Qwen3-VL or StarVLA codebases.

## Non-Goals

- Do not copy or fork Qwen3-VL trainer code into this repository.
- Do not copy or fork StarVLA trainer code into this repository.
- Do not provide private datasets, model checkpoints, or unpublished experiment logs.
- Do not hard-code local paths from the author's workstation.
- Do not claim one-command full reproduction when external upstream repositories and datasets are required.

## Upstream Dependencies

Users are expected to clone and install these repositories separately:

- Qwen3-VL: `https://github.com/QwenLM/Qwen3-VL`
- StarVLA: `https://github.com/starVLA/starVLA/tree/starVLA`

This repository will provide scripts that call into those projects through explicit environment variables:

- `QWEN3_VL_ROOT`: path to a local Qwen3-VL checkout.
- `STARVLA_ROOT`: path to a local StarVLA checkout.
- `RETHINK_DATA_ROOT`: path to data manifests and prepared datasets.
- `RETHINK_OUTPUT_ROOT`: path to checkpoints, logs, and generated result files.

## Repository Structure

```text
Rethink_VLA_Initialization/
  README.md
  LICENSE
  CITATION.cff
  pyproject.toml
  .gitignore
  docs/
    setup.md
    data.md
    stage1_vlm_adaptation.md
    stage2_vla_training.md
    robot_pretraining.md
    experiments.md
    results.md
  configs/
    stage1_qwen3vl/
      qwen3vl_4b_grounding_lora.yaml
      qwen3vl_4b_grounding_full_ft.yaml
      qwen3vl_4b_grounding_ego_lora.yaml
      domain_defaults.yaml
    stage2_starvla/
      libero10_oft.yaml
      simplerbridge_oft.yaml
      robocasa_oft.yaml
      libero10_diffusion.yaml
      robocasa_diffusion.yaml
    robot_pretraining/
      agibot_robot_only_lora_r64.yaml
      agibot_robot_vqa_lora_r64.yaml
      grounding_ego_then_agibot_lora_r64.yaml
    analysis/
      main_tables.yaml
  examples/
    manifests/
      embodied_vqa_manifest.example.yaml
    results/
      single_domain_results.example.csv
      robot_pretraining_results.example.csv
  scripts/
    setup/
      check_environment.py
    stage1/
      launch_qwen3vl_adaptation.sh
    stage2/
      launch_starvla_training.sh
    analysis/
      make_tables.py
  src/rethink_vla_init/
    __init__.py
    config.py
    manifests.py
    recipes.py
    analysis.py
  tests/
    test_config.py
    test_manifests.py
    test_analysis.py
```

## Stage-1 VLM Adaptation Design

Stage-1 configuration files describe the capability domain, update strategy, data manifest, and Qwen3-VL launch arguments.

The launch script will:

1. Validate `QWEN3_VL_ROOT`.
2. Validate the selected YAML config.
3. Resolve the data manifest into Qwen3-VL-compatible train files.
4. Print and execute a command that calls Qwen3-VL's training entrypoint.

The script must support dry-run mode so users can inspect the exact upstream command before launching expensive training.

Initial public configs should cover representative paper recipes:

- Grounding LoRA.
- Grounding Full Finetune.
- Grounding + Egocentric Understanding LoRA.
- Domain default settings for the seven embodied VQA domains.

## Stage-2 VLA Training Design

Stage-2 configuration files describe the StarVLA experiment, benchmark, action head, initialization checkpoint, and training overrides.

The launch script will:

1. Validate `STARVLA_ROOT`.
2. Validate that the Stage-1 checkpoint path exists unless dry-run mode is enabled.
3. Render the StarVLA command with benchmark-specific settings.
4. Call StarVLA's training entrypoint without modifying upstream code.

Initial public configs should cover:

- Libero-10 with OpenVLA-OFT-style MLP head.
- SimplerBridge with OpenVLA-OFT-style MLP head.
- RoboCasa GR1 Tabletop with OpenVLA-OFT-style MLP head.
- Libero-10 and RoboCasa diffusion-expert recipes where StarVLA supports them.

## Robot-Data Pretraining Design

Robot-pretraining configs describe AgiBot-based action-side pretraining recipes:

- Base VLM + AgiBot, LoRA rank 64.
- Base VLM + AgiBot + VQA, LoRA rank 64.
- Grounding + Ego initialized VLM followed by AgiBot LoRA rank 64.

These configs are recipes and validation targets. They do not include AgiBot data or checkpoints.

## Data Manifest Design

The repository uses YAML manifests to describe embodied VQA data pools. A manifest entry contains:

- `domain`: one of `spatial`, `grounding`, `plan_reasoning`, `camera_prediction`, `egocentric_understanding`, `temporal_understanding`, `action_ntp`.
- `name`: dataset or shard name.
- `path`: local file or directory path relative to `RETHINK_DATA_ROOT`, or an absolute path.
- `format`: source format, such as `qwen_vl_json`, `jsonl`, or `parquet`.
- `samples`: expected sample count.
- `weight`: optional sampling weight.
- `license`: optional dataset license note.

The manifest validator checks domain names, required fields, path resolution, non-negative sample counts, and duplicate dataset names within a domain.

## Analysis Tools

The first analysis tool reads CSV files and produces Markdown tables for paper-style reporting.

Supported initial outputs:

- Single-domain VQA adaptation summary.
- Domain-composition summary.
- Robot-data pretraining summary.

The analysis code is intentionally lightweight and deterministic. It does not require training dependencies.

## Documentation

The README should lead with the paper question and the repository scope:

"This repository provides recipes and lightweight tooling for studying how VLM representation choices affect VLA initialization."

Documentation pages cover:

- Setup and required upstream repositories.
- Data manifest preparation.
- Stage-1 Qwen3-VL adaptation.
- Stage-2 StarVLA training.
- Robot-data pretraining.
- Experiment matrix and expected result table format.
- Citation and license notes.

## Testing Strategy

The repository should have lightweight tests that can run without Qwen3-VL, StarVLA, datasets, or GPUs:

- Import test for the Python package.
- YAML config schema validation.
- Manifest validation.
- Analysis script test using example CSV files.
- Dry-run command rendering tests for launch recipes.

Training itself is not tested in CI because it depends on external repositories, datasets, and GPUs.

## Success Criteria

The initial public repository is acceptable when:

- `python -m pytest` passes locally.
- `python scripts/setup/check_environment.py --dry-run` reports required env vars and missing optional upstream paths clearly.
- `python scripts/analysis/make_tables.py --input examples/results/single_domain_results.example.csv --table single_domain` produces a Markdown table.
- Stage-1 and Stage-2 launch scripts support dry-run mode and print reproducible upstream commands.
- README explains that Qwen3-VL and StarVLA must be installed separately.
- No private local paths, private checkpoints, or unpublished data paths appear in tracked files.

## Implementation Order

1. Create package metadata, README, license, citation, and `.gitignore`.
2. Add Python package skeleton and config/manifest validators.
3. Add example manifests and example result CSV files.
4. Add analysis table generation.
5. Add dry-run launch scripts for Qwen3-VL and StarVLA.
6. Add docs for setup, data, Stage-1, Stage-2, robot pretraining, and experiments.
7. Add tests and run verification.

