import json, datetime
from jsonschema import validate, Draft202012Validator
from pathlib import Path
from datetime import datetime, timezone

def write_report(obj: dict, out_path: str, schema_path: str):
    # Validate against JSON Schema (fail fast here; UI can catch & display)
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(obj)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return out_path

def build_report(meta: dict) -> dict:
    return {
        "version": "FAIRy-Report-v0",
        "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dataset_id": { "filename": meta["filename"], "sha256": meta["sha256"] },
        "summary": {
            "n_rows": meta["n_rows"],
            "n_cols": meta["n_cols"],
            "fields_validated": meta["fields_validated"],
        },
        "warnings": meta["warnings"],
        "rulepacks": [],
        "provenance": { "license": None, "source_url": None, "notes": None }
    }
