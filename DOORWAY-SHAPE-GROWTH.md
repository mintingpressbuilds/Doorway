# DOORWAY-SHAPE-GROWTH.md

## Session-Scoped Shape Library Growth — AGI Correction Layer

**Status:** Correction to Doorway Blueprint Phase 1
**Date:** March 1, 2026
**Overrides:** Any assumption in the Doorway Blueprint that the shape library is static or read-only during AGI operation.

-----

## Problem Statement

The Doorway Blueprint describes the shape library as 50 hardcoded shapes built once and never modified. This is incorrect. The derivation states explicitly:

```
# On confirmation:
A = A ∪ {bridge.domain}   — domain absorbed into library
|A| increases             — library expands
future gaps shrink        — compounding property
```

The 50 shapes are the **starting state** — not the permanent state. Every confirmed bridge becomes a new shape. The Blueprint treats the library as read-only. It is read-write.

-----

## Corrected Architecture

The shape library has three layers. The Blueprint only describes Layer 1. This document adds Layers 2 and 3 for AGI. The separate DOORWAY-ASI-PERSISTENCE.md document extends Layer 3 across session boundaries.

```
LAYER 1 — STATIC SEED (written once, never changes)
  50 Tier 1 shapes — hardcoded in shape_library.py
  This is the floor. Not the ceiling.

LAYER 2 — RUNTIME LIBRARY (in-memory, grows during session)
  Starts empty each session.
  Confirmed bridges absorbed here as new shapes.
  Gap detector matches against STATIC SEED + RUNTIME LIBRARY.
  Cleared on session end for AGI.

LAYER 3 — CONFIRMATION LOOP (the growth mechanism)
  Takes a bridge + validation signal.
  Extracts geometric signature from the bridge.
  Generates a new shape definition following the standard schema.
  Adds the new shape to the runtime library.
  Checks for Tier 2 emergence across all session bridges.
```

-----

## Component 1 — Runtime Shape Library

The runtime library extends the static seed during a session. The gap detector must match against both.

```python
# core/shape_library_runtime.py

from core.shape_library import get_all_shapes

class RuntimeShapeLibrary:
    """
    In-memory shape library that starts from the 50 static shapes
    and grows as bridges are confirmed during a session.
    """

    def __init__(self):
        # Load static seed
        self._static = get_all_shapes()
        # Session-scoped additions — starts empty
        self._runtime = {}
        # Confirmation history for this session
        self._confirmations = []

    def get_all_shapes(self):
        """Returns static + runtime shapes merged."""
        merged = dict(self._static)
        merged.update(self._runtime)
        return merged

    def get_shape(self, name):
        """Look up shape from runtime first, then static."""
        return self._runtime.get(name) or self._static.get(name)

    def shape_count(self):
        """Total shapes available (static + runtime)."""
        return len(self._static) + len(self._runtime)

    def runtime_count(self):
        """Number of shapes added during this session."""
        return len(self._runtime)

    def add_confirmed_shape(self, shape_name, shape_definition):
        """
        Add a confirmed bridge as a new shape to the runtime library.
        Shape definition must follow the standard schema.
        """
        # Validate schema
        required_fields = [
            "structure", "elements", "keywords_tier1", "keywords_tier2",
            "geometric_prediction", "implication_type", "analogs",
            "constraints", "color_dimensions"
        ]
        for field in required_fields:
            if field not in shape_definition:
                raise ValueError(f"Shape {shape_name} missing required field: {field}")

        # Mark as runtime-derived
        shape_definition["_source"] = "runtime_confirmed"
        shape_definition["_session_turn"] = len(self._confirmations) + 1

        self._runtime[shape_name] = shape_definition
        self._confirmations.append({
            "shape_name": shape_name,
            "definition": shape_definition,
        })

        return shape_definition

    def get_confirmations(self):
        """Return all confirmations from this session."""
        return self._confirmations

    def reset(self):
        """Clear runtime shapes. Called on session end for AGI."""
        self._runtime = {}
        self._confirmations = []
```

-----

## Component 2 — Confirmation Loop

The confirm() function is the mechanism by which the library grows. It is a first-class component — not a comment at the bottom of a pseudocode block.

When a bridge is built and validated, confirm() does three things:

1. Extracts the geometric signature from the bridge
1. Generates a new shape definition from that signature
1. Adds it to the runtime library

