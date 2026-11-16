from datetime import date, timedelta

def collect_dates(summaries):
    all_dates = []
    for summary in summaries:
        course_code = summary["course"]["code"] or summary["course"]["name"] or "Unknown course"
        for item in summary["important_dates"]:
            event = dict(item)
            event["course"] = course_code
            all_dates.append(event)
    return all_dates

def get_date(event):
    return event["date"]


def sort_dates(all_dates):
    dated = []
    undated = []
    for event in all_dates:
        if event["date"]:
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