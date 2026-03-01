# core/confirmation.py — Confirmation Loop
# Extracts the geometry of the unknown domain B from a bridge.
# What enters the library is B's geometry — NOT a copy of the source shape.
# Deduplicates against existing library. Writes to shared confirmed_shapes
# table in Supabase (no user_id — shared across all users).
#
# extract_geometry uses the content layer (LLM) to produce genuine
# structural descriptions of B. Falls back to signal-based inference
# when ANTHROPIC_API_KEY is not set (offline/local dev).

import os
import json
import urllib.error
import urllib.request
from dotenv import load_dotenv

load_dotenv()

_API_KEY = os.getenv("ANTHROPIC_API_KEY")
_MODEL = os.getenv("DOORWAY_MODEL", "claude-sonnet-4-20250514")

# Minimum gap_score for a bridge to be confirmable
CONFIRM_GAP_THRESHOLD = 0.35

# Maximum keyword overlap with any existing shape before we call it a duplicate
DEDUP_OVERLAP_THRESHOLD = 0.70

# Valid implication types for the shape schema
_VALID_IMPL_TYPES = {"threshold", "increases", "decreases", "conditional"}

# ── Signals for offline implication inference ──
_THRESHOLD_SIGNALS = [
    "threshold", "critical", "tipping", "phase transition", "rupture",
    "breaking point", "saturation", "boiling", "melting", "capacity",
    "limit", "cliff", "snap", "collapse", "decoherence", "coherence",
    "error threshold", "tolerance", "fault tolerance",
]
_INCREASE_SIGNALS = [
    "compound", "exponential", "growth", "accumulate", "amplif",
    "accelerat", "scaling", "multiply", "spread", "viral",
    "compound interest", "snowball", "reinvest",
]
_DECREASE_SIGNALS = [
    "decay", "deplet", "erosion", "degradat", "attrition", "dissipat",
    "entropy", "decline", "fade", "wither", "half-life", "depreciat",
]


# ═══════════════════════════════════════════════════════════════════
# extract_geometry — the core extraction function
# ═══════════════════════════════════════════════════════════════════

def extract_geometry(bridge):
    """
    Extract the geometry of the unknown domain B from a bridge result.

    Uses the content layer (LLM) to analyze the bridge text and
    dimensional texture, producing a genuinely new geometric pattern
    that describes what B actually IS structurally.

    Falls back to signal-based inference when offline.

    Returns a shape definition dict, or None if extraction fails.
    """
    target_domain = bridge.get("target_domain", "unknown_domain")
    if target_domain == "unknown_domain":
        return None

    source_shape = bridge.get("shape_name", "unknown")
    gap_score = bridge.get("gap_score", 0)

    # Try LLM extraction — produces genuine geometry
    extracted = _extract_via_llm(bridge)

    # Fall back to signal-based inference (offline mode)
    if extracted is None:
        extracted = _extract_via_signals(bridge)

    if extracted is None:
        return None

    return {
        "name": target_domain,
        "tier": 1,
        "structure": extracted["structure"],
        "elements": extracted["elements"],
        "keywords_tier1": extracted["keywords_tier1"],
        "keywords_tier2": extracted["keywords_tier2"],
        "geometric_prediction": extracted["geometric_prediction"],
        "implication_type": extracted["implication_type"],
        "color_dims": extracted["color_dims"],
        "confirmed_via": source_shape,
        "gap_at_confirmation": gap_score,
    }


# ═══════════════════════════════════════════════════════════════════
# LLM extraction — uses bridge text + gap_dims to understand B
# ═══════════════════════════════════════════════════════════════════

_EXTRACTION_PROMPT = """You are extracting the geometric structure of an unknown domain.

A geometric bridge was built FROM the shape "{source_shape}" TO a target domain.

Bridge text (describes how the source geometry maps to the target):
{bridge_text}

Dimensional texture of the bridge:
{gap_dims}

The user's input that triggered this bridge:
{input_text}

Extract the genuine geometric structure of the TARGET DOMAIN — what it actually IS structurally. Do NOT copy the source shape's description. The target domain has its own geometry.

Respond with ONLY a JSON object (no markdown, no explanation):
{{
  "structure": "A precise 1-2 sentence description of how the target domain operates structurally — what its geometric pattern IS",
  "elements": ["3-5 structural components that make this domain work — these are the building blocks, not keywords"],
  "keywords_tier1": ["4-5 primary domain terms for keyword matching"],
  "keywords_tier2": ["5-8 secondary domain terms for keyword matching"],
  "geometric_prediction": "What this domain's geometry predicts about behavior — a specific structural claim",
  "implication_type": "one of: threshold, increases, decreases, conditional — based on the TARGET domain's geometry, not the source",
  "color_dims": {{"axis_name": "low_end_to_high_end"}}
}}"""