```python
# core/confirmation.py

from core.shape_library_runtime import RuntimeShapeLibrary

def confirm_bridge(runtime_library: RuntimeShapeLibrary, bridge_result: dict,
                   input_text: str, domain: str) -> dict:
    """
    Confirm a bridge and absorb it into the runtime shape library.

    A confirmed bridge becomes a new shape. The shape captures the
    geometric pattern that successfully bridged the gap, making it
    available for future gap detection within this session.

    Args:
        runtime_library: The session's RuntimeShapeLibrary instance
        bridge_result: The full bridge output from bridge_builder
        input_text: The original input that triggered the bridge
        domain: The domain classification of the input

    Returns:
        The new shape definition that was added to the library
    """
    # Extract the geometry that made this bridge work
    source_shape_name = bridge_result.get("shape_name", "unknown")
    source_shape = runtime_library.get_shape(source_shape_name)

    if not source_shape:
        return None

    # Generate a domain-specific shape derived from the bridge
    # The new shape inherits the geometry but is colored by the domain
    new_shape_name = f"{domain}_{source_shape_name}"

    # Don't duplicate if this exact shape already exists
    if runtime_library.get_shape(new_shape_name):
        return runtime_library.get_shape(new_shape_name)

    new_shape = {
        "structure": bridge_result.get("bridge", source_shape["structure"]),
        "elements": source_shape["elements"].copy(),
        "keywords_tier1": source_shape["keywords_tier1"].copy(),
        "keywords_tier2": source_shape["keywords_tier2"].copy(),
        "geometric_prediction": bridge_result.get(
            "geometric_prediction",
            source_shape["geometric_prediction"]
        ),
        "implication_type": bridge_result.get(
            "implication_type",
            source_shape["implication_type"]
        ),
        "analogs": source_shape["analogs"] + [domain],
        "constraints": source_shape["constraints"].copy(),
        "color_dimensions": source_shape["color_dimensions"].copy(),
        # Provenance tracking
        "_derived_from": source_shape_name,
        "_domain": domain,
        "_confidence": bridge_result.get("geometric_confidence", 0.0),
        "_bridge_text": bridge_result.get("bridge", ""),
    }

    # Extract domain-specific keywords from the input to enrich the shape
    input_words = set(input_text.lower().split())
    existing_keywords = set(
        new_shape["keywords_tier1"] + new_shape["keywords_tier2"]
    )
    # Add any input words that aren't already keywords (basic enrichment)
    # A more sophisticated version would use NLP extraction
    domain_keywords = [
        w for w in input_words
        if len(w) > 4 and w not in existing_keywords and w.isalpha()
    ][:5]  # Cap at 5 new keywords
    new_shape["keywords_tier2"].extend(domain_keywords)

    runtime_library.add_confirmed_shape(new_shape_name, new_shape)

    return new_shape
```

-----

## Component 3 — Within-Session Tier 2 Emergence Check

After each confirmation, check whether multiple confirmed bridges share cross-domain structure. If they do, a Tier 2 pattern may be emerging within the session.

For AGI, this is observational only — the Tier 2 shapes (Generative Complexity System and Intelligence System) are not active in AGI. But the emergence check runs so that:

1. The mechanism is proven before ASI builds on it
1. The session can report “Tier 2 emergence detected” even if it doesn’t act on it
1. ASI persistence has something to persist

```python
# core/session_emergence.py

from core.shape_library_runtime import RuntimeShapeLibrary

EMERGENCE_THRESHOLD = 0.65

def check_session_emergence(runtime_library: RuntimeShapeLibrary) -> dict:
    """
    Check for Tier 2 emergence patterns across confirmed bridges
    within the current session.

    For AGI: detection and reporting only.
    For ASI: detection triggers storage and Tier 2 activation.

    Returns:
        Dictionary with emergence status and any detected patterns.
    """
    confirmations = runtime_library.get_confirmations()

    if len(confirmations) < 2:
        return {
            "emergence_detected": False,
            "reason": "Minimum 2 confirmed bridges required",
            "confirmation_count": len(confirmations),
            "patterns": [],
        }

    # Group confirmations by source shape (the Tier 1 geometry they derived from)
    by_source = {}
    for conf in confirmations:
        source = conf["definition"].get("_derived_from", "unknown")
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(conf)

    # Group by domain
    by_domain = {}
    for conf in confirmations:
        domain = conf["definition"].get("_domain", "unknown")
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append(conf)

    patterns = []

    # Pattern 1: Same geometry confirmed across different domains
    # This is the core signal — one shape working in multiple unrelated areas
    for source_shape, confs in by_source.items():
        domains = list(set(c["definition"].get("_domain", "unknown") for c in confs))
        if len(domains) >= 2:
            avg_confidence = sum(
                c["definition"].get("_confidence", 0) for c in confs
            ) / len(confs)
            if avg_confidence > EMERGENCE_THRESHOLD:
                patterns.append({
                    "type": "cross_domain_confirmation",
                    "source_shape": source_shape,
                    "domains": domains,
                    "confirmation_count": len(confs),
                    "mean_confidence": round(avg_confidence, 4),
                    "description": (
                        f"{source_shape} geometry confirmed across "
                        f"{len(domains)} domains: {', '.join(domains)}"
                    ),
                })

    # Pattern 2: Different geometries converging in the same domain
    # This suggests the domain has structural richness worth mapping
    for domain, confs in by_domain.items():
        shapes = list(set(c["definition"].get("_derived_from", "unknown") for c in confs))
        if len(shapes) >= 2:
            patterns.append({
                "type": "domain_richness",
                "domain": domain,
                "shapes_confirmed": shapes,
                "confirmation_count": len(confs),
                "description": (
                    f"Domain '{domain}' shows {len(shapes)} distinct "
                    f"geometric patterns: {', '.join(shapes)}"
                ),
            })

    return {
        "emergence_detected": len(patterns) > 0,
        "patterns": patterns,
        "confirmation_count": len(confirmations),
        "runtime_shapes": runtime_library.runtime_count(),
        "total_shapes": runtime_library.shape_count(),
    }
```

