import argparse, json
from pathlib import Path
from hashlib import sha256
from ..core.services.report_writer import write_report, _now_utc_iso

def sha256_bytes(b: bytes) -> str:
    h = sha256(); h.update(b); return h.hexdigest()

def main(argv=None):
    p = argparse.ArgumentParser(prog="fairy-demo")
    p.add_argument("--input", required=True, help="CSV file to summarize")
    p.add_argument("--out", default="project_dir/reports", help="Output directory for report_v0.json")
    p.add_argument("--dry-run", action="store_true", help="Print JSON to stdout instead of writing")
    args = p.parse_args(argv)

    data_path = Path(args.input)
    data_bytes = data_path.read_bytes()

    # Placeholder meta; later wire to your validator
    meta = {"n_rows": 0, "n_cols": 0, "fields_validated": [], "warnings": []}

    payload = {
        "version": "0.1.0",
        "run_at": _now_utc_iso(),
        "dataset_id": {"filename": data_path.name, "sha256": sha256_bytes(data_bytes)},
        "summary": {
            "n_rows": meta["n_rows"],
            "n_cols": meta["n_cols"],
            "fields_validated": sorted(meta["fields_validated"]),
        },
        "warnings": meta["warnings"],
        "rulepacks": [],
        "provenance": {"license": None, "source_url": None, "notes": None},
        "scores": {"preflight": 0.0}
    }

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)); return 0
    else:
        path = write_report(
            out_dir=args.out,
            filename=data_path.name,
            sha256=payload["dataset_id"]["sha256"],
            meta=meta,
            rulepacks=[],
            provenance={"license": None, "source_url": None, "notes": None},
        )
        print(f"Wrote {path}"); return 0

if __name__ == "__main__":
    raise SystemExit(main())
