# Results

Result CSV files are intentionally simple so they can be produced by different training systems.

Generate a Markdown table:

```bash
python3 scripts/analysis/make_tables.py \
  --input examples/results/single_domain_results.example.csv \
  --table single_domain
```

Supported table names:

- `single_domain`
- `domain_composition`
- `robot_pretraining`

