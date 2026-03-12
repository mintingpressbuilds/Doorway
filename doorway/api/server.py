# api/server.py — Phase 9: API Server (Component 7)
# Exposes the engine over HTTP. Both vantagepoint and doorway-platform consume this.
# Sessions hold shape_library and bridge_history state.

import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, List, Optional
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


# ── Session state ──
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


# ── doorway-memory integration ──
# Single Memory instance persists across requests. Shapes stored by one
# request are available to the next. Uses Supabase backend when credentials
# are present so memory survives server restarts.

from doorway_memory import (
    Memory, Shape, Dimension,
    find_containing_shapes, find_nearest_shapes, find_void,
)

_memory: Optional[Memory] = None


def _get_memory() -> Memory:
    global _memory
    if _memory is not None:
        return _memory

    sb_url = os.getenv("SUPABASE_URL")
    sb_key = os.getenv("SUPABASE_SERVICE_KEY")
    if sb_url and sb_key:
        backend = "supabase"
        config = {"url": sb_url, "key": sb_key}
    else:
        backend = "memory"
        config = None

    _memory = Memory(
        namespace="doorway_agi",
        backend=backend,
        config=config,
        anchor=False,
        growth=True,
        overlap=True,
        decay=True,
        merge=True,
        narrative=True,
    )
    return _memory


# ── Request / response models ──

class HistoryMessage(BaseModel):
    role: str
    content: str


class ReasoningRequest(BaseModel):
    input: str
    session_name: str = "doorway_agi"
    user_id: Optional[str] = None
    history: Optional[List[HistoryMessage]] = None


class MemoryTestRequest(BaseModel):
    point: Dict[str, float]


class MemoryStoreRequest(BaseModel):
    dimensions: Dict[str, Dict[str, float]]
    metadata: Optional[Dict[str, Any]] = None


class MemoryScanRequest(BaseModel):
    source_type: str
    data: Any


# ── Reasoning endpoints ──

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


# ── Memory endpoints ──

@app.get("/memory/chain")
async def memory_chain():
    """Chain timeline — all shapes ordered chronologically."""
    mem = _get_memory()
    shapes = list(mem.all_shapes())
    return {
        "chain": [
            {
                "shape_id": s.id,
                "dimensions": {
                    name: {"min": d.min_value, "max": d.max_value}
                    for name, d in s.dimensions.items()
                },
                "metadata": s.metadata,
                "anchor_id": s.anchor_id,
                "confidence": s.confidence,
                "hit_count": s.hit_count,
            }
            for s in shapes
        ],
        "count": len(shapes),
    }


@app.get("/memory/library")
async def memory_library():
    """All shapes with metadata, recall counts, source type."""
    mem = _get_memory()
    shapes = list(mem.all_shapes())
    return {
        "shapes": [
            {
                "shape_id": s.id,
                "dimensions": {
                    name: {"min": d.min_value, "max": d.max_value}
                    for name, d in s.dimensions.items()
                },
                "metadata": s.metadata,
                "confidence": s.confidence,
                "hit_count": s.hit_count,
                "parent_id": s.parent_id,
                "anchor_id": s.anchor_id,
            }
            for s in shapes
        ],
        "count": len(shapes),
    }


@app.post("/memory/test")
async def memory_test(req: MemoryTestRequest):
    """Test a point against memory — containing shapes, nearest, void check."""
    mem = _get_memory()
    all_shapes = list(mem.all_shapes())

    containing = find_containing_shapes(req.point, all_shapes)
    nearest = find_nearest_shapes(req.point, all_shapes)
    void = find_void(req.point, all_shapes)

    return {
        "containing": [
            {"shape_id": s.id, "confidence": s.confidence}
            for s in containing
        ],
        "nearest": [
            {"shape_id": s.id, "distance": d}
            for s, d in nearest
        ],
        "void": void,
    }


@app.post("/memory/store")
async def memory_store(req: MemoryStoreRequest):
    """Store a new shape in memory."""
    dims = {}
    for name, bounds in req.dimensions.items():
        if "min" not in bounds or "max" not in bounds:
            raise HTTPException(
                status_code=400,
                detail=f"Dimension '{name}' must have 'min' and 'max'",
            )
        dims[name] = Dimension(name, bounds["min"], bounds["max"])

    shape = Shape(dimensions=dims, metadata=req.metadata or {})
    mem = _get_memory()
    shape_id = mem.store(shape)
    return {"shape_id": shape_id}


@app.post("/memory/scan")
async def memory_scan(req: MemoryScanRequest):
    """Scan a data source and store extracted shapes."""
    mem = _get_memory()
    count = mem.scan_and_store(req.data, name=req.source_type)
    return {"shapes_stored": count}


@app.get("/memory/void")
async def memory_void():
    """Void analysis — percentage and regions across all known dimensions."""
    mem = _get_memory()
    all_shapes = list(mem.all_shapes())

    # Collect bounds from all stored shapes
    dim_bounds: Dict[str, list] = {}
    for s in all_shapes:
        for name, d in s.dimensions.items():
            if name not in dim_bounds:
                dim_bounds[name] = [d.min_value, d.max_value]
            else:
                dim_bounds[name][0] = min(dim_bounds[name][0], d.min_value)
                dim_bounds[name][1] = max(dim_bounds[name][1], d.max_value)

    # Expand bounds by 20% on each side so void detection sees edges
    for name in dim_bounds:
        span = dim_bounds[name][1] - dim_bounds[name][0]
        margin = max(span * 0.2, 1.0)
        dim_bounds[name][0] -= margin
        dim_bounds[name][1] += margin

    # Void percentage across all dimensions
    if dim_bounds:
        bounds_tuples = {n: tuple(b) for n, b in dim_bounds.items()}
        void_pct = mem.void_percentage(bounds_tuples)
    else:
        void_pct = 1.0

    # Void regions per dimension
    void_regions = []
    for name, (lo, hi) in dim_bounds.items():
        regions = mem.map_void(name, (lo, hi))
        for r in regions:
            void_regions.append({
                "dimensions": {
                    n: {"min": d.min_value, "max": d.max_value}
                    for n, d in r.dimensions.items()
                },
                "bounded_by": r.bounded_by,
            })

    return {
        "void_percentage": void_pct,
        "void_regions": void_regions,
    }


@app.post("/memory/maintain")
async def memory_maintain():
    """Run decay cycle — archive stale shapes."""
    mem = _get_memory()
    result = mem.maintain()
    return {"shapes_archived": result.get("archived", 0)}
