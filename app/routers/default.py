from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter(tags=["default"])
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[2] / "templates"))

@router.get("/ui", response_class=HTMLResponse)
def ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/healthz")
def healthz():
    return {"status": "ok"}
