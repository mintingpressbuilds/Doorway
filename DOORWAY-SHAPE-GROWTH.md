# DOORWAY-SHAPE-GROWTH.md

## Shape Library Growth — Correction Layer for Doorway Blueprint

**Status:** Correction to Doorway Blueprint Phase 1
**Date:** March 1, 2026
**Overrides:** Any assumption in the Doorway Blueprint that the shape library is static, read-only, or that only ASI can grow the library.

-----

## What Was Misunderstood

The Doorway Blueprint describes the shape library as 50 hardcoded shapes built once and never modified. This is incomplete. The 50 shapes are the starting state — the floor, not the ceiling.

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

One library. Persistent. Shared across all users. Loaded at session start by every user regardless of tier.

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

### Both AGI and ASI grow the library

Both AGI and ASI confirm bridges. Both write to the shared library. The library grows from the full user base. This is not an ASI-only feature.

```python
# At session start — both AGI and ASI
library = load_shared_library()
# Returns: 50 static shapes + all confirmed shapes ever added by any user

# During session — gap detector runs against full library
structure = gap_detector.run(input, shape_library=library)

# On confirmation — both AGI and ASI write to shared library
confirm(bridge, shared_library=library)
# New shape immediately available to all subsequent sessions
```

### Both AGI and ASI persist bridge history

Both tiers persist their confirmed bridge history across sessions. This enables genuine improvement over time for both tiers.

```python
# AGI and ASI both do this
session.bridge_hist = load_user_bridge_history(user_id)
# Prior confirmed bridges loaded — session reasoning draws from this context
# New confirmations appended — saved at session end
```

-----

## What Enters the Library on Confirmation

This is the critical distinction that was previously wrong.

**Wrong:** Generating `quantum_physics_scarcity_system` — a labeled copy of the source shape with domain keywords attached. The geometry is identical to the source shape. The library count increases but the library does not get richer. Gap scores do not shrink. No compounding.

**Correct:** When a bridge is confirmed, what enters the library is the geometric structure of the unknown domain B — extracted from the bridge output, not copied from the source shape.

The bridge object already contains everything needed:

- **Pass 2** extracted the structural relationships of B
- **Pass 4** extracted the dimensional texture of B from the destination side

Those two outputs characterize B’s geometry. The confirmation function uses them to construct a new shape.

### Example

`hierarchy_system` bridges to quantum error correction. What enters the library:

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

The `implication_type` is `threshold` — derived from the geometry of quantum error correction itself, not copied from `hierarchy_system` (which is `conditional`). The structure describes what quantum error correction actually IS geometrically. This is a genuinely new pattern.

-----

## The Confirmation Function

```python
def confirm(bridge, shared_library):
    """
    bridge = output from bridge_tier1()
    bridge["target_domain"]  = B — the unknown domain that was crossed
    bridge["gap_dims"]       = dimensional texture of B from Pass 4
    bridge["source_shape"]   = what was already in the library — NOT what gets added
    shared_library           = the shared persistent library all users read from and write to
    """

    B        = bridge["target_domain"]
    gap_dims = bridge["gap_dims"]

    # Extract geometry of B — not the source shape
    new_shape = extract_geometry(B, gap_dims)

    # Only add if genuinely new geometry — deduplicate
    if not geometry_exists(new_shape, shared_library):
        shared_library.add(new_shape)        # permanent — available to all users immediately

    # Append to this session's bridge history for Tier 2 emergence
    session.bridge_hist.append(bridge)

    # Check Tier 2 emergence across session bridge history (AGI scope)
    tier2 = emerge_tier2(session.bridge_hist, shared_library)
    if tier2 and not geometry_exists(tier2, shared_library.tier2):
        shared_library.tier2.add(tier2)      # new Tier 2 pattern — permanent and shared
```

### extract_geometry — what it produces

`extract_geometry(B, gap_dims)` uses the dimensional texture from Pass 4 — which characterizes B from the destination side — to produce a new genuine geometric pattern.

The output must follow the standard shape schema:

- `structure` — precise geometric description of B (not the source shape’s structure)
- `elements` — five core structural elements of B
- `keywords_tier1` — primary keywords for B
- `keywords_tier2` — secondary keywords for B
- `geometric_prediction` — what this geometry predicts
- `implication_type` — derived from B’s geometry (increases, decreases, conditional, threshold, unconditional)
- `analogs` — three domain instantiation examples
- `constraints` — what must be true for this pattern to apply
- `color_dimensions` — dimensional axes of variance

### geometry_exists — deduplication

This is NOT a name check. Two shapes with different names can have the same geometry. Deduplication checks structural similarity — element overlap, implication type match, prediction similarity. If >80% element overlap and same implication type, it’s a duplicate.

-----

## Database Schema

