-- Doorway Supabase Schema
-- Two tables: confirmed_shapes (shared) and bridge_history (per-user).

-- confirmed_shapes: Shared across all users. No user_id.
-- Every confirmed bridge that produces a genuinely new geometric pattern
-- gets added here. Available to every user on every subsequent session.
CREATE TABLE IF NOT EXISTS confirmed_shapes (
    id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name        TEXT UNIQUE NOT NULL,
    tier        INTEGER DEFAULT 1,
    structure   TEXT NOT NULL,
    elements    JSONB NOT NULL DEFAULT '[]',
    keywords_tier1    JSONB NOT NULL DEFAULT '[]',
    keywords_tier2    JSONB NOT NULL DEFAULT '[]',
    geometric_prediction TEXT NOT NULL,
    implication_type     TEXT NOT NULL,
    color_dims           JSONB DEFAULT '{}',
    confirmed_via        TEXT NOT NULL,
    gap_at_confirmation  FLOAT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_confirmed_shapes_tier
    ON confirmed_shapes (tier);
CREATE INDEX IF NOT EXISTS idx_confirmed_shapes_name
    ON confirmed_shapes (name);

-- bridge_history: Per-user. Tracks every bridge built across sessions.
-- Used for Tier 2 emergence detection and user-specific history.
CREATE TABLE IF NOT EXISTS bridge_history (
    id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id     TEXT NOT NULL,
    input_text  TEXT NOT NULL DEFAULT '',
    source_shape    TEXT NOT NULL,
    target_domain   TEXT NOT NULL,
    bridge_text     TEXT NOT NULL DEFAULT '',
    gap_score       FLOAT NOT NULL DEFAULT 0,
    geometric_confidence FLOAT NOT NULL DEFAULT 0,
    implication_type     TEXT NOT NULL DEFAULT 'conditional',
    gap_dims        JSONB DEFAULT '{}',
    status          TEXT NOT NULL DEFAULT 'provisional',
    session_name    TEXT DEFAULT 'doorway_agi',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_bridge_history_user
    ON bridge_history (user_id);
CREATE INDEX IF NOT EXISTS idx_bridge_history_user_created
    ON bridge_history (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_bridge_history_source
    ON bridge_history (source_shape);