def _extract_via_llm(bridge):
    """
    Use the content layer LLM to extract B's genuine geometry from
    the bridge text and dimensional texture.

    Returns dict with structure/elements/etc, or None if unavailable.
    """
    if not _API_KEY:
        return None

    bridge_text = bridge.get("bridge", "")
    gap_dims = bridge.get("gap_dims", {})
    input_text = bridge.get("input_text", "")
    source_shape = bridge.get("shape_name", "unknown")

    prompt = _EXTRACTION_PROMPT.format(
        source_shape=source_shape,
        bridge_text=bridge_text,
        gap_dims=json.dumps(gap_dims),
        input_text=input_text,
    )

    payload = json.dumps({
        "model": _MODEL,
        "max_tokens": 500,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": _API_KEY,
            "anthropic-version": "2023-06-01",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read())
            text = data["content"][0]["text"].strip()
            # Strip markdown fences if present
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:text.rfind("```")]
            parsed = json.loads(text.strip())
            return _validate_extracted(parsed)
    except Exception as e:
        print(f"[confirmation] LLM extraction failed: {e}")
        return None


def _validate_extracted(parsed):
    """Validate and normalize the LLM extraction result."""
    if not isinstance(parsed, dict):
        return None

    structure = parsed.get("structure")
    elements = parsed.get("elements")
    if not structure or not elements:
        return None

    impl_type = parsed.get("implication_type", "conditional")
    if impl_type not in _VALID_IMPL_TYPES:
        impl_type = "conditional"

    return {
        "structure": str(structure),
        "elements": [str(e) for e in elements][:5],
        "keywords_tier1": [str(k) for k in parsed.get("keywords_tier1", elements[:4])][:5],
        "keywords_tier2": [str(k) for k in parsed.get("keywords_tier2", [])][:8],
        "geometric_prediction": str(parsed.get("geometric_prediction", "")),
        "implication_type": impl_type,
        "color_dims": parsed.get("color_dims", {}),
    }


# ═══════════════════════════════════════════════════════════════════
# Signal-based extraction — offline fallback
# ═══════════════════════════════════════════════════════════════════

_STOP_WORDS = frozenset([
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "during", "before", "after", "between", "out", "off", "over", "under",
    "again", "then", "here", "there", "when", "where", "why", "how",
    "all", "both", "each", "some", "no", "not", "very", "just", "now",
    "and", "but", "or", "if", "that", "this", "what", "which", "who",
    "its", "it", "about", "work", "works", "make", "makes", "does",
    "describe", "many", "much", "more", "most",
])


def _extract_via_signals(bridge):
    """
    Offline fallback: infer B's geometry from bridge text signals
    and dimensional texture. Produces reasonable but less precise
    geometry than LLM extraction.
    """
    input_text = bridge.get("input_text", "")
    bridge_text = bridge.get("bridge", "")
    gap_dims = bridge.get("gap_dims", {})
    target_domain = bridge.get("target_domain", "unknown_domain")

    domain_label = target_domain.replace("_system", "").replace("_", " ")
    domain_words = _extract_domain_words(input_text)

    impl_type = _infer_implication_type(input_text, gap_dims)
    elements = _derive_elements(domain_words, gap_dims)
    keywords_tier1 = domain_words[:5]
    keywords_tier2 = domain_words[5:13] + list(gap_dims.keys())
    color_dims = dict(gap_dims) if gap_dims else {}

    elem_str = ", ".join(elements[:3]) if elements else domain_label
    structure_templates = {
        "threshold": (
            f"{domain_label} operates through {elem_str} — "
            f"system maintains stability until critical threshold "
            f"triggers state change"
        ),
        "increases": (
            f"{domain_label} driven by {elem_str} — "
            f"output compounds non-linearly over time"
        ),
        "decreases": (
            f"{domain_label} governed by {elem_str} — "
            f"structure degrades following predictable rate toward residual state"
        ),
        "conditional": (
            f"{domain_label} structured around {elem_str} — "
            f"behavior depends on configuration of interacting components"
        ),
    }
    prediction_templates = {
        "threshold": (
            f"{domain_label} holds below critical threshold — "
            f"beyond that point {elem_str} collapse or transform"
        ),
        "increases": (
            f"{elem_str} compound producing non-linear growth in {domain_label}"
        ),
        "decreases": (
            f"{elem_str} degrade over time following predictable decay in {domain_label}"
        ),
        "conditional": (
            f"{domain_label} outcome depends on interaction between {elem_str}"
        ),
    }

    return {
        "structure": structure_templates.get(impl_type, structure_templates["conditional"]),
        "elements": elements,
        "keywords_tier1": keywords_tier1,
        "keywords_tier2": keywords_tier2,
        "geometric_prediction": prediction_templates.get(impl_type, prediction_templates["conditional"]),
        "implication_type": impl_type,
        "color_dims": color_dims,
    }