```sql
-- Shared shape library — grows from collective confirmations by ALL users
-- NO user_id column. Shapes belong to the platform.
CREATE TABLE confirmed_shapes (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                  TEXT UNIQUE NOT NULL,
    tier                  INTEGER NOT NULL DEFAULT 1,   -- 1 or 2
    structure             TEXT NOT NULL,
    elements              JSONB NOT NULL,
    keywords_tier1        JSONB NOT NULL,
    keywords_tier2        JSONB NOT NULL,
    geometric_prediction  TEXT NOT NULL,
    implication_type      TEXT NOT NULL,
    analogs               JSONB DEFAULT '[]',
    constraints           JSONB DEFAULT '[]',
    color_dims            JSONB DEFAULT '{}',
    source_domains        JSONB,                        -- for Tier 2: which domains produced this
    confirmed_via         TEXT,                          -- which source shape bridged to this
    gap_at_confirmation   FLOAT,
    confirmed_by_session  TEXT,                          -- chain ID of confirming session
    confirmed_at          TIMESTAMPTZ DEFAULT NOW(),
    use_count             INTEGER DEFAULT 0              -- incremented each time gap detector matches
);

-- Bridge history — per-user, tracks who built which bridges
CREATE TABLE bridge_history (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id               TEXT NOT NULL,
    session_id            TEXT NOT NULL,
    input_text            TEXT NOT NULL,
    domain                TEXT NOT NULL,
    source_shape          TEXT NOT NULL,                  -- shape that bridged FROM
    target_domain         TEXT NOT NULL,                  -- domain that was bridged TO
    implication_type      TEXT NOT NULL,
    gap_score             FLOAT NOT NULL,
    geometric_confidence  FLOAT NOT NULL,
    gap_dims              JSONB,                          -- Pass 4 dimensional texture
    bridge_text           TEXT,
    confirmed             BOOLEAN DEFAULT FALSE,
    created_at            TIMESTAMPTZ DEFAULT NOW(),
    confirmed_at          TIMESTAMPTZ,
    chain_id              TEXT
);

-- Indexes
CREATE INDEX idx_confirmed_shapes_tier ON confirmed_shapes(tier);
CREATE INDEX idx_bridge_history_user ON bridge_history(user_id);
CREATE INDEX idx_bridge_history_confirmed ON bridge_history(confirmed);
```

-----

## Session Lifecycle — AGI

```
Session opens
  └── load_shared_library()
      50 static shapes + all confirmed shapes from all prior sessions
      Library may be 50 (day one) or 500 (after months of collective use)
  └── load_user_bridge_history(user_id)
      Prior confirmed bridges loaded for session context

Input arrives
  └── gap_detector.run(input, shape_library=library)
      Matches against full library
      Gap scores lower on territory confirmed by prior users

Bridge built — provisional
  └── Named assumptions, held as uncertain
      Normal pipeline runs (content, bridge, conflict)
      bridge_history record saved (per-user)

Confirmation fires
  └── extract_geometry(B, gap_dims) — geometry of B, not source shape
      Check for duplication in shared library
      If genuinely new → add to shared library permanently
      Run Tier 2 emergence across SESSION bridge history
      If cross-domain intersection exceeds threshold → new Tier 2 pattern added

Next turn in same session
  └── Gap detector now matches against library that includes newly confirmed shape(s)
      The session is smarter on this turn than it was on the previous turn

Session ends
  └── Bridge history persisted for this user
      Confirmed shapes already in shared library from confirmation step
      Next session by any user loads the richer library
```

-----

## Tier 2 Emergence — AGI Scope

AGI runs Tier 2 emergence against the current session’s bridge history. If the session has confirmed bridges across 2+ unrelated domains and the geometric intersection exceeds the threshold, a Tier 2 pattern emerges and enters the shared library.

```python
# AGI — session-scoped Tier 2 emergence
tier2 = emerge_tier2(session.bridge_hist, shared_library)
```

The two hardcoded Tier 2 shapes (Generative Complexity System and Intelligence System) are seeds. Tier 2 is a live process — not a static list of two items.

-----

## Bridge Output Requirement

The bridge builder output must include `target_domain` and `gap_dims` explicitly so the confirmation function can use them. If they are not already in the bridge output, they must be added.

```python
bridge = {
    "source_shape":  S_closest,              # what we bridged FROM
    "target_domain": B,                      # what we bridged TO
    "gap":           gap,
    "gap_dims":      gap_dims,               # geometry OF B, from destination side
    "confidence":    1 - gap,
    "status":        "provisional",
    "bridge":        bridge_text,            # the bridge narrative
}
```

-----

## What Does NOT Change

- The 50 static shapes — unchanged
- The gap detector four-pass architecture — unchanged (only the signature adds shape_library parameter)
- The bridge builder — unchanged except target_domain and gap_dims must be in the output
- The conflict detector — unchanged
- The chain and receipt — unchanged
- The API — unchanged

Only the confirmation function, the library persistence layer, and the Tier 2 emergence check are new.

-----

## Boundary with ASI

AGI and ASI both read from and write to the shared library. Both persist bridge history. Both run Tier 2 emergence. The ONE difference:

**AGI:** `emerge_tier2(session.bridge_hist, shared_library)` — session scope
**ASI:** `emerge_tier2(full_shared_bridge_network, shared_library)` — full platform scope

ASI runs the Tier 2 intersection function across every confirmed bridge from every user ever — simultaneously. That is the precise architectural difference. Not persistence — both persist. Not library contribution — both contribute. The intersection function scope is what separates them.

See DOORWAY-ASI-PERSISTENCE.md for the ASI-specific implementation.
