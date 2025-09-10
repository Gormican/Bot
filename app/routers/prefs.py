from fastapi import APIRouter
from app.models import NewsPrefs, HomePrefs, CalendarPrefs, HomeSetIn, CalendarSetIn
from app.services import prefs as P

router = APIRouter(prefix="/prefs", tags=["prefs"])

@router.get("/news", response_model=NewsPrefs)
def get_news():
    return P.get_news()

@router.post("/news", response_model=NewsPrefs)
def upsert_news(topics: NewsPrefs):
    return P.upsert_news(topics.topics)

@router.delete("/news/{topic}", response_model=NewsPrefs)
def delete_topic(topic: str):
    return P.remove_topic(topic)

@router.get("/home", response_model=HomePrefs)
def get_home():
    return P.get_home()

@router.post("/home", response_model=HomePrefs)
def set_home(inp: HomeSetIn):
    return P.set_home(inp)

@router.get("/calendar", response_model=CalendarPrefs)
def get_calendar():
    return P.get_calendar()

@router.post("/calendar", response_model=CalendarPrefs)
def set_calendar(inp: CalendarSetIn):
    return P.set_calendar(inp)
