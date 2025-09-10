from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers.prefs import router as prefs_router
from app.routers.study import router as study_router
from app.routers.report import router as report_router
from app.routers.default import router as default_router

app = FastAPI(title="Personal Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(prefs_router)
app.include_router(study_router)
app.include_router(report_router)
app.include_router(default_router)
