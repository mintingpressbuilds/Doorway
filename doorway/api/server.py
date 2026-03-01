# api/server.py — Phase 9: API Server (Component 7)
# Exposes the engine over HTTP. Both vantagepoint and doorway-platform consume this.
# Sessions hold shape_library and bridge_history state.

import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
from pydantic import BaseModel
from ..main import run
from ..core.shape_library_loader import load_full_library
from ..core.bridge_history import load_bridge_history

app = FastAPI(title="Doorway AGI", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["POST", "GET"], allow_headers=["*"])


def _get_supabase_client():
    """Return a Supabase client if credentials are configured, else None."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        return None
    try:
        from supabase import create_client
        return create_client(url, key)
    except Exception:
        return None


# Session state: each session holds a shape_library dict and bridge_history list
_sessions: Dict[str, dict] = {}


def _get_session(session_name: str, user_id: str = None) -> dict:
    if session_name not in _sessions:
        sb = _get_supabase_client()
        library = load_full_library(supabase_client=sb)
        history = load_bridge_history(user_id, supabase_client=sb) if user_id else []
        _sessions[session_name] = {
            "shape_library": library,
            "bridge_history": history,
            "supabase_client": sb,
        }
    return _sessions[session_name]


class HistoryMessage(BaseModel):
    role: str
    content: str


class ReasoningRequest(BaseModel):
    input: str
    session_name: str = "doorway_agi"
    user_id: Optional[str] = None
    history: Optional[List[HistoryMessage]] = None


@app.post("/run")
async def reasoning(req: ReasoningRequest):
    print(f"REQUEST BODY: {json.dumps(req.model_dump())}")
    if not req.input.strip():
        raise HTTPException(status_code=400, detail="Input required")
    history = [m.model_dump() for m in req.history] if req.history else None

    session = _get_session(req.session_name, req.user_id)
    return run(
        req.input, verbose=False, history=history,
        shape_library=session["shape_library"],
        bridge_history=session["bridge_history"],
        supabase_client=session["supabase_client"],
        user_id=req.user_id,
        session_name=req.session_name,
    )


@app.post("/session/reset")
async def reset_session(session_name: str = "doorway_agi"):
    """Drop session state. Next request rebuilds from database."""
    _sessions.pop(session_name, None)
    return {"status": "reset", "session_name": session_name}


@app.get("/health")
async def health():
    return {"status": "ok", "engine": "doorway_agi"}
