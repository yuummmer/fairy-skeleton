# validation/process_csv.py
from __future__ import annotations

import io
import hashlib
from typing import Any, Dict, List, Tuple, Union

import pandas as pd
import pandera.pandas as pa
from schemas.sample_table import schema  # our minimal Pandera schema

FileLike = Union[str, bytes, io.BytesIO]

def _sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

def _read_csv(file_like: FileLike) -> Tuple[pd.DataFrame, bytes, str]:
    """Return (df, raw_bytes, filename_guess)."""
    if isinstance(file_like, str):
        with open(file_like, "rb") as f:
            raw = f.read()
        df = pd.read_csv(io.BytesIO(raw))
        return df, raw, file_like.split("/")[-1]
    if isinstance(file_like, (bytes, bytearray)):
        raw = bytes(file_like)
        return pd.read_csv(io.BytesIO(raw)), raw, "<uploaded.csv>"
    if isinstance(file_like, io.BytesIO):
        raw = file_like.getvalue()
        return pd.read_csv(io.BytesIO(raw)), raw, "<uploaded.csv>"
    raise TypeError(f"Unsupported file_like type: {type(file_like)}")

def process_csv(file_like: FileLike) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """
    Validate one CSV in 'warn-mode' and return:
      meta: {
        filename, sha256, n_rows, n_cols, fields_validated, warnings[]
      }
      df: pandas DataFrame
    """
    df, raw, filename = _read_csv(file_like)
    warnings: List[Dict[str, Any]] = []

    try:
        schema.validate(df, lazy=True)  # collect all failures
    except pa.errors.SchemaErrors as err:
        fc = err.failure_cases.fillna("")
        for row in fc.itertuples(index=False):
            warnings.append({
                "column": str(getattr(row, "column", "")),
                "check": str(getattr(row, "check", "")),
                "failure": str(getattr(row, "failure_case", "")),
                "index": str(getattr(row, "index", "")),
            })

    meta: Dict[str, Any] = {
        "filename": filename,
        "sha256": _sha256_bytes(raw),
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "fields_validated": list(schema.columns.keys()),
        "warnings": warnings,
    }
    return meta, df
