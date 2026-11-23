"""Loads the scraped CofC academic calendar (data/calendar.json) for the model prompt."""

import json
import re
from functools import lru_cache
from pathlib import Path

CALENDAR_PATH = Path(__file__).resolve().parents[3] / "data" / "calendar.json"
TERM_RE = re.compile(r"\b(Fall|Spring|Summer)\s+(20\d\d)\b", re.IGNORECASE)


@lru_cache
def load_calendar() -> list[dict]:
    if not CALENDAR_PATH.exists():
        return []
    with open(CALENDAR_PATH, encoding="utf-8") as f:
        return json.load(f)


def calendar_context(syllabus_text: str) -> str:
    """Return the calendar as prompt text, narrowed to the syllabus's term when it can be detected."""
    events = load_calendar()
    if not events:
        return ""

    found = TERM_RE.search(syllabus_text)
    if found:
        season, year = found.group(1).capitalize(), found.group(2)
        matching = [e for e in events if e["term"].startswith(f"{year} {season}")]
        if matching:
            events = matching

    lines = []
    for e in events:
        when = e["due_at"] + (f" to {e['end_date']}" if e.get("end_date") else "")
        lines.append(f"- {when}: {e['title']} ({e['term']})")
    return "\n".join(lines)
