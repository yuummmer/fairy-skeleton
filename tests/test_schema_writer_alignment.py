# tests/test_schema_writer_alignment.py
import json, jsonschema
from pathlib import Path
from fairy.core.services.report_writer import write_report

SCHEMA = json.loads(Path("schemas/report_v0.schema.json").read_text())

def test_writer_output_matches_schema(tmp_path):
    p = write_report(
        tmp_path,
        filename="samples_toy.csv",
        sha256="0"*64,
        meta={"n_rows":1, "n_cols":2, "fields_validated":["a","b"], "warnings":[]},
        rulepacks=[{"name":"core","version":"0.1.0"}],
        provenance={"license": None, "source_url": None, "notes": None},
        input_path="samples_toy.csv"
    )
    data = json.loads(p.read_text())
    jsonschema.validate(data, SCHEMA)
