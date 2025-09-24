
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

import pandas as pd
import streamlit as st

APP_TITLE = "FAIRy — Data Preparation Wizard"
st.set_page_config(page_title=APP_TITLE, page_icon="✨", layout="wide")

# --- Simple local persistence for prototype (per user/machine) ---
DATA_DIR = Path(".fairy_data")
DATA_DIR.mkdir(exist_ok=True)
PROJECTS_JSON = DATA_DIR / "projects.json"

def load_projects() -> List[Dict[str, Any]]:
    if PROJECTS_JSON.exists():
        return json.loads(PROJECTS_JSON.read_text(encoding="utf-8"))
    return []

def save_projects(projects: List[Dict[str, Any]]):
    PROJECTS_JSON.write_text(json.dumps(projects, indent=2), encoding="utf-8")

def new_project(title: str, description: str) -> Dict[str, Any]:
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "id": f"prj_{int(datetime.utcnow().timestamp())}",
        "title": title,
        "description": description,
        "status": "In Progress",
        "created_at": now,
        "updated_at": now,
        "data_inventory": [],
        "permissions": {"contains_human_data": None, "irb_required": None, "notes": ""},
        "deid": {"strategy": "", "notes": ""},
        "metadata": {"project": {}, "samples": []},
        "repository": {"choice": None, "notes": ""},
        "exports": []
    }

def update_project_timestamp(p):
    p["updated_at"] = datetime.utcnow().isoformat() + "Z"

st.sidebar.title("Navigation")
view = st.sidebar.radio("Go to", ["Home", "Project"], index=0)

if "selected_project_id" not in st.session_state:
    st.session_state.selected_project_id = None

projects = load_projects()

def get_selected_project(projects):
    pid = st.session_state.selected_project_id
    if not pid:
        return None
    for p in projects:
        if p["id"] == pid:
            return p
    return None

def save_and_refresh(projects):
    save_projects(projects)
    st.experimental_rerun()

# --- HOME VIEW ---
if view == "Home":
    st.title("✨ FAIRy")
    st.caption("Prototype dashboard — manage datasets and prepare them for FAIR-compliant submission.")

    with st.expander("➕ Create a new project", expanded=True):
        col1, col2 = st.columns([2,1])
        with col1:
            title = st.text_input("Project title*", placeholder="e.g., RNA-seq study on XYZ")
            desc = st.text_area("Short description*", placeholder="One or two lines about the dataset and study.")
        with col2:
            if st.button("Create project", type="primary", disabled=not (title.strip() and desc.strip())):
                p = new_project(title.strip(), desc.strip())
                projects.insert(0, p)
                save_and_refresh(projects)

    if not projects:
        st.info("No projects yet. Create your first one above!")
    else:
        st.subheader("Your projects")
        df = pd.DataFrame([{
            "Title": p["title"],
            "Status": p["status"],
            "Updated": p["updated_at"],
            "ID": p["id"]
        } for p in projects])
        st.dataframe(df, use_container_width=True, hide_index=True)

        select_id = st.selectbox("Open a project", options=["— select —"] + [p["id"] for p in projects])
        if select_id != "— select —":
            st.session_state.selected_project_id = select_id
            st.experimental_rerun()

# --- PROJECT VIEW ---
else:
    p = get_selected_project(projects)
    if not p:
        st.warning("No project selected. Go to Home and choose a project, or create a new one.")
        st.stop()

    st.title(f"📁 {p['title']}")
    st.caption(p["description"])

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
        st.subheader("Overview")
        col1, col2 = st.columns(2)
        with col1:
            new_title = st.text_input("Title", value=p["title"])
            new_desc = st.text_area("Description", value=p["description"])
            if st.button("Save overview"):
                p["title"], p["description"] = new_title.strip(), new_desc.strip()
                update_project_timestamp(p)
                save_and_refresh(projects)
        with col2:
            st.markdown(f"**Status:** {p['status']}")
            st.markdown(f"**Created:** {p['created_at']}")
            st.markdown(f"**Updated:** {p['updated_at']}")

    with tabs[1]:
        st.subheader("Data Inventory")
        st.caption("Link to where your raw data lives (S3/GS/Box/Drive or local path). FAIRy doesn't upload your data; it records locations.")
        name = st.text_input("Item name", placeholder="e.g., FASTQ files (batch A)")
        path = st.text_input("Path or URL", placeholder="e.g., s3://bucket/run1/*.fastq.gz")
        notes = st.text_input("Notes (optional)")
        add = st.button("Add to inventory")
        if add and name.strip() and path.strip():
            p["data_inventory"].append({"name": name.strip(), "path": path.strip(), "notes": notes.strip()})
            update_project_timestamp(p)
            save_and_refresh(projects)
        if p["data_inventory"]:
            st.table(pd.DataFrame(p["data_inventory"]))

    with tabs[2]:
        st.subheader("Permissions & Ethics (placeholder)")
        contains_human = st.radio("Does your dataset include human subjects data?", options=["Unknown","No","Yes"], index=0)
        irb = st.radio("IRB/ethics approval required?", options=["Unknown","No","Yes"], index=0)
        perm_notes = st.text_area("Notes")
        if st.button("Save permissions"):
            p["permissions"] = {
                "contains_human_data": None if contains_human=="Unknown" else (contains_human=="Yes"),
                "irb_required": None if irb=="Unknown" else (irb=="Yes"),
                "notes": perm_notes.strip()
            }
            update_project_timestamp(p)
            save_and_refresh(projects)

    with tabs[3]:
        st.subheader("De-identification (placeholder)")
        strategy = st.text_area("Strategy / approach", value=p["deid"].get("strategy",""))
        deid_notes = st.text_area("Notes", value=p["deid"].get("notes",""))
        if st.button("Save de-identification"):
            p["deid"] = {"strategy": strategy.strip(), "notes": deid_notes.strip()}
            update_project_timestamp(p)
            save_and_refresh(projects)

    with tabs[4]:
        st.subheader("Metadata (prototype)")
        uploaded = st.file_uploader("Upload samples CSV", type=["csv"])
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                p["metadata"]["samples"] = df.to_dict(orient="records")
                update_project_timestamp(p)
                save_and_refresh(projects)
            except Exception as e:
                st.error(f"Failed to read CSV: {e}")
        if p["metadata"]["samples"]:
            st.dataframe(pd.DataFrame(p["metadata"]["samples"]), use_container_width=True)

    with tabs[5]:
        st.subheader("Repository (placeholder)")
        repo = st.selectbox("Choose a repository", ["— select —","GEO","SRA","ENA","Zenodo","dbGaP"], index=0)
        repo_notes = st.text_area("Notes")
        if st.button("Save repository choice"):
            p["repository"] = {"choice": None if repo=="— select —" else repo, "notes": repo_notes.strip()}
            update_project_timestamp(p)
            save_and_refresh(projects)

    with tabs[6]:
        st.subheader("Export & Validate (prototype)")
        if st.button("Generate placeholder export"):
            export_record = {
                "id": f"exp_{int(datetime.utcnow().timestamp())}",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "summary": "Placeholder export generated (implement real exporters next)."
            }
            p["exports"].append(export_record)
            update_project_timestamp(p)
            save_and_refresh(projects)
        if p["exports"]:
            st.write(pd.DataFrame(p["exports"])[["id","created_at","summary"]])

    if st.sidebar.button("← Back to Home"):
        st.session_state.selected_project_id = None
        st.experimental_rerun()
