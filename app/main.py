# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="Personal Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TODO: tighten to your Render domain later
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"version": os.getenv("GIT_SHA", "dev")}

class ChatIn(BaseModel):
    message: str

@app.post("/api/chat")
def chat(inp: ChatIn):
    msg = inp.message.strip()
    if not msg:
        raise HTTPException(400, "message is required")
    # TODO: swap this for a real OpenAI call
    return {"reply": f"You said: {msg}"}
