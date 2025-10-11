from pathlib import Path
from validation.process_csv import process_csv
from fairy.core.services.report_writer import write_report
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
    meta, _ = process_csv(str(CSV))
    out_path = write_report(
        out_dir=tmp_path,
        filename=CSV.name,
        sha256=meta["sha256"],
        meta={
            "n_rows": meta["n_rows"],
            "n_cols": meta["n_cols"],
            "fileds_validated": meta.get("fields_validated", []),
            "warnings": meta.get("warnings", [])
        },
        rulepacks=[],
        provenance={"license": None, "source_url": None, "notes": None},
        input_path=str(CSV),
        )
    
    assert out_path.name == "report.json" and out_path.exists()
    loaded = json.loads(out_path.read_text("utf-8"))
    assert loaded["summary"]["n_rows"] == meta["n_rows"]
