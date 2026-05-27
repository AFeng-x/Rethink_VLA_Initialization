# Robot-Data Pretraining

Robot-data pretraining injects action-side supervision before downstream VLA training.

The public recipes focus on AgiBot-style pretraining patterns:

- Base VLM + AgiBot with LoRA rank 64.
- Base VLM + AgiBot + VQA with LoRA rank 64.
- Grounding + Egocentric Understanding initialized VLM followed by AgiBot LoRA rank 64.

Recipes live in `configs/robot_pretraining/`. They document the experiment settings but do not include robot data or checkpoints.

