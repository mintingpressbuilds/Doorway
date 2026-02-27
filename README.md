# Doorway

The first AI reasoning engine derived from human cognition. Geometric bridging. Honest gap detection. Verifiable reasoning chains. Every output receipted.

## Install

```bash
pip install -r requirements.txt
```

Create a `.env` file (optional — runs locally without any keys):

```
ANTHROPIC_API_KEY=your_key_here
PRUV_API_KEY=pv_live_your_key_here
```

`ANTHROPIC_API_KEY` enables the content layer (Claude). Without it, the engine runs structure-only.
`PRUV_API_KEY` enables cloud chain sync. Without it, chains are verified locally.

## Run — CLI

Single input:

```bash
python cli.py run "How does compound interest work?"
```

## Run — API Server

Start the server:

```bash
python cli.py serve
```

Default: `http://0.0.0.0:8000`. Override with `--host` and `--port`.

### POST /run

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"input": "How does compound interest work?"}'
```

Request body:

```json
{"input": "your question", "session_name": "doorway_agi"}
```

Response:

```json
{
  "status": "GROUND | BRIDGE | CONFLICT | PROVISIONAL",
  "content": {"answer": "...", "confidence": 0.85, "implication": "increases", "success": true},
  "structure": {"closest_shape": "growth_system", "gap_score": 0.12, "fires": false, "...": "..."},
  "bridge": null,
  "conflict": {"conflict": false, "...": "..."},
  "chain": {"id": "abc123", "root": "xy_...", "length": 1, "verified": true},
  "receipt": {"chain_id": "abc123", "chain_root": "xy_...", "chain_length": 1, "chain_verified": true, "receipt": "..."}
}
```

### GET /health

```bash
curl http://localhost:8000/health
```

Returns `{"status": "ok", "engine": "doorway_agi"}`.

## Run — Python

```python
from main import run

result = run("How does compound interest work?")
# result["status"]  → "GROUND" | "BRIDGE" | "CONFLICT" | "PROVISIONAL"
# result["chain"]   → {"id", "root", "length", "verified"}
```

## Status Meanings

| Status | Meaning |
|---|---|
| GROUND | Known territory. Gap quiet or content leads with high confidence. |
| BRIDGE | Adjacent territory. Gap fires, geometric bridge built. Held as provisional. |
| CONFLICT | Content and structure disagree directionally. Neither treated as ground. |
| PROVISIONAL | Insufficient information. Content failed or confidence too low. |

## Test

```bash
python -m pytest tests/ -v
python examples/run_tests.py
```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | None | Content layer (Claude API) |
| `PRUV_API_KEY` | None | Cloud chain sync |
| `DOORWAY_MODEL` | `claude-sonnet-4-20250514` | Content layer model |

## Architecture

```
input
  ├── content_layer.run()      → answer + confidence + implication
  ├── gap_detector.run()       → closest shape + gap score + fires
  ├── bridge_builder.build()   → geometric bridge (if gap fires)
  └── conflict_detector.check() → directional agreement check
          │
          ▼
    status determination → GROUND | BRIDGE | CONFLICT | PROVISIONAL
          │
          ▼
    xy_wrap chain → {id, root, length, verified} + receipt
```

## License

All Rights Reserved. doorwayagi.com
