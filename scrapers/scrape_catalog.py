from bs4 import BeautifulSoup
import json
import os
from playwright.sync_api import sync_playwright

def main():
    # computing school majors
    CS_BS = "https://catalog.cofc.edu/preview_program.php?catoid=32&poid=6311"
    CITA_ART = "https://catalog.cofc.edu/preview_program.php?catoid=32&poid=6312"
    CITA_DIG_MEDIA = "https://catalog.cofc.edu/preview_program.php?catoid=32&poid=6444"
    CITA_GAME_DEV = "https://catalog.cofc.edu/preview_program.php?catoid=32&poid=6468"
    CITA_MUSIC = "https://catalog.cofc.edu/preview_program.php?catoid=32&poid=6313"
    CITA_THEATRE = "https://catalog.cofc.edu/preview_program.php?catoid=32&poid=6314"
    CIS = "https://catalog.cofc.edu/preview_program.php?catoid=32&poid=6309"
    CS_BA = "https://catalog.cofc.edu/preview_program.php?catoid=32&poid=6310"
    DATA_SCI = "https://catalog.cofc.edu/preview_program.php?catoid=32&poid=6498"
    SWEN = "https://catalog.cofc.edu/preview_program.php?catoid=32&poid=6500"

    majors = {"cs_bs": CS_BS, "cita_art": CITA_ART, "cita_dig_media": CITA_DIG_MEDIA, "cita_game_dev": CITA_GAME_DEV, "cita_music": CITA_MUSIC, "cita_theatre": CITA_THEATRE, "cis": CIS, "data_sci": DATA_SCI, "swen": SWEN, "cs_ba": CS_BA}

    for major, url in majors.items():

        soup = parse_majors(major, url)

        os.makedirs("data", exist_ok=True)
        with open(f"data/{major}.json", "w", encoding="utf-8") as f:
            json.dump(walker(soup), f, indent=2)

def walker(soup):
    elements = soup.select("div.acalog-core")
    results = []

    for el in elements:
        heading = (el.select_one("h2, h3, h4")).get_text(strip=True)
        courses = []

        for course in el.select("li.acalog-course"):
            courses.append(course.get_text(strip=True))

        section = {"heading": heading, "courses": courses}

        results.append(section)

    return results

def parse_majors(major, URL):
    soup = BeautifulSoup(fetch_majors(major, URL), "html.parser")
    print(f"{major} courses found:", len(soup.select("li.acalog-course")))

    return soup

def fetch_majors(major, URL):
    CACHE = f"cache/{major}.html"

    os.makedirs("cache", exist_ok=True)

    if os.path.exists(CACHE) and os.path.getsize(CACHE) > 0:
        html = open(CACHE, encoding="utf-8").read()
    else:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            page = b.new_page()
            page.goto(URL, wait_until="networkidle")
            html = page.content()
            b.close()

        if len(html) < 50_000 or "li.acalog-course" not in html:
            raise RuntimeError(f"bad fetch: {len(html)} chars")

        open(CACHE, "w", encoding="utf-8").write(html)

    return html

