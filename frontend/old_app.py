"""Streamlit front end for the syllabus summarizer.

Run the backend first (from backend/):  uvicorn app.main:app --reload
Then run this (from frontend/):         streamlit run app.py
"""

import json

import requests
import streamlit as st

API_URL = "http://localhost:8000/api/v1/syllabi/summarize"

# Badge color for each event "type" the model can return.
TYPE_COLORS = {
    "exam": "red",
    "quiz": "green",
    "assignment": "blue",
    "presentation": "orange",
    "academic_deadline": "violet",
    "class_schedule": "gray",
    "other": "gray",
}


def call_api(syllabus_text: str, course_name: str | None) -> dict:
    """Send the syllabus to the backend and return the parsed JSON summary."""
    response = requests.post(
        API_URL,
        json={"syllabus_text": syllabus_text, "course_name": course_name or None},
        timeout=120,
    )
    response.raise_for_status()
    # The backend returns the model's JSON as a string in "summary",
    # so it has to be parsed a second time.
    return json.loads(response.json()["summary"])


def show_header(data: dict) -> None:
    title = " · ".join(
        part for part in (data.get("course_code"), data.get("course_name")) if part
    )
    st.title(title or "Your course")


def show_summary_and_instructor(data: dict) -> None:
    left, right = st.columns([2, 1])

    with left, st.container(border=True):
        st.subheader("Summary")
        st.write(data.get("summary") or "No summary returned.")

    instructor = data.get("instructor") or {}
    with right, st.container(border=True):
        st.subheader("Instructor")
        st.write(f":material/person: {instructor.get('name') or 'Not listed'}")
        st.write(f":material/mail: {instructor.get('email') or 'Not listed'}")
        st.write(f":material/schedule: {instructor.get('office_hours') or 'Not listed'}")


def show_dates(data: dict) -> None:
    dates = data.get("important_dates") or []

    with st.container(border=True):
        st.subheader("Important dates")
        if not dates:
            st.caption("No dates found in this syllabus.")
            return

        # Exact dates first, in order. Unclear ones ("Week 9") go to the end.
        dates = sorted(dates, key=lambda d: (d.get("date") is None, d.get("date") or ""))

        for item in dates:
            when_col, what_col, type_col = st.columns([1, 3, 1])

            if item.get("date"):
                when_col.markdown(f"**{item['date']}**")
            else:
                # Never show a guessed date as certain: show the original wording.
                when_col.markdown(f":orange[\"{item.get('date_text') or '?'}\"]")

            what_col.write(item.get("title") or "Untitled")
            if item.get("date_precision") not in (None, "exact"):
                what_col.caption(":material/warning: Date unclear, check with your instructor")
            if item.get("details"):
                what_col.caption(item["details"])

            event_type = item.get("type") or "other"
            color = TYPE_COLORS.get(event_type, "gray")
            type_col.markdown(f":{color}-badge[{event_type}]")


def show_todos_and_policies(data: dict) -> None:
    left, right = st.columns(2)

    with left, st.container(border=True):
        st.subheader("To-do")
        actions = data.get("student_actions") or []
        if not actions:
            st.caption("Nothing to do yet.")
        for i, action in enumerate(actions):
            st.checkbox(action, key=f"todo-{i}")

    with right, st.container(border=True):
        st.subheader("Policies")
        policies = data.get("policies") or []
        with st.expander(f"Show {len(policies)} policies"):
            for policy in policies:
                st.write(f"- {policy}")


def show_uncertainties(data: dict) -> None:
    uncertainties = data.get("uncertainties") or []
    if uncertainties:
        st.warning(
            "**Check with your instructor:**\n\n"
            + "\n".join(f"- {u}" for u in uncertainties),
            icon=":material/warning:",
        )


def main() -> None:
    st.set_page_config(page_title="Syllabus helper", layout="wide")

    with st.sidebar:
        st.header("Add a syllabus")
        course_name = st.text_input("Course name (optional)", placeholder="CSCI 270")
        syllabus_text = st.text_area("Paste the syllabus text", height=300)

        if st.button("Summarize", type="primary"):
            if not syllabus_text.strip():
                st.error("Paste a syllabus first.")
            else:
                with st.spinner("Reading the syllabus…"):
                    try:
                        # Save the result so it survives Streamlit reruns
                        # (every checkbox click reruns the whole script).
                        st.session_state["data"] = call_api(syllabus_text, course_name)
                    except requests.RequestException as error:
                        st.error(f"Couldn't reach the backend. Is it running? ({error})")
                    except (json.JSONDecodeError, KeyError):
                        st.error("The model's reply wasn't valid JSON. Try again.")

    data = st.session_state.get("data")
    if data is None:
        st.title("Syllabus helper")
        st.write("Paste a syllabus in the sidebar and select **Summarize** to see it here.")
        return

    show_header(data)
    show_summary_and_instructor(data)
    show_dates(data)
    show_todos_and_policies(data)
    show_uncertainties(data)


main()
