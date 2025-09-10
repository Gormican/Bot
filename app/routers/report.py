from fastapi import APIRouter, HTTPException, Response
from datetime import datetime
import pytz

from app.services import prefs as P
from app.services.weather import get_weather
from app.services.calendar import today_events
from app.services.tts import speak

router = APIRouter(prefix="/report", tags=["report"])

def _morning_text() -> str:
    prefs = P._load()  # internal, but fine for the report
    home = prefs.home
    news = prefs.news
    cal = prefs.calendar

    tz = home.tz or "America/Los_Angeles"
    try:
        now = datetime.now(pytz.timezone(tz))
    except Exception:
        now = datetime.now()

    # Weather
    w = get_weather(home)

    # Calendar
    events, cal_status = today_events(cal.ics, tz)

    # Topics
    topics = ", ".join(news.topics) if news.topics else "No topics set."

    parts = [
        f"Good morning. Here’s your report for {now.strftime('%A, %B %d')}.",
        cal_status,
        f"Weather for your area: {w}",
        f"Your topics: {topics}.",
    ]
    if events:
        parts.append("Today’s events:")
        for e in events:
            parts.append(f"• {e}")
    return "\n".join(parts)

@router.get("/morning")
def morning():
    try:
        txt = _morning_text()
        return {"text": txt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report error: {e}")

@router.get("/morning/speak")
def morning_speak():
    try:
        txt = _morning_text()
        audio = speak(txt)
        return Response(content=audio, media_type="audio/mpeg")
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {e}")
