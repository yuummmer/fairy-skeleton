import json
from pathlib import Path
from fairy.core.services.report_writer import write_report
from fairy.validation.process_csv import process_csv

REPO = Path(__file__).resolve().parents[1]
BAD = REPO / "tests" / "fairy" / "test_bad.csv"
EXP = REPO / "tests" / "golden" / "expected" / "report_bad.json"

def _normalize(d: dict) -> dict:
    d = dict(d)
    d.pop("run_at", None)
    return d

def test_bad_csv_matches_expected(tmp_path):
    # Produce a report using the real writer flow
    # (meta like row/col counts + warnings are produced upstream; for the golden we just write a minimal consistent structure)
    meta, _ = process_csv(str(BAD))

    out = write_report(
        tmp_path,
        filename=BAD.name,
        sha256=meta["sha256"],
        meta={"n_rows": meta["n_rows"],
              "n_cols": meta["n_cols"],
              "fields_validated": meta.get("fields_validated", []),
              "warnings":meta.get("warnings", []),
              },
        rulepacks=[],
        provenance={"license": None, "source_url": None, "notes": None},
        input_path=str(BAD),
    )

    actual = json.loads(Path(out).read_text(encoding="utf-8"))
    expected = json.loads(EXP.read_text(encoding="utf-8"))
    assert _normalize(actual) == _normalize(expected)
