# Data Manifests

Embodied VQA data is described with manifest files. Each entry declares a domain, dataset name, path, format, sample count, optional sampling weight, and optional license note.

Supported domains:

- `spatial`
- `grounding`
- `plan_reasoning`
- `camera_prediction`
- `egocentric_understanding`
- `temporal_understanding`
- `action_ntp`

Example:

```json
{
  "entries": [
    {
      "domain": "grounding",
      "name": "robopoint_sample",
      "path": "grounding/robopoint_sample.jsonl",
      "format": "qwen_vl_json",
      "samples": 1000,
      "weight": 1.0,
      "license": "dataset-specific"
    }
  ]
}
```

The checked-in examples use JSON-compatible YAML so validation works with Python's standard library.

