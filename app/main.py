# app/main.py
from __future__ import annotations

import os
from uuid import uuid4
from typing import Dict, Optional, List
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel, Field


# ---------- App & Middleware ----------
app = FastAPI(title="Personal Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # TODO: tighten to your Render domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Root / Health / Version ----------
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h2>Personal Agent</h2>
    <p>Backend is running.</p>
    <p><a href="/docs">Open API docs</a></p>
    """

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"version": os.getenv("GIT_SHA", "dev")}


# ---------- Chat (stub) ----------
class ChatIn(BaseModel):
    message: str = Field(..., min_length=1)

@app.post("/api/chat")
def chat(inp: ChatIn):
    msg = inp.message.strip()
    if not msg:
        raise HTTPException(status_code=400, detail="message is required")
    # TODO: replace with real OpenAI call
    return {"reply": f"You said: {msg}"}


# ---------- Calendar (.ics, no external deps) ----------
class EventIn(BaseModel):
    title: str
    start: datetime   # ISO 8601, e.g. 2025-09-12T14:00:00-07:00
    end: datetime     # must be after start
    description: Optional[str] = ""
    location: Optional[str] = ""

class EventOut(BaseModel):
    id: str
    title: str
    start: datetime
    end: datetime
    description: Optional[str] = ""
    location: Optional[str] = ""
    ics_path: str

# In-memory store (swap to DB later if needed)
EVENTS: Dict[str, Dict[str, object]] = {}

def _to_utc(dt: datetime) -> datetime:
    """Ensure UTC; treat naive as UTC."""
    return dt if dt.tzinfo is None else dt.astimezone(timezone.utc)

def _fmt_ics(dt: datetime) -> str:
    """RFC5545 UTC timestamp."""
    return _to_utc(dt).strftime("%Y%m%dT%H%M%SZ")

def _esc(text: str) -> str:
    """RFC5545 text escaping."""
    return (text or "").replace("\\", "\\\\").replace(";", r"\;").replace(",", r"\,").replace("\n", r"\n")

def _make_ics(uid: str, ev: EventIn) -> str:
    now = _fmt_ics(datetime.now(timezone.utc))
    dtstart = _fmt_ics(ev.start)
    dtend = _fmt_ics(ev.end)
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Personal Agent//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{now}",
        f"DTSTART:{dtstart}",
        f"DTEND:{dtend}",
        f"SUMMARY:{_esc(ev.title)}",
    ]
    if ev.description:
        lines.append(f"DESCRIPTION:{_esc(ev.description)}")
    if ev.location:
        lines.append(f"LOCATION:{_esc(ev.location)}")
    lines += ["END:VEVENT", "END:VCALENDAR"]
    return "\r\n".join(lines) + "\r\n"

@app.post("/calendar/events", response_model=EventOut)
def create_event(ev: EventIn):
    if ev.end <= ev.start:
        raise HTTPException(status_code=400, detail="end must be after start")
    eid = str(uuid4())
    ics_text = _make_ics(eid, ev)
    EVENTS[eid] = {"in": ev, "ics": ics_text}
    return EventOut(
        id=eid,
        title=ev.title,
        start=ev.start,
        end=ev.end,
        description=ev.description,
        location=ev.location,
        ics_path=f"/calendar/events/{eid}.ics",
    )

@app.get("/calendar/events/{event_id}.ics")
def download_event_ics(event_id: str):
    rec = EVENTS.get(event_id)
    if not rec:
        raise HTTPException(status_code=404, detail="event not found")
    headers = {"Content-Disposition": f'attachment; filename="event-{event_id}.ics"'}
    return Response(content=rec["ics"], media_type="text/calendar", headers=headers)

@app.get("/calendar/events", response_model=List[EventOut])
def list_events():
    out: List[EventOut] = []
    for eid, rec in EVENTS.items():
        ev: EventIn = rec["in"]  # type: ignore
        out.append(EventOut(
            id=eid,
            title=ev.title,
            start=ev.start,
            end=ev.end,
            description=ev.description,
            location=ev.location,
            ics_path=f"/calendar/events/{eid}.ics",
        ))
    return out


# ---------- Local dev entrypoint ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
