from pathlib import Path
from validation.process_csv import process_csv
from validation.report_writer import build_report, write_report
import json

HERE = Path(__file__).parent
CSV = HERE / "test.csv"

def test_process_csv_meta():
    meta, df = process_csv(str(CSV))
    assert meta["n_rows"] >= 1
    assert meta["n_cols"] >= 1
    assert "sha256" in meta and len(meta["sha256"]) == 64
    assert isinstance(meta["warnings"], list)

def test_report_json_schema_roundtrip(tmp_path):
    meta, _ = process_csv("tests/test.csv")
    obj = build_report(meta)
    out = tmp_path / "report.json"
    write_report(obj, str(out), "schemas/report_v0.schema.json")
    loaded = json.loads(out.read_text("utf-8"))
    assert loaded["summary"]["n_rows"] == meta["n_rows"]
