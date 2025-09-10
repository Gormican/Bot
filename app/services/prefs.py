import json
from pathlib import Path
from typing import List
from app.models import AllPrefs, NewsPrefs, HomePrefs, CalendarPrefs, HomeSetIn, CalendarSetIn

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
PREFS_FILE = DATA_DIR / "prefs.json"

def _load() -> AllPrefs:
    if PREFS_FILE.exists():
        with PREFS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return AllPrefs(**data)
    return AllPrefs()

def _save(prefs: AllPrefs) -> None:
    with PREFS_FILE.open("w", encoding="utf-8") as f:
        json.dump(prefs.dict(), f, indent=2)

# ---- News ----
def get_news() -> NewsPrefs:
    return _load().news

def upsert_news(topics: List[str]) -> NewsPrefs:
    prefs = _load()
    s = set(prefs.news.topics)
    for t in topics:
        t = t.strip()
        if t:
            s.add(t)
    prefs.news.topics = sorted(s)
    _save(prefs)
    return prefs.news

def remove_topic(topic: str) -> NewsPrefs:
    prefs = _load()
    prefs.news.topics = [t for t in prefs.news.topics if t.lower() != topic.lower()]
    _save(prefs)
    return prefs.news

# ---- Home ----
def get_home() -> HomePrefs:
    return _load().home

def set_home(inp: HomeSetIn) -> HomePrefs:
    prefs = _load()
    if inp.zipcode:
        prefs.home.zipcode = inp.zipcode.strip()
        prefs.home.lat = None
        prefs.home.lon = None
    if inp.lat is not None:
        prefs.home.lat = float(inp.lat)
    if inp.lon is not None:
        prefs.home.lon = float(inp.lon)
    if inp.tz:
        prefs.home.tz = inp.tz
    _save(prefs)
    return prefs.home

# ---- Calendar ----
def get_calendar() -> CalendarPrefs:
    return _load().calendar

def set_calendar(inp: CalendarSetIn) -> CalendarPrefs:
    prefs = _load()
    prefs.calendar.ics = inp.ics.strip()
    _save(prefs)
    return prefs.calendar
