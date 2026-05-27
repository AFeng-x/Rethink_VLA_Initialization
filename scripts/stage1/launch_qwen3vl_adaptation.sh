#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/stage1/launch_qwen3vl_adaptation.sh <recipe.yaml> [--dry-run]" >&2
  exit 2
fi

RECIPE="$1"
shift
DRY_RUN=false
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
QWEN_ROOT="${QWEN3_VL_ROOT:-\$QWEN3_VL_ROOT}"
COMMAND="$(PYTHONPATH="$ROOT/src" python3 -m rethink_vla_init.cli render-stage1 "$RECIPE" --qwen-root "$QWEN_ROOT")"

if [[ "$DRY_RUN" == "true" ]]; then
  echo "[dry-run] $COMMAND"
  exit 0
fi

if [[ -z "${QWEN3_VL_ROOT:-}" ]]; then
  echo "QWEN3_VL_ROOT is required when not using --dry-run." >&2
  exit 1
fi

echo "Launching: $COMMAND"
eval "exec $COMMAND"

