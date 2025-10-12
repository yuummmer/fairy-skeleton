from __future__ import annotations
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import pandas as pd
import hashlib, io, json, time
import streamlit as st

from pathlib import Path
from fairy.core.storage import update_project_timestamp
from fairy.utils.projects import project_dir, exports_dir, load_manifest, save_manifest
from fairy.utils.ui import status_chip, format_bytes, shape_badge
from fairy.validation.checks import (
    missing_required, duplicate_in_column, column_name_mismatch
)
from fairy.validation.process_csv import process_csv
from fairy.core.services.report_writer import write_report
from fairy.ui.preview_utils import run_validators, build_tooltip_matrix, styled_preview
from fairy.ui.tabs.export_validate import render_export_validate_tab
from fairy.ui.tabs.data_inventory import render_data_inventory_tab
from fairy.ui.shared.context import ProjectCtx
from fairy.ui.tabs.overview import render_overview_tab
from fairy.ui.tabs.permissions_ethics import render_permissions_tab
from fairy.ui.tabs.deidentification import render_deidentification_tab
from fairy.ui.tabs.repository import render_repository_tab
from fairy.ui.tabs.metadata import render_metadata_tab



def _get_selected_project(projects):
    pid = st.session_state.get("selected_project_id")
    if not pid:
        return None
    for proj in projects:
        if proj["id"] == pid:
            return proj
    return None

def render_project(projects, save_and_refresh) -> None:
    p = _get_selected_project(projects)
    if not p:
        st.warning("No project selected. Go to Home and choose a project, or create a new one.")
        return

    ctx = ProjectCtx(project=p, projects=projects, save_and_refresh=save_and_refresh)

    st.title(f"📁 {ctx.project['title']}")
    st.caption(ctx.project["description"])

    tabs = st.tabs([
        "Overview",
        "Data Inventory",
        "Permissions & Ethics",
        "De-identification",
        "Metadata",
        "Repository",
        "Export & Validate"
    ])

    with tabs[0]:
        render_overview_tab(ctx)
    with tabs[1]:
        render_data_inventory_tab(ctx)
    with tabs[2]:
        render_permissions_tab(ctx)
    with tabs[3]:
        render_deidentification_tab(ctx)
    with tabs[5]:
        render_repository_tab(ctx)
    with tabs[4]:
        render_metadata_tab(ctx)
    with tabs[6]:
        render_export_validate_tab(ctx)

    # ---- Metadata -------------------------------------------------

        
    if st.sidebar.button("← Back to Home"):
        st.session_state.selected_project_id = None
        st.rerun()
