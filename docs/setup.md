# Setup

This repository is a thin recipe layer over Qwen3-VL and StarVLA.

## 1. Clone Upstream Repositories

```bash
git clone https://github.com/QwenLM/Qwen3-VL.git
git clone --branch starVLA https://github.com/starVLA/starVLA.git
```

Install each upstream project according to its own README.

## 2. Set Environment Variables

```bash
export QWEN3_VL_ROOT=/path/to/Qwen3-VL
export STARVLA_ROOT=/path/to/starVLA
export RETHINK_DATA_ROOT=/path/to/prepared/data
export RETHINK_OUTPUT_ROOT=/path/to/outputs
```

## 3. Check Local Environment

```bash
python3 scripts/setup/check_environment.py --dry-run
```

The dry-run check reports missing paths without launching training.

