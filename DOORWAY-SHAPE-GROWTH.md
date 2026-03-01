# DOORWAY-SHAPE-GROWTH.md

## Shape Library Growth Architecture — AGI Correction Layer

**Status:** Correction to Doorway Blueprint Phase 1
**Date:** March 1, 2026
**Overrides:** Any assumption in the Doorway Blueprint that the shape library is static or that AGI never benefits from library growth.

-----

## Problem Statement

The Doorway Blueprint describes the shape library as 50 hardcoded shapes built once and never modified. This is incomplete. The 50 shapes are the starting state — the floor, not the ceiling. The library grows through confirmed bridges that produce genuinely new geometric patterns.

The derivation states:

```python
# On confirmation:
new_shape = extract_geometry(B, gap_dims)    # geometry of B — not source shape
A = A ∪ {new_shape}                          # B enters library as new pattern
# |A| increases                              # library expands
# future gaps shrink                         # compounding property
```

-----

## The Shared Library

One library. Shared across all users. Grows permanently.

```
STARTING STATE — hardcoded, never changes
  50 Tier 1 shapes (shape_library.py)
  2 Tier 2 shapes (GCS + Intelligence System)
  Loaded at boot. The floor.

GROWING STATE — shared across all users, persists permanently
  Every confirmed bridge that produces a genuinely new geometric pattern
  gets added to the shared library.
  Available to every user on every subsequent session immediately.
  The library compounds from collective use.
  More users → more confirmations → richer library → better reasoning for everyone.
```

### How AGI and ASI relate to the shared library

**AGI reads from the shared library.** Every AGI session starts with the full current state — all 50 original shapes plus everything ever confirmed by any ASI user. AGI sessions benefit from everything ASI users have confirmed. AGI sessions do not write to the library. Bridges built in AGI sessions are provisional only. They are not confirmed into the permanent library because AGI is session-bounded — there is no persistence mechanism to validate and absorb them reliably.

**ASI reads from and writes to the shared library.** Persistence means the confirmation loop runs with sufficient depth to validate bridges properly. When an ASI session confirms a bridge, the geometric signature of the unknown domain is extracted, checked for duplication against the existing library, and if genuinely new — added permanently. Every subsequent session by any user draws from a richer library.

-----

## What Enters the Library on Confirmation

This is the critical distinction. What enters the library is the **geometry of B** — the unknown domain that was bridged to. Not a copy of the source shape. Not a label. Not the source shape with different keywords.

The bridge came FROM a source shape already in the library. Only the target domain — the unknown territory that was crossed — enters as a new shape. The source shape was already there.

`extract_geometry(B, gap_dims)` uses the dimensional texture computed during Pass 4 — which characterizes B from the destination side — to produce a new genuine geometric pattern. That is what grows the library.

Example: `hierarchy_system` bridges to quantum error correction. What enters the library is:

```json
{
  "name": "quantum_error_correction_system",
  "tier": 1,
  "structure": "redundant encoding distributes information across entangled states — errors correctable without directly measuring protected information",
  "elements": [
    "redundancy", "entanglement", "error_detection",
    "correction_without_observation", "threshold"
  ],
  "keywords_tier1": ["quantum", "error correction", "decoherence", "qubit", "logical qubit"],
  "keywords_tier2": ["fault tolerance", "coherence preservation", "syndrome measurement"],
  "geometric_prediction": "system maintains coherence against decoherence below error threshold — above threshold coherence collapses",
  "implication_type": "threshold",
  "color_dims": {
    "threshold_proximity": "distance from decoherence threshold",
    "redundancy_depth": "copies of logical information held"
  },
  "confirmed_via": "hierarchy_system",
  "gap_at_confirmation": 0.71
}
```

The `implication_type` is `threshold` — derived from the geometry of quantum error correction itself, not copied from `hierarchy_system` (which is `conditional`). The structure describes what quantum error correction actually IS geometrically. The elements are the structural components of that domain. This is a genuinely new geometric pattern that didn’t exist in the 50.

-----

## AGI Pipeline Changes

