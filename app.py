from pathlib import Path
from typing import Dict, Any, List
import streamlit as st
import pandas as pd  # needed by UI for dataframes

from fairy.core.storage import Storage, update_project_timestamp
from fairy.ui.home_view import render_home
from fairy.ui.project_view import render_project
from fairy.utils.projects import project_dir, load_manifests, save_manifest

APP_TITLE = "FAIRy — Data Preparation Helper"
st.set_page_config(page_title=APP_TITLE, page_icon="✨", layout="wide")

store = Storage()

def save_and_refresh(projects: List[Dict[str, Any]]) -> None:
    store.save_projects(projects)
    st.rerun()

if "selected_project_id" not in st.session_state:
    st.session_state.selected_project_id = None

st.sidebar.title("Navigation")

if st.session_state.get("__nav_go_home__"):
    st.session_state["main_nav"] = "Home"
    del st.session_state["__nav_go_home__"]

view = st.sidebar.radio(
    "Go to",
    ["Home", "Project"],
    index=0,
    key="main_nav"
)

projects = store.load_projects()

if view == "Home":
    render_home(projects, save_and_refresh)
else:
    render_project(projects, save_and_refresh)

st.sidebar.markdown("—")
st.sidebar.caption("If you use FAIRy, please cite v0.1 (prototype). See **README → Attribution**.")

