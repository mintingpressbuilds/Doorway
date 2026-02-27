# CLAUDE.md — Doorway AGI Engine

## What This Repo Is

The AGI reasoning engine. Geometric bridging with honest gap detection derived from human cognition. This is infrastructure — not a chatbot, not a wrapper, not a SaaS feature.

## Before Writing Any Code

Read `BLUEPRINT.md` completely. It is the master build specification. Every build decision, every phase, every verification gate is defined there. Follow it exactly. Build in the exact sequence specified. Do not skip phases. Do not combine phases.

## Build Order

Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8 → Phase 9. Each phase confirmed before the next begins.

## Critical Rules

- The shape library is the most important work. All 50 shapes must pass the cross-domain validation test (biology + economics + physics) before any other component is built.
- The gap score is not a confidence metric. It measures how much maximum potential is pressing against the boundary of known geometry.
- xy_wrap api_key must be conditional — only passed if PRUV_API_KEY is present in environment. Local dev runs with zero network dependency.
- The content layer model string must be configurable via DOORWAY_MODEL env var.
- Status determination includes a content-leads path for GROUND. Read Phase 7 carefully.
- Tier 2 shapes are NOT in this build. They are ASI components. Do not implement them.
- The toolkit (8 instruments) is NOT in this build. It is the next build after the core is confirmed.
- Do not add alignment mechanisms, safety filters, or value injection. Honest uncertainty is the safety mechanism.
- The run() function must serialize the chain object into { id, root, length, verified }. This is the interface contract downstream repos consume.

## Stack

- Python 3.11+
- anthropic (content layer)
- xycore (chain primitive — imported via pruv)
- pruv (xy_wrap, receipts, cloud sync)
- fastapi + uvicorn (API server)
- pytest (testing)

## Definition of Done

All 11 checks in BLUEPRINT.md must pass. The API server must respond correctly on POST /run. README must document how to run (CLI + API).
