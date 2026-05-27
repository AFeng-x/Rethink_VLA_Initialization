# Stage-1 VLM Adaptation

Stage-1 adapts a base VLM with capability-oriented embodied VQA supervision before downstream VLA training.

Representative recipes are stored in `configs/stage1_qwen3vl/`.

Dry-run a recipe:

```bash
bash scripts/stage1/launch_qwen3vl_adaptation.sh \
  configs/stage1_qwen3vl/qwen3vl_4b_grounding_lora.yaml \
  --dry-run
```

The launcher validates the recipe and prints the Qwen3-VL training command. Remove `--dry-run` only after confirming paths, data, and GPU resources.

The public recipes cover LoRA, Full Finetune, and Grounding + Egocentric Understanding adaptation patterns.