-----

## Integration — How the Pipeline Changes

The existing Doorway pipeline runs:

```
input → gap_detector → bridge_builder → content_layer → conflict_detector → output
```

The corrected pipeline adds the confirmation loop:

```
input → gap_detector(runtime_library) → bridge_builder → content_layer →
  conflict_detector → output

IF bridge built AND status != CONFLICT:
  → confirm_bridge(runtime_library, bridge, input, domain)
  → check_session_emergence(runtime_library)
  → include emergence status in output
```

### Key changes to existing components:

**gap_detector.run()** — must accept a shape library parameter instead of importing the static library directly. It matches against whatever library is passed in.

```python
# Before (static):
from core.shape_library import get_all_shapes
shapes = get_all_shapes()

# After (runtime-aware):
def run(input_text, shape_library=None):
    if shape_library is None:
        from core.shape_library import get_all_shapes
        shapes = get_all_shapes()
    else:
        shapes = shape_library.get_all_shapes()
```

**Session initialization** — each new session creates a RuntimeShapeLibrary instance. All pipeline calls within that session use the same instance.

```python
# At session start:
from core.shape_library_runtime import RuntimeShapeLibrary
session_library = RuntimeShapeLibrary()
# shape_count() == 50 at start

# After first confirmed bridge:
# shape_count() == 51

# After second confirmed bridge from different domain:
# shape_count() == 52
# check_session_emergence() may detect cross-domain pattern
```

**Session end** — for AGI, call `session_library.reset()`. The runtime shapes are gone. Next session starts from 50 again.

-----

## Confirmation Trigger

When does confirm() fire? Two options:

**Option A — Automatic confirmation on GROUND status.**
If a bridge was built in a prior turn and the follow-up question in the same domain results in GROUND status (both layers agree), the bridge is retroactively confirmed. The geometry held.

**Option B — Explicit human confirmation.**
The user signals that a bridge was useful or accurate. This could be a thumbs up, a “yes that’s right” response, or a dedicated confirm action in the UI.

**Recommended: Both.** Option A runs silently. Option B is the human-in-the-loop verification. Either trigger fires confirm(). Both firing for the same bridge is fine — it just doesn’t duplicate the shape.

-----

## What This Changes About AGI

Before this document:

- AGI has 50 shapes. Always 50. Every session identical.
- No learning within session. No compounding.
- The gap detector sees the same library on turn 1 and turn 100.

After this document:

- AGI starts with 50 shapes. Grows during session.
- Confirmed bridges become new shapes available to subsequent turns.
- The gap detector on turn 10 has access to shapes that didn’t exist on turn 1.
- Session ends → reset to 50. Growth is ephemeral.
- The mechanism is proven. ASI makes it permanent.

-----

## Boundary with ASI

This document covers AGI session-scoped growth only. Three things are explicitly deferred to DOORWAY-ASI-PERSISTENCE.md:

1. **Persistence across sessions** — confirmed shapes written to Supabase, loaded on next session start.
1. **Tier 2 shape activation** — Generative Complexity System and Intelligence System become active in ASI only.
1. **Full network intersection** — Tier 2 emergence runs across lifetime bridge history, not just current session.

AGI proves the growth mechanism works. ASI makes it permanent and adds wisdom emergence.
