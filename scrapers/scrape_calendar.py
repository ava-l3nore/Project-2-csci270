from bs4 import BeautifulSoup
from datetime import date
import json
import os
import re
import requests

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
DATE_RE = re.compile(r"(" + "|".join(MONTHS) + r")\s+(\d{1,2})")
YEAR_RE = re.compile(r"\b(20\d\d)\b")


def parse_calendar():
    soup = BeautifulSoup(fetch_calendar(), "html.parser")
    return walker(soup)


def fetch_calendar():
    CACHE = "cache/calendar.html"
    URL = "https://charleston.edu/registrar/calendar/index.php"

    os.makedirs("cache", exist_ok=True)

    if os.path.exists(CACHE) and os.path.getsize(CACHE) > 0:
        html = open(CACHE, encoding="utf-8").read()
    else:
        resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        resp.raise_for_status()
        html = resp.text

        if "accordions__item" not in html:
            raise RuntimeError(f"bad fetch: {len(html)} chars")

        open(CACHE, "w", encoding="utf-8").write(html)

    return html


def walker(soup):
    # first accordion section on the page is "Academic Calendars"
    section = soup.select_one("section.accordions")
    results = []

    for item in section.select("li.accordions__item"):
        term = item.select_one("span.accordions__label").get_text(" ", strip=True)
        if "archived" in term.lower():
            continue

        term_year = int(YEAR_RE.search(term).group(1))
        content = item.select_one("div.user-markup")
        heading_year = term_year

        # walk month headings and date labels in page order
        for tag in content.find_all(["h3", "strong"]):
            text = tag.get_text(" ", strip=True).replace("\xa0", " ")

            if tag.name == "h3":
                found = YEAR_RE.search(text)
                heading_year = int(found.group(1)) if found else term_year
                continue

            dates = DATE_RE.findall(text)
            if not dates:
                continue  # a <strong> that isn't a date, e.g. "NOTE:"

            start = to_date(dates[0], heading_year, term)
            end = to_date(dates[-1], heading_year, term)

            for title in event_titles(tag, text):
                results.append({
                    "title": title,
                    "due_at": start.isoformat(),
                    "end_date": end.isoformat() if end != start else None,
                    "term": term,
                })

    return results


def to_date(match, year, term):
    month = MONTHS.index(match[0]) + 1
    # fall terms list January/February of the next year
    if "Fall" in term and month <= 2 and year == int(YEAR_RE.search(term).group(1)):
        year += 1
    return date(year, month, int(match[1]))


def event_titles(strong, strong_text):
    li = strong.find_parent("li")
    if li is None:
        return []

    # usual layout: date <li> with a nested <ul> of events
    nested = li.find("ul")
    if nested:
        titles = [clean(e.get_text(" ", strip=True)) for e in nested.find_all("li", recursive=False)]
        return [t for t in titles if t]

    # event text sits right after the date, inside the same <li>
    rest = clean(li.get_text(" ", strip=True).replace("\xa0", " ").replace(strong_text, "", 1))
    if rest:
        return [rest]

    # event is in the next sibling <li>
    sibling = li.find_next_sibling("li")
    if sibling and not sibling.find("strong"):
        return [clean(sibling.get_text(" ", strip=True))]

    return []


def clean(text):
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()

def main():
    events = parse_calendar()

    os.makedirs("data", exist_ok=True)
    with open("data/calendar.json", "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)

    print("calendar events found:", len(events))

if __name__=="__main__":
    main()