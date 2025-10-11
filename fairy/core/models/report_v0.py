from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class DatasetId:
    filename: str
    sha256: str

@dataclass
class Rulepack:
    name: str
    version: str

@dataclass
class Provenance:
    license: Optional[str] = None
    source_url: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class Summary:
    n_rows: int
    n_cols: int
    fields_validated: List[str]

@dataclass
class WarningItem:
    column: str
    check: str
    failure: str
    index: int

# Optional v0 fields you may want (schema-friendly, safe defaults)
@dataclass
class InputFile:
    path: str
    bytes: int

@dataclass
class Inputs:
    project_dir: str
    files: List[InputFile] = field(default_factory=list)

@dataclass
class ReportV0:
    version: str
    run_at: str
    dataset_id: DatasetId
    summary: Summary
    warnings: List[WarningItem] = field(default_factory=list)
    rulepacks: List[Rulepack] = field(default_factory=list)
    provenance: Provenance = field(default_factory=Provenance)
    # present but optional in v0 (writer can ignore or populate later)
    inputs: Inputs = field(default_factory=lambda: Inputs(project_dir=".", files=[]))
    checks: List[Dict] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=lambda: {"preflight": 0.0})
