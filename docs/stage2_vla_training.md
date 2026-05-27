# Stage-2 VLA Training

Stage-2 initializes a VLA policy from a Stage-1 checkpoint and trains on downstream robot trajectories with StarVLA.

Representative recipes are stored in `configs/stage2_starvla/`.

Dry-run a recipe:

```bash
bash scripts/stage2/launch_starvla_training.sh \
  configs/stage2_starvla/libero10_oft.yaml \
  --dry-run
```

The launcher renders a StarVLA command and checks the upstream root. It does not modify StarVLA source files.

