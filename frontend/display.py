import streamlit as st
from streamlit_calendar import calendar
from datetime import timedelta

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

#color mapping for calendar events
TYPE_COLORS = {
    "assignment": "#2563eb",
    "exam": "#dc2626",
    "quiz": "#a16207",
    "presentation": "#7c3aed",
    "deadline": "#be185d",
    "to_read": "#047857",
    "final_exam": "#991b1b",
    "class_schedule": "#0369a1",
    "other": "#4b5563",
    }

def show_header(data):
    course = data["course"]
    st.title(f"{course['code']} · {course['name']}")
    st.caption(course["term"])


def show_summary(data):
    with st.container(border=True):
        course = data["course"]
        st.subheader(course["code"] or course["name"] or "Summary")
        st.write(data["summary"])

def show_undated(undated):
    if undated:
        st.subheader("Date not clear")
        st.caption("These entries need a confirmed date before being scheduled.")
        for event in undated:
            st.write(f"**{event['date_text']}** · {event['course']} · {event['title']}")

def show_planner(dated, undated):
    st.header("📅 Planner")
    for event in dated:
        with st.container(border=True):
            st.write(f"**{event['date']}** · {event['course']} · {event['title']}")

    show_undated(undated)


def show_week_calendar(weeks, undated):
    st.header("📅 Week by week")

    #for results without an exact date to display
    if not weeks:
        st.info("No events with exact dates to display.")

    for monday, events in weeks.items():
        st.subheader(f"Week of {monday.strftime('%b %d')}")
        columns = st.columns(7)

        for i in range(7):
            day = monday + timedelta(days=i)
            with columns[i]:
                st.markdown(f"**{DAY_NAMES[i]} {day.day}**")
                for event in events:
                    if event["date"] == day.isoformat():
                        st.info(f"**{event['course']}**\n\n{event['title']}")

    show_undated(undated)

def show_month_calendar(events, undated, key):
    st.header("Month calendar")

    if not events:
        st.info("No events with exact dates to display.")
        show_undated(undated)
        return
    
    for event in events:
        event_type = event["extendedProps"].get("type","other")
        event["color"] = TYPE_COLORS.get(event_type, TYPE_COLORS["other"])
        event["textColor"] = "#ffffff"

        legend = " &nbsp; ".join(
        f'<span style="color:{color}">● {kind.replace("_", " ").title()}</span>'
        for kind, color in TYPE_COLORS.items()
    )
    st.markdown(legend, unsafe_allow_html=True)
    st.caption("Click an event for details. Dates have no specified time.")

    result = calendar(
        events=events,
        options={
            "initialView": "dayGridMonth",
            "initialDate": events[0]["start"],
            "firstDay": 1,
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "",
            },
            "editable": False,
            "selectable": False,
            "height": "auto",
        },
        callbacks=["eventClick"],
        key=key,
    )

    # no selected event exists on the calendar's first render.
    if result and result.get("callback") == "eventClick":
        selected = result["eventClick"]["event"]
        details = selected.get("extendedProps", {})
        with st.container(border=True):
            st.subheader(selected["title"])
            st.caption(f"{details.get('date', '')} · Time unspecified")
            if details.get("details"):
                st.write(details["details"])
            if details.get("evidence"):
                st.markdown("**Syllabus excerpt**")
                st.write(details["evidence"])

    show_undated(undated)