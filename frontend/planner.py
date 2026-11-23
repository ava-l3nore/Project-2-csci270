import re
from datetime import date, datetime, timedelta

def fill_year(event, term):
    text = event.get("date_text") or ""
    year = re.search(r"20\d\d", term or "")
    md = re.match(r"\s*(\d{1,2})[/-](\d{1,2})", text)
    named = re.match(r"\s*([A-Za-z]{3,})\.?\s+(\d{1,2})", text)
    month_day = None
    if md:
        month_day = (int(md.group(1)), int(md.group(2)))
    elif named:
        try:
            month_day = (datetime.strptime(named.group(1)[:3], "%b").month, int(named.group(2)))
        except ValueError:
            pass
    if not year or not month_day:
        return event
    if event.get("date"):
        d = date.fromisoformat(event["date"])
        if (d.year, d.month, d.day) == (int(year.group()), *month_day):
            event["date_precision"] = "exact"
        return event
    try:
        event["date"] = date(int(year.group()), *month_day).isoformat()
        event["date_precision"] = "exact"
    except ValueError:
        pass
    return event


def is_college_date(item):
    # the backend tells the model to mark scraped calendar dates with this evidence
    return "academic calendar" in (item.get("evidence") or "").lower()


def collect_dates(summaries):
    all_dates = []
    seen_college = set()
    for summary in summaries:
        course_code = summary["course"]["code"] or summary["course"]["name"] or "Unknown course"
        term = summary["course"]["term"]
        for item in summary["important_dates"]:
            event = fill_year(dict(item), term)
            if is_college_date(event):
                # college-wide dates are shown once, not once per course
                key = (event.get("date"), event["title"].strip().lower())
                if key in seen_college:
                    continue
                seen_college.add(key)
                event["course"] = "CofC"
            else:
                event["course"] = course_code
            all_dates.append(event)
    return all_dates

def get_date(event):
    return event["date"]


def sort_dates(all_dates):
    dated = []
    undated = []
    for event in all_dates:
        if event["date"] and event.get("date_precision") == "exact":
            dated.append(event)
        else:
            undated.append(event)
    dated.sort(key=get_date)
    return dated, undated

def week_start(date_string):
    day = date.fromisoformat(date_string)
    return day - timedelta(days=day.weekday())


def group_by_week(dated):
    weeks = {}
    for event in dated:
        monday = week_start(event["date"])
        if monday not in weeks:
            weeks[monday] = []
        weeks[monday].append(event)
    return weeks

def to_calendar_events(dated):
    events = []
    for index, event in enumerate(dated):
        events.append({
            "id": str(index),
            "title": f"{event['course']} · {event['title']}",
            "start": event["date"],
            "allDay": True,
            "extendedProps": event.copy(),
        })
    return events