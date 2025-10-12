from __future__ import annotations
import streamlit as st
from fairy.ui.shared.context import ProjectCtx
from fairy.core.storage import update_project_timestamp

def render_permissions_tab(ctx: ProjectCtx) -> None:
    p = ctx.project
    st.subheader("Permissions & Ethics")

    contains_human = st.radio(
        "Does your dataset include human subjects data?",
        options=["Unknown", "No", "Yes"],
        index=0,
        key=f"perm_contains_human_{p['id']}",
    )
    irb = st.radio(
        "IRB/ethics approval required?",
        options=["Unknown", "No", "Yes"],
        index=0,
        key=f"perm_irb_{p['id']}",
    )
    notes = st.text_area("Notes", key=f"perm_notes_{p['id']}")

    if st.button("Save permissions"):
        p["permissions"] = {
            "contains_human_data": None if contains_human == "Unknown" else (contains_human == "Yes"),
            "irb_required": None if irb == "Unknown" else (irb == "Yes"),
            "notes": notes.strip(),
        }
        update_project_timestamp(p)
        ctx.save_and_refresh(ctx.projects)
