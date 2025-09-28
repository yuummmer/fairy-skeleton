from pathlib import Path
import json
from fairy.core.storage import Storage

def test_storage_roundtrip(tmp_path: Path):
    s = Storage(data_dir=tmp_path / ".fairy_data_test")
    projects = [{"id":"p1","title":"T","description":"D","status":"In Progress","created_at":"x","updated_at":"y",
                 "data_inventory":[], "permissions":{}, "deid":{}, "metadata":{"project":{}, "samples":[]},
                 "repository":{"choice":None,"notes":""}, "exports":[]}]
    s.save_projects(projects)
    loaded = s.load_projects()
    assert loaded == projects
