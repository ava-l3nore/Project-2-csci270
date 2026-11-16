import streamlit as st
from datetime import timedelta

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def show_header(data):
    course = data["course"]
    st.title(f"{course['code']} · {course['name']}")
    st.caption(course["term"])


def show_summary(data):
    with st.container(border=True):
        st.subheader("Summary")
        st.write(data["summary"])

def show_planner(dated, undated):
    st.header("📅 Planner")
    for event in dated:
        with st.container(border=True):
            st.write(f"**{event['date']}** · {event['course']} · {event['title']}")

    if undated:
        st.subheader("⚠️ Date not clear")
        for event in undated:
            st.write(f"{event['date_text']} · {event['course']} · {event['title']}")


def show_week_calendar(weeks, undated):
    st.header("📅 Week by week")

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

    if undated:
        st.subheader("⚠️ Date not clear")
        for event in undated:
            st.write(f"{event['date_text']} · {event['course']} · {event['title']}")