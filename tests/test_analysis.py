from rethink_vla_init.analysis import render_table_from_csv


def test_render_table_from_csv_outputs_markdown(tmp_path):
    csv_path = tmp_path / "single_domain.csv"
    csv_path.write_text(
        "Domain,MLP Libero-10,MLP RoboCasa,Diffusion Libero-10\n"
        "Baseline,92.4,49.5,91.8\n"
        "Grounding,95.6,50.4,94.2\n",
        encoding="utf-8",
    )

    table = render_table_from_csv(csv_path, table_name="single_domain")

    assert "| Domain | MLP Libero-10 | MLP RoboCasa | Diffusion Libero-10 |" in table
    assert "| Grounding | 95.6 | 50.4 | 94.2 |" in table
    assert table.startswith("### Single-Domain VQA Adaptation")