def _extract_domain_words(input_text):
    """Pull meaningful words from input."""
    words = [w.strip("?.,!\"'()") for w in input_text.lower().split()]
    return [w for w in words if w.isalpha() and len(w) > 2
            and w not in _STOP_WORDS]


def _infer_implication_type(input_text, gap_dims):
    """
    Determine B's implication type from the input text and dimensional
    texture. Scans for domain-specific signals.
    """
    text = input_text.lower()
    dim_text = " ".join(list(gap_dims.keys()) + list(gap_dims.values())).lower()
    combined = text + " " + dim_text

    threshold_score = sum(1 for s in _THRESHOLD_SIGNALS if s in combined)
    increase_score = sum(1 for s in _INCREASE_SIGNALS if s in combined)
    decrease_score = sum(1 for s in _DECREASE_SIGNALS if s in combined)

    if threshold_score >= 2:
        return "threshold"
    if threshold_score == 1 and increase_score == 0 and decrease_score == 0:
        return "threshold"
    if increase_score > decrease_score and increase_score >= 1:
        return "increases"
    if decrease_score > increase_score and decrease_score >= 1:
        return "decreases"
    return "conditional"


def _derive_elements(domain_words, gap_dims):
    """Extract B's structural elements from domain words and gap_dims."""
    elements = []
    for w in domain_words:
        if len(elements) >= 5:
            break
        if w not in elements:
            elements.append(w)
    for axis in gap_dims:
        if len(elements) >= 5:
            break
        if axis not in elements:
            elements.append(axis)
    return elements if elements else ["structure", "pattern", "relationship"]


# ═══════════════════════════════════════════════════════════════════
# Deduplication + Supabase write + confirm()
# ═══════════════════════════════════════════════════════════════════

def _is_duplicate(new_shape, shared_library):
    """
    Check if a shape with high keyword overlap already exists.
    Exact name match OR high keyword overlap = duplicate.
    """
    name = new_shape["name"]
    if name in shared_library:
        return True

    new_kw = set(new_shape["keywords_tier1"] + new_shape["keywords_tier2"])
    if not new_kw:
        return False

    for existing in shared_library.values():
        existing_kw = set(
            existing.get("keywords_tier1", []) + existing.get("keywords_tier2", [])
        )
        if not existing_kw:
            continue
        overlap = len(new_kw & existing_kw) / max(len(new_kw), 1)
        if overlap >= DEDUP_OVERLAP_THRESHOLD:
            return True

    return False


def _write_to_supabase(shape, supabase_client):
    """Write a confirmed shape to the shared confirmed_shapes table."""
    supabase_client.table("confirmed_shapes").upsert({
        "name": shape["name"],
        "tier": shape.get("tier", 1),
        "structure": shape["structure"],
        "elements": shape["elements"],
        "keywords_tier1": shape["keywords_tier1"],
        "keywords_tier2": shape["keywords_tier2"],
        "geometric_prediction": shape["geometric_prediction"],
        "implication_type": shape["implication_type"],
        "color_dims": shape.get("color_dims", {}),
        "confirmed_via": shape["confirmed_via"],
        "gap_at_confirmation": shape["gap_at_confirmation"],
    }, on_conflict="name").execute()


def confirm(bridge, shared_library, supabase_client=None):
    """
    Confirm a bridge and extract B's geometry into the shared library.

    Args:
        bridge: Bridge result dict (must include target_domain, gap_dims).
        shared_library: Current shared library dict (static + confirmed).
        supabase_client: If provided, writes confirmed shape to database.

    Returns:
        The new shape definition if genuinely new, or None if duplicate/invalid.
    """
    if not bridge or bridge.get("status") != "provisional":
        return None

    gap_score = bridge.get("gap_score", 0)
    if gap_score < CONFIRM_GAP_THRESHOLD:
        return None

    new_shape = extract_geometry(bridge)
    if new_shape is None:
        return None

    if _is_duplicate(new_shape, shared_library):
        return None

    # Add to in-memory shared library for this session
    shape_for_library = {
        "structure": new_shape["structure"],
        "elements": new_shape["elements"],
        "keywords_tier1": new_shape["keywords_tier1"],
        "keywords_tier2": new_shape["keywords_tier2"],
        "geometric_prediction": new_shape["geometric_prediction"],
        "implication_type": new_shape["implication_type"],
        "color_dimensions": new_shape.get("color_dims", {}),
        "analogs": [],
        "constraints": [],
        "_confirmed": True,
        "_confirmed_via": new_shape["confirmed_via"],
        "_gap_at_confirmation": new_shape["gap_at_confirmation"],
    }
    shared_library[new_shape["name"]] = shape_for_library

    # Persist to Supabase if available
    if supabase_client:
        try:
            _write_to_supabase(new_shape, supabase_client)
        except Exception as e:
            print(f"[confirmation] Could not write to Supabase: {e}")

    return new_shape
