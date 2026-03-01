# api/server.py — Phase 9: API Server (Component 7)
# Exposes the engine over HTTP. Both vantagepoint and doorway-platform consume this.

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from ..main import run

app = FastAPI(title="Doorway AGI", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["POST", "GET"], allow_headers=["*"])


class HistoryMessage(BaseModel):
    role: str
    content: str


class ReasoningRequest(BaseModel):
    input: str
    session_name: str = "doorway_agi"
    history: Optional[List[HistoryMessage]] = None


@app.post("/run")
async def reasoning(req: ReasoningRequest):
    if not req.input.strip():
        raise HTTPException(status_code=400, detail="Input required")
    history = [m.model_dump() for m in req.history] if req.history else None
    return run(req.input, verbose=False, history=history)


@app.get("/health")
async def health():
    return {"status": "ok", "engine": "doorway_agi"}
