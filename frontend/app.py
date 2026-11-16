import streamlit as st

import api
import display
import planner


st.set_page_config(page_title="Syllabus planner", layout="wide")
st.title("Syllabus planner")

uploaded_files = st.file_uploader(
    "Upload your syllabi",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

if st.button("Build my planner", type="primary"):
    if not uploaded_files:
        st.error("Upload at least one syllabus first.")
    else:
        with st.spinner("Reading your syllabi..."):
            try:
                st.session_state["summaries"] = api.summarize_files(uploaded_files)
            except Exception as error:
                st.error(f"Something went wrong: {error}")

if "summaries" in st.session_state:
    all_dates = planner.collect_dates(st.session_state["summaries"])
    dated, undated = planner.sort_dates(all_dates)
    weeks = planner.group_by_week(dated)
    display.show_week_calendar(weeks, undated)