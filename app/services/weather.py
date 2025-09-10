import requests
from typing import Optional, Tuple
from app.models import HomePrefs

def _resolve_zip(zipcode: str) -> Optional[Tuple[float, float]]:
    """Resolve US zipcode to (lat, lon) using zippopotam.us (no key)."""
    try:
        r = requests.get(f"https://api.zippopotam.us/us/{zipcode}", timeout=8)
        if r.status_code == 200:
            j = r.json()
            place = j["places"][0]
            lat = float(place["latitude"])
            lon = float(place["longitude"])
            return lat, lon
    except Exception:
        pass
    return None

def get_weather(home: HomePrefs) -> str:
    """Return a short weather string or an explanation."""
    tz = home.tz or "America/Los_Angeles"
    lat, lon = home.lat, home.lon

    # If only ZIP provided, resolve to lat/lon
    if (lat is None or lon is None) and home.zipcode:
        res = _resolve_zip(home.zipcode)
        if res:
            lat, lon = res

    if lat is None or lon is None:
        return "weather unavailable (missing home coordinates or ZIP)."

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "temperature_unit": "fahrenheit",
        "timezone": tz,
    }
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=10)
        r.raise_for_status()
        j = r.json()
        daily = j.get("daily", {})
        tmax = daily.get("temperature_2m_max", [None])[0]
        tmin = daily.get("temperature_2m_min", [None])[0]
        if tmax is not None and tmin is not None:
            return f"today’s high {round(tmax)}°F / low {round(tmin)}°F."
        return "details unavailable right now (imperial)."
    except Exception:
        return "details unavailable right now (imperial)."
