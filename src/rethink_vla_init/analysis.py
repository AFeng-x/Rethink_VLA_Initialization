from __future__ import annotations

import csv
from pathlib import Path


TABLE_TITLES = {
    "single_domain": "Single-Domain VQA Adaptation",
    "domain_composition": "Domain Composition",
    "robot_pretraining": "Robot-Data Pretraining",
}


def _markdown_row(values: list[str]) -> str:
    return "| " + " | ".join(values) + " |"


def render_table_from_csv(path: str | Path, *, table_name: str) -> str:
    csv_path = Path(path)
    title = TABLE_TITLES.get(table_name, table_name.replace("_", " ").title())

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{csv_path} does not contain a CSV header")
        rows = list(reader)

    columns = list(reader.fieldnames)
    output = [
        f"### {title}",
        "",
        _markdown_row(columns),
        _markdown_row(["---"] * len(columns)),
    ]
    for row in rows:
        output.append(_markdown_row([row.get(column, "") for column in columns]))

    return "\n".join(output) + "\n"