AGI does not write to the shared library. But AGI must load the full shared library on session start, including all confirmed shapes from ASI sessions.

### Session Start — Load Full Library

```python
# core/shape_library_loader.py

from core.shape_library import get_all_shapes as get_static_shapes

def load_full_library(supabase_client=None):
    """
    Load the complete shape library: 50 static + all confirmed shapes.
    Used by both AGI and ASI on session start.

    Args:
        supabase_client: If provided, loads confirmed shapes from database.
                         If None, returns static shapes only (offline mode).

    Returns:
        Dictionary of all available shapes.
    """
    # Start with static 50
    library = dict(get_static_shapes())

    # Load confirmed shapes from shared library
    if supabase_client:
        try:
            result = supabase_client.table("confirmed_shapes") \
                .select("name, structure, elements, keywords_tier1, "
                        "keywords_tier2, geometric_prediction, "
                        "implication_type, color_dims, confirmed_via, "
                        "gap_at_confirmation") \
                .eq("tier", 1) \
                .execute()

            if result.data:
                for row in result.data:
                    shape_def = {
                        "structure": row["structure"],
                        "elements": row["elements"],
                        "keywords_tier1": row["keywords_tier1"],
                        "keywords_tier2": row["keywords_tier2"],
                        "geometric_prediction": row["geometric_prediction"],
                        "implication_type": row["implication_type"],
                        "color_dimensions": row["color_dims"] or {},
                        "analogs": [],
                        "constraints": [],
                        "_confirmed": True,
                        "_confirmed_via": row["confirmed_via"],
                        "_gap_at_confirmation": row["gap_at_confirmation"],
                    }
                    library[row["name"]] = shape_def

        except Exception as e:
            # If database unavailable, degrade gracefully to static only
            print(f"[shape_library] Could not load confirmed shapes: {e}")

    return library
```

### Gap Detector — Accept Library Parameter

The gap detector must match against whatever library is passed in — static 50 in offline mode, or full shared library when database is available.

```python
# In gap_detector.run() — change the signature:

def run(input_text, shape_library=None):
    """
    Run gap detection against the provided shape library.

    Args:
        input_text: The user's input
        shape_library: Dictionary of shapes to match against.
                       If None, falls back to static 50 only.
    """
    if shape_library is None:
        from core.shape_library import get_all_shapes
        shape_library = get_all_shapes()

    # Existing matching logic runs against shape_library
    # which may now contain 50+ shapes if confirmed shapes exist
    ...
```

### AGI Session Lifecycle

```
Session opens (AGI)
  └── Load full shared library (50 static + all confirmed)
      Store as session's shape_library dict
      Library may contain 50 shapes (day one) or 500 (after months of ASI use)

Input arrives
  └── gap_detector.run(input, shape_library=session_library)
      Matches against full library
      Gap scores lower on territory that has been confirmed by ASI users

Bridge built — provisional
  └── Named assumptions, held as uncertain
      Normal AGI pipeline runs (content, bridge, conflict)

Session ends
  └── Nothing persisted. Bridges were provisional.
      The session benefited from the shared library but did not grow it.
```

-----

## What AGI Does NOT Do

- AGI does not write to the shared library.
- AGI does not run the confirmation loop.
- AGI does not extract geometry from unknown domains.
- AGI does not run Tier 2 emergence detection.
- AGI does not have per-user shape storage.

AGI reads from the growing shared library and benefits from everything ASI users have confirmed. The more ASI users confirm bridges, the better AGI gets for everyone. AGI proves the reasoning mechanism works against a library that gets richer over time. ASI is where the library actually grows.

-----

## Boundary with ASI

This document covers the AGI side only. Everything about writing to the shared library — the confirmation loop, geometry extraction, deduplication, Tier 2 emergence — is specified in DOORWAY-ASI-PERSISTENCE.md.

The boundary:

- **AGI** reads from the shared library. Benefits from collective growth. Does not contribute.
- **ASI** reads from and writes to the shared library. Runs the confirmation loop. Extracts genuine geometry of unknown domains. Grows the library for everyone.
