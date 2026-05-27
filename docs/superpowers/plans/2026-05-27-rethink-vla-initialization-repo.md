# Rethink VLA Initialization Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a public experiment-recipe repository for reproducing the paper's VLM-to-VLA initialization workflow without vendoring Qwen3-VL or StarVLA.

**Architecture:** The repository is a thin wrapper around upstream projects. Python modules validate recipe configs, validate data manifests, render dry-run launch commands, and generate Markdown result tables from CSV files. Shell scripts and docs expose the workflow for Stage-1 Qwen3-VL adaptation, Stage-2 StarVLA training, and robot-data pretraining.

**Tech Stack:** Python 3.9+ standard library, pytest for tests, POSIX shell launch scripts, JSON-compatible YAML config files, Markdown docs.

---

### Task 1: Repository Metadata and Documentation Shell

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `CITATION.cff`
- Create: `.gitignore`
- Create: `pyproject.toml`
- Create: `docs/setup.md`
- Create: `docs/data.md`
- Create: `docs/stage1_vlm_adaptation.md`
- Create: `docs/stage2_vla_training.md`
- Create: `docs/robot_pretraining.md`
- Create: `docs/experiments.md`
- Create: `docs/results.md`

- [ ] **Step 1: Add public-facing docs and metadata**

Create concise files that state the repo is a thin recipe layer, requires separate Qwen3-VL and StarVLA clones, and does not include private data or checkpoints.

- [ ] **Step 2: Verify metadata files exist**

Run: `find . -maxdepth 2 -type f | sort`
Expected: metadata and docs files are listed.

- [ ] **Step 3: Commit**

Run: `git add README.md LICENSE CITATION.cff .gitignore pyproject.toml docs && git commit -m "docs: add repository documentation shell"`

### Task 2: Tests for Core Python Behavior

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/test_manifests.py`
- Create: `tests/test_config.py`
- Create: `tests/test_analysis.py`
- Create: `tests/test_recipes.py`

- [ ] **Step 1: Write failing tests for manifest validation**

Tests should expect `load_manifest()` to accept valid example manifests and reject invalid domains, negative sample counts, and duplicate names within a domain.

- [ ] **Step 2: Write failing tests for recipe loading and command rendering**

Tests should expect `load_recipe()` to read JSON-compatible `.yaml`, and renderers to include upstream roots and dry-run commands for Qwen3-VL and StarVLA.

- [ ] **Step 3: Write failing tests for CSV table generation**

Tests should expect `render_table_from_csv()` to generate Markdown tables for single-domain and robot-pretraining examples.

- [ ] **Step 4: Run tests to verify RED**

Run: `python3 -m pytest -q`
Expected: FAIL because the package modules do not exist yet.

- [ ] **Step 5: Commit tests**

Run: `git add tests && git commit -m "test: define repository tooling behavior"`

### Task 3: Python Package Implementation

**Files:**
- Create: `src/rethink_vla_init/__init__.py`
- Create: `src/rethink_vla_init/config.py`
- Create: `src/rethink_vla_init/manifests.py`
- Create: `src/rethink_vla_init/recipes.py`
- Create: `src/rethink_vla_init/analysis.py`

- [ ] **Step 1: Implement manifest validation**

Use standard-library dataclasses and JSON parsing. Treat `.yaml` files as JSON-compatible YAML for zero-dependency validation.

- [ ] **Step 2: Implement recipe loading and command rendering**

Support recipe kinds `stage1_qwen3vl`, `stage2_starvla`, and `robot_pretraining`. Render commands without executing them.

- [ ] **Step 3: Implement CSV-to-Markdown table generation**

Use `csv.DictReader`, preserve column order, and format values as Markdown table cells.

- [ ] **Step 4: Run tests to verify GREEN**

Run: `python3 -m pytest -q`
Expected: PASS.

- [ ] **Step 5: Commit implementation**

Run: `git add src tests pyproject.toml && git commit -m "feat: add validation and analysis tooling"`

### Task 4: Example Configs, Manifests, and Results

**Files:**
- Create files under `configs/stage1_qwen3vl/`
- Create files under `configs/stage2_starvla/`
- Create files under `configs/robot_pretraining/`
- Create: `configs/analysis/main_tables.yaml`
- Create: `examples/manifests/embodied_vqa_manifest.example.yaml`
- Create: `examples/results/single_domain_results.example.csv`
- Create: `examples/results/domain_composition_results.example.csv`
- Create: `examples/results/robot_pretraining_results.example.csv`

- [ ] **Step 1: Add JSON-compatible YAML configs**

Configs should cover the representative recipes from the design spec and include paper-aligned defaults.

- [ ] **Step 2: Add example manifest and result CSVs**

Use non-private sample paths under domain folders and example numeric values from the paper tables.

- [ ] **Step 3: Run tests**

Run: `python3 -m pytest -q`
Expected: PASS.

- [ ] **Step 4: Commit examples**

Run: `git add configs examples && git commit -m "feat: add experiment recipes and examples"`

### Task 5: CLI Scripts

**Files:**
- Create: `scripts/setup/check_environment.py`
- Create: `scripts/analysis/make_tables.py`
- Create: `scripts/stage1/launch_qwen3vl_adaptation.sh`
- Create: `scripts/stage2/launch_starvla_training.sh`

- [ ] **Step 1: Add environment checker**

The checker reports `QWEN3_VL_ROOT`, `STARVLA_ROOT`, `RETHINK_DATA_ROOT`, and `RETHINK_OUTPUT_ROOT`, and exits successfully in `--dry-run`.

- [ ] **Step 2: Add analysis CLI**

The script calls `render_table_from_csv()` and prints Markdown.

- [ ] **Step 3: Add launch shell scripts**

The scripts pass recipe paths to Python renderers and support dry-run mode.

- [ ] **Step 4: Verify scripts**

Run:
`python3 scripts/setup/check_environment.py --dry-run`
`python3 scripts/analysis/make_tables.py --input examples/results/single_domain_results.example.csv --table single_domain`
Expected: both commands exit 0.

- [ ] **Step 5: Commit scripts**

Run: `git add scripts && git commit -m "feat: add dry-run command scripts"`

### Task 6: Final Verification and Cleanup

**Files:**
- Modify docs if command names or paths changed during implementation.

- [ ] **Step 1: Run full test suite**

Run: `python3 -m pytest -q`
Expected: all tests pass.

- [ ] **Step 2: Run smoke checks**

Run:
`python3 scripts/setup/check_environment.py --dry-run`
`python3 scripts/analysis/make_tables.py --input examples/results/single_domain_results.example.csv --table single_domain`
`bash scripts/stage1/launch_qwen3vl_adaptation.sh configs/stage1_qwen3vl/qwen3vl_4b_grounding_lora.yaml --dry-run`
`bash scripts/stage2/launch_starvla_training.sh configs/stage2_starvla/libero10_oft.yaml --dry-run`

Expected: all commands exit 0 and print clear dry-run output.

- [ ] **Step 3: Check tracked files for private paths**

Run: `rg -n '/Users/|linweifeng|Downloads/local_code|A800dev' .`
Expected: no output except in git metadata if searched accidentally; do not search `.git`.

- [ ] **Step 4: Commit final cleanup**

Run: `git status --short`; if docs changed, commit them with `git commit -m "docs: align usage instructions"`.
