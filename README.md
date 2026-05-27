# Rethink VLA Initialization

Recipe and lightweight tooling repository for the paper **"Rethinking VLM Representation for VLA Initialization."**

This repository studies a practical question: what kind of pretrained VLM representation is useful for initializing Vision-Language-Action (VLA) policies? It provides reproducible experiment recipes for:

- Stage-1 VLM adaptation with Qwen3-VL.
- Stage-2 VLA training with StarVLA.
- Robot-data pretraining recipes.
- Embodied VQA data manifests.
- Lightweight result-table generation from CSV logs.

This is a thin recipe layer. It does not vendor Qwen3-VL or StarVLA code, and it does not include private datasets or checkpoints.

## Upstream Projects

Clone and install these separately:

- Qwen3-VL: <https://github.com/QwenLM/Qwen3-VL>
- StarVLA: <https://github.com/starVLA/starVLA/tree/starVLA>

Set these environment variables before launching training:

```bash
export QWEN3_VL_ROOT=/path/to/Qwen3-VL
export STARVLA_ROOT=/path/to/starVLA
export RETHINK_DATA_ROOT=/path/to/prepared/data
export RETHINK_OUTPUT_ROOT=/path/to/outputs
```

## Quick Start

```bash
python3 scripts/setup/check_environment.py --dry-run
python3 scripts/analysis/make_tables.py \
  --input examples/results/single_domain_results.example.csv \
  --table single_domain

bash scripts/stage1/launch_qwen3vl_adaptation.sh \
  configs/stage1_qwen3vl/qwen3vl_4b_grounding_lora.yaml \
  --dry-run

bash scripts/stage2/launch_starvla_training.sh \
  configs/stage2_starvla/libero10_oft.yaml \
  --dry-run
```

## Repository Layout

```text
configs/              Experiment recipes for Stage-1, Stage-2, robot pretraining, and analysis
docs/                 Setup, data, training, and experiment documentation
examples/             Example manifests and result CSVs
scripts/              Dry-run launchers and analysis CLI
src/rethink_vla_init/ Lightweight validators, renderers, and analysis helpers
tests/                Zero-GPU tests for repository tooling
```

## Config Format

Files under `configs/` use `.yaml` extensions, but intentionally stay in a JSON-compatible YAML subset. This keeps local validation dependency-free while remaining readable as YAML.

## Citation

If you use this repository, please cite the paper using the metadata in `CITATION.cff`.

