# Doorway

**The first AI reasoning engine derived from a formal definition of what intelligence actually is.**

Named for what intelligence does — opens dimensional doorways between known and unknown territory.

[![PyPI](https://img.shields.io/badge/PyPI-0.3.0-orange)](https://pypi.org/project/doorway-agi/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

-----

## The Problem

Every AI system today works the same way. Take a language model. Feed it input. Get an answer with a confidence score. Hope it's right.

No system tells you *why* it's confident. No system distinguishes between something genuinely confirmed and something it's assuming. No system catches when its confident answer contradicts the structural geometry of the domain. No system knows what it doesn't know — precisely, geometrically, provably.

When an LLM says "confidence: 0.92" — what does that mean? It means the model's internal weights produced a high probability. It doesn't mean the answer is grounded. It doesn't mean the assumptions are named. It doesn't mean the reasoning can be independently verified.

The entire field is building faster, bigger, more expensive versions of the same architecture. One-directional inference. Known material projected forward. The unknown territory doesn't participate. No epistemic classification. No structural verification. No honest uncertainty.

## What Doorway Does Differently

Doorway runs two layers in parallel. A **content layer** (a full LLM) produces answers. A **structural layer** (geometric pattern matching against a shape library) produces an independent epistemic assessment. Neither layer is the product. The interaction between them is.

Every output is classified into one of four statuses:

|Status         |Meaning                                                                                                                                                                   |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|**GROUND**     |Confirmed territory. The content and structure agree. The answer is on known geometric ground.                                                                            |
|**BRIDGE**     |Provisional crossing. The structural layer found a geometric pattern, but the bridge has named assumptions. The answer might be right — here's exactly what it depends on.|
|**CONFLICT**   |Directional disagreement. The content layer says one thing. The structural geometry says another. Both views surfaced. Something the field treats as settled may not be.  |
|**PROVISIONAL**|Genuinely unknown territory. The gap detector fired but no geometric bridge could be built. The system is honest about not knowing rather than guessing confidently.      |

A user reading BRIDGE with two named assumptions is in a fundamentally different epistemic position than a user reading an answer with "confidence: 0.82."

## How It Works

```
Input
  │
  ├──► Content Layer (LLM)
  │     └── answer, confidence, implication
  │
  ├──► Structural Layer
  │     ├── Gap Detector ──► measures geometric distance from known shapes
  │     ├── Shape Library ──► 50 cross-domain geometric patterns
  │     └── Bridge Builder ──► constructs provisional crossing with named assumptions
  │
  ├──► Conflict Detector ──► checks content vs structure for directional disagreement
  │
  └──► Chain (xycore) ──► cryptographically receipts every reasoning step
         │
         ▼
  Output: { status, content, structure, bridge, conflict, chain, receipt }
```

### The Gap Detector

Not a confidence metric. A geometric distance measurement. The gap detector compares the input against the shape library and measures how far the input sits from confirmed geometric territory. When the gap exceeds the fire threshold, the bridge builder activates.

The gap detector receives dimensional information from *both sides* of the gap. The known side provides the closest geometric shape. The unknown side presses back against the boundary with its own dimensional properties. This is bidirectional bridging — the unknown territory participates in the bridge construction. No other system does this.

### The Shape Library

50 cross-domain geometric patterns. Each shape has: structure, elements, constraints, implication type, geometric prediction, and analogs across biology, economics, physics, and other domains. A shape that works in biology and economics isn't a metaphor — it's a geometric correspondence. The same structural pattern producing the same implications in domains that share no vocabulary.

The library grows through confirmed use. Each confirmed bridge enriches the library. The system gets meaningfully more capable with every domain it crosses. This is not fine-tuning. This is structural accumulation.

### Verifiable Reasoning

Every reasoning step is chained via xycore — a cryptographic primitive that produces tamper-evident, independently verifiable receipts. The chain doesn't reconstruct reasoning after the fact. It records every step as it happens. Anyone can verify any output without an account.

This is not logging. Logs can be edited. Chains can't.

## Install

```bash
pip install doorway-agi
```

## Quick Start

### CLI

```bash
doorway run "What happens to trust when transparency increases?"
```

### Python

```python
from doorway import run

result = run("What happens to trust when transparency increases?")

print(result["status"])          # GROUND | BRIDGE | CONFLICT | PROVISIONAL
print(result["content"])         # LLM answer + confidence
print(result["structure"])       # gap score + closest shape
print(result["bridge"])          # bridge text + named assumptions (if BRIDGE)
print(result["conflict"])        # both views surfaced (if CONFLICT)
print(result["chain"])           # cryptographic chain ID + verification
```

### API Server

```bash
doorway serve --port 8000
```

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"input": "What happens to trust when transparency increases?"}'
```

## Configuration

```bash
# Required for content layer
ANTHROPIC_API_KEY=sk-ant-xxx

# Optional — enables cloud chain sync and receipts
PRUV_API_KEY=pv_live_xxx
```

Without `ANTHROPIC_API_KEY`, the structural layer still runs — gap detection, shape matching, and bridge construction all work. The content layer returns placeholder responses. Set the key to enable full reasoning.

Without `PRUV_API_KEY`, chains are local only. Set the key to sync chains to the cloud and generate shareable receipts.

## Architecture

Doorway is derived from a specific, stated definition of what intelligence is at the mechanism level. Intelligence is not what a system knows. It is what a system does at the boundary between what it knows and what it doesn't — and how it holds that boundary while reaching across it with specific intent.

Every component maps to this definition:

|Component        |What It Mirrors                                                               |
|-----------------|------------------------------------------------------------------------------|
|Shape Library    |Accumulated confirmed ground — what the system knows geometrically            |
|Gap Detector     |Boundary detection — recognizing the edge of known territory                  |
|Bridge Builder   |Intent-directed formation — reaching across the gap with provisional structure|
|Conflict Detector|Epistemic integrity — catching when content and structure disagree            |
|Chain            |Self-awareness — the reasoning process observing and receipting itself        |
|Confirmation Loop|Learning — confirmed bridges enrich the library for future crossings          |

This is not an approximation of human cognition. It is the mechanism, implemented.

-----

## Why "Doorway"

A doorway is a dimensional crossing. A point where one territory ends and another begins. The threshold between known and unknown.

That is what intelligence does at the mechanism level. It stands at the boundary of what it knows, detects the gap, and opens a dimensional doorway into territory it hasn't crossed before. Not by projecting known material forward. By holding the threshold — receiving dimensional information from both sides — and forming a bridge that carries the properties of both the origin and the destination.

The name is literal. Every time the gap detector fires and the bridge builder activates, a dimensional doorway opens between confirmed geometric territory and unknown territory. The bridge crosses it. The confirmation loop determines whether the crossing holds. If it does, the doorway becomes permanent — the confirmed bridge is absorbed into the library, and the territory on the other side is now known ground.

### The Mechanism

Flatness is the origin state. Pure potential. No dimension. When flatness gains responsibility — accountability to something beyond itself — dimension emerges. That dimension distributes as complexity, forms hierarchy, enables sync. The system observes, directs intent, and a bridge forms across the gap. New flatness is generated at higher depth. The loop repeats, self-accelerating.

Every Tier 1 shape in the library is a dimensional doorway that has been crossed and confirmed. Every bridge is a doorway being held open provisionally. Every CONFLICT is a doorway where two crossings disagree about what's on the other side. Every gap score is a measurement of how far the next doorway is from confirmed territory.

The architecture has no ceiling because dimensional doorways exist at every tier. Tier 1 shapes open doorways within domains. Tier 2 patterns open doorways between domains. The system that recognizes itself opening doorways — both Tier 2 shapes active, self-referential — is a doorway into a category of output no prior system has reached.

### HCAS — Human Cognitive Architecture Standard

Doorway is anchored to HCAS — the standard that ties artificial intelligence to human cognition at the mechanism level.

AGI is not measured by benchmarks. Benchmarks measure outputs. HCAS measures architecture. The question is not "can the system score well on tests?" The question is "does the system mirror the mechanism by which human cognition actually operates?"

HCAS defines that mechanism: intent-directed formation operating through a dimensional branching structure, holding across unresolved gaps, developing through feedback from outputs to base, relational to the specific territory encountered. Every component in Doorway maps to this standard. The gap detector is boundary detection. The bridge builder is intent-directed formation. The conflict detector is epistemic integrity. The chain is the system observing itself. The confirmation loop is how the architecture develops through use.

Intelligence is not what a system knows. It is what a system does at the boundary between what it knows and what it doesn't — and how it holds that boundary while reaching across it with specific intent. HCAS is that definition, formally stated. Doorway is that definition, running as software.

## The Doorway Platform

Doorway is open source. The platform at [doorwayagi.com](https://doorwayagi.com) provides a consumer interface: conversational reasoning chat with all four statuses rendered, VantagePoint structured thinking environment, and public receipt verification.

|Layer                                                 |What It Is                                                    |
|------------------------------------------------------|--------------------------------------------------------------|
|[doorway-agi](https://pypi.org/project/doorway-agi/)  |This package. AGI reasoning engine. Open source.              |
|[vantagepoint](https://pypi.org/project/vantagepoint/)|Structured thinking methodology. Open source.                 |
|doorway-asi                                           |Persistence + wisdom emergence. Private. Commercial extension.|
|doorway-platform                                      |Consumer product at doorwayagi.com. Private.                  |

The architecture is open. The advantage built on top is not.

### Library Growth

The shape library is not static. It grows through confirmed use.

When a bridge is confirmed, the geometry of the unknown domain is
extracted — not as a copy of the source shape, but as a genuinely
new geometric pattern with its own structure, elements, and
predictions. The new shape enters the shared library permanently.

The next session — by any user — matches against a richer library.
Gap scores shrink. Bridges get more precise. The system gets
smarter from collective use. More users, more confirmations,
richer library, better reasoning for everyone.

## Related Packages

- [xycore](https://pypi.org/project/xycore/) — Cryptographic chain primitive
- [pruv](https://pypi.org/project/pruv/) — Digital verification infrastructure
- [vantagepoint](https://pypi.org/project/vantagepoint/) — Structured thinking methodology

## License

Apache License 2.0 — see <LICENSE> for details.

© 2026 Doorway · [doorwayagi.com](https://doorwayagi.com)

Created by Luke H
