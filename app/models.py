from pydantic import BaseModel, Field
from typing import List, Optional

class NewsPrefs(BaseModel):
    topics: List[str] = Field(default_factory=list)

class HomePrefs(BaseModel):
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz: str = "America/Los_Angeles"
    zipcode: Optional[str] = None  # optional helper

class CalendarPrefs(BaseModel):
    ics: Optional[str] = None

class AllPrefs(BaseModel):
    news: NewsPrefs = NewsPrefs()
    home: HomePrefs = HomePrefs()
    calendar: CalendarPrefs = CalendarPrefs()

class StudyQuestion(BaseModel):
    question: str

class HomeSetIn(BaseModel):
    # allow either zipcode or lat/lon + tz
    zipcode: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz: Optional[str] = None

class CalendarSetIn(BaseModel):
    ics: str
