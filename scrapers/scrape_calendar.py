from bs4 import BeautifulSoup

def parse_calendar():
    soup = BeautifulSoup(fetch_calendar(), "html.parser")


def fetch_calendar():
    CACHE = f"cache/calendar.html"
    URL = "https://charleston.edu/registrar/calendar/index.php"