## 🧩 Project Directories & Manifest System

### What we’re building
Each FAIRy project needs a place on disk to store uploaded files and a manifest file that tracks metadata about them.

### Why this matters
- Stateful projects: reopening FAIRy tomorrow shows your files + settings.
- Transparent + simple: JSON is human-readable, diffable, and easy to back up.
- Future-proof: the manifest grows into the single source of truth for validation, templates, checksums, etc.

### Code pieces
- `project_dir(project_id)` → ensures folder structure exists.
- `manifest_path(project_id)` → resolves `manifest.json` path.
- `load_manifest(project_id)` → loads JSON or creates a fresh manifest if missing.
- `save_manifest(project_id, manifest)` → writes indented JSON to disk.

### Example (data, manifest, or UI)
```json
{
  "project_id": "demo-project",
  "created_at": 1727736200,
  "files": [
    {
      "name": "metadata.csv",
      "original_name": "upload.csv",
      "bytes": 1204,
      "hash": "abc123...",
      "saved_at": 1727736300,
      "columns": ["sample_id","organism","condition"],
      "template": "GEO RNA-seq minimal"
    }
  ]
}# FAIRy Development Notes\n
