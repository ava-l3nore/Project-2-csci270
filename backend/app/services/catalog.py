"""Looks up a syllabus's course in the scraped CofC catalog major files (data/<major>.json)."""

import json
import re
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[3] / "data"

MAJOR_NAMES = {
    "cs_bs": "Computer Science BS",
    "cs_ba": "Computer Science BA",
    "cis": "Computer Information Systems BS",
    "data_sci": "Data Science BS",
    "swen": "Software Engineering BS",
    "cita_art": "Computing in the Arts BA (Art)",
    "cita_dig_media": "Computing in the Arts BA (Digital Media)",
    "cita_game_dev": "Computing in the Arts BA (Game Development)",
    "cita_music": "Computing in the Arts BA (Music)",
    "cita_theatre": "Computing in the Arts BA (Theatre)",
}

# catalog entries look like "CSCI 220 Computer Programming I (3)"
ENTRY_RE = re.compile(r"^([A-Z]{2,4}) (\d{3}[A-Z]?) (.+?) \(([^)]*)\)$")
# syllabus codes look like "CSCI 340", "CSCI-340" or "CSCI340"
CODE_RE = re.compile(r"\b([A-Z]{2,4})[\s-]?(\d{3}[A-Z]?)\b")


@lru_cache
def load_catalog() -> dict[str, dict]:
    """Map course code -> {"title", "credits", "counts_toward": [(major, section), ...]}."""
    courses: dict[str, dict] = {}
    for stem, major in MAJOR_NAMES.items():
        path = DATA_DIR / f"{stem}.json"
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as f:
            sections = json.load(f)
        for section in sections:
            for entry in section["courses"]:
                found = ENTRY_RE.match(entry)
                if not found:
                    continue
                code = f"{found.group(1)} {found.group(2)}"
                course = courses.setdefault(
                    code,
                    {"title": found.group(3), "credits": found.group(4), "counts_toward": []},
                )
                place = (major, section["heading"].rstrip(":"))
                if place not in course["counts_toward"]:
                    course["counts_toward"].append(place)
    return courses


def catalog_context(syllabus_text: str) -> str:
    """Return the catalog entry for the first course code in the syllabus that the catalog knows."""
    catalog = load_catalog()
    for subject, number in CODE_RE.findall(syllabus_text):
        course = catalog.get(f"{subject} {number}")
        if course:
            places = "; ".join(f"{major} ({section})" for major, section in course["counts_toward"])
            return (
                f"{subject} {number} - {course['title']} ({course['credits']} credit hours)\n"
                f"Counts toward: {places}"
            )
    return ""
