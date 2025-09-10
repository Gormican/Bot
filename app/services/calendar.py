import requests
from datetime import date
import pytz
from ics import Calendar
from typing import List, Tuple, Optional

def today_events(ics_url: Optional[str], tzname: str) -> Tuple[List[str], str]:
    """Return list of today’s events and a status string."""
    if not ics_url:
        return [], "No calendar connected yet."

    try:
        resp = requests.get(ics_url, timeout=15)
        resp.raise_for_status()
        cal = Calendar(resp.text)
    except Exception:
        return [], "Calendar couldn’t be loaded."

    try:
        tz = pytz.timezone(tzname)
    except Exception:
        tz = pytz.timezone("America/Los_Angeles")

    today_local = date.today()
    events_today = []
    try:
        for ev in cal.events:
            start = ev.begin.astimezone(tz).date() if ev.begin else None
            if start == today_local:
                title = ev.name or "Untitled"
                start_time = ev.begin.astimezone(tz).strftime("%-I:%M %p") if ev.begin else ""
                events_today.append(f"{title} at {start_time}".strip())
    except Exception:
        return [], "Calendar parsed but reading events failed."

    if not events_today:
        return [], "No events today."
    return events_today, "Calendar loaded."
