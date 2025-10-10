from __future__ import annotations
import json, datetime
from pathlib import Path
from typing import List, Optional
from ..models.report_v0 import ReportV0, DatasetId, Summary, WarningItem, Rulepack, Provenance

ISO_UTC = "%Y-%m-%dT%H:%M:%SZ"

def _now_utc_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).strftime(ISO_UTC)

def write_report(
    out_dir,
    *,
    filename,
    sha256,
    meta,                              # expects: n_rows, n_cols, fields_validated, warnings[]
    rulepacks: Optional[List[dict]] = None,
    provenance: Optional[dict] = None,
):
    """Create project_dir/reports/report_v0.json (pretty, deterministic key order)."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    report = ReportV0(
        version="0.1.0",
        run_at=_now_utc_iso(),
        dataset_id=DatasetId(filename=filename, sha256=sha256),
        summary=Summary(
            n_rows=int(meta.get("n_rows", 0)),
            n_cols=int(meta.get("n_cols", 0)),
            fields_validated=sorted(list(meta.get("fields_validated", []))),
        ),
        warnings=[WarningItem(**w) for w in meta.get("warnings", [])],
        rulepacks=[Rulepack(**rp) for rp in (rulepacks or [])],
        provenance=Provenance(**(provenance or {})),
    )

    path = out_path / "report_v0.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(report, f, default=lambda o: o.__dict__, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return path
