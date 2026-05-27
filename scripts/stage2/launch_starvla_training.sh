#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/stage2/launch_starvla_training.sh <recipe.yaml> [--dry-run]" >&2
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
STARVLA_ROOT_VALUE="${STARVLA_ROOT:-\$STARVLA_ROOT}"

KIND="$(PYTHONPATH="$ROOT/src" python3 - "$RECIPE" <<'PY'
import sys
from rethink_vla_init.config import load_recipe
print(load_recipe(sys.argv[1]).kind)
PY
)"

if [[ "$KIND" == "robot_pretraining" ]]; then
  COMMAND="$(PYTHONPATH="$ROOT/src" python3 -m rethink_vla_init.cli render-robot "$RECIPE" --starvla-root "$STARVLA_ROOT_VALUE")"
else
  COMMAND="$(PYTHONPATH="$ROOT/src" python3 -m rethink_vla_init.cli render-stage2 "$RECIPE" --starvla-root "$STARVLA_ROOT_VALUE")"
fi

if [[ "$DRY_RUN" == "true" ]]; then
  echo "[dry-run] $COMMAND"
  exit 0
fi

if [[ -z "${STARVLA_ROOT:-}" ]]; then
  echo "STARVLA_ROOT is required when not using --dry-run." >&2
  exit 1
fi

echo "Launching: $COMMAND"
eval "exec $COMMAND"

