import json, re
from pathlib import Path
from jsonschema import validate
from fairy.core.services.validator import validate_csv
from fairy.core.services.report_writer import write_report

def test_roundtrip(tmp_path: Path):
    csv = tmp_path/"toy.csv"
    csv.write_text("sample_id,read_length\nA1,100\n,0\n", encoding="utf-8")
    meta = validate_csv(str(csv), kind="rna")
    # build meta dict for writer
    md = {
        "n_rows": meta.n_rows,
        "n_cols": meta.n_cols,
        "fields_validated": meta.fields_validated,
        "warnings": [w.__dict__ for w in meta.warnings],
    }
    out = write_report(tmp_path, filename=csv.name, sha256="deadbeef", meta=md, input_path=str(csv))
    data = json.loads(out.read_text("utf-8"))
    schema = json.loads(Path("schema/report_v0.json").read_text("utf-8"))
    validate(instance=data, schema=schema)
    assert data["dataset_id"]["filename"] == "toy.csv"
    assert re.match(r".*Z$", data["run_at"])
    assert "inputs" in data and data["inputs"]["files"][0]["path"].endswith("toy.csv")
