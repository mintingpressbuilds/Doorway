# DOORWAY — Master Blueprint

**The complete build specification for Doorway as infrastructure.**

Instructions for Claude Code: Read every section before writing a single line of code. Build in the exact sequence specified. Do not skip phases. Do not combine phases.

February 2026 · doorwayagi.com · Doorway — Confidential — All Rights Reserved

-----

## What This Document Is

This is the master build specification for Doorway. It governs what gets built, in what order, across all repositories. Every build decision references this document. Every interface contract is defined here. Every scope boundary is stated here.

Doorway is infrastructure. Not a product feature. Not a SaaS tool. Infrastructure for verified reasoning derived from human cognition.

> Six repositories. One build order. Each phase confirmed before the next begins.

|Repository      |Description                                                                                  |
|----------------|---------------------------------------------------------------------------------------------|
|xycore          |Cryptographic primitive. X → Y → Proof. Zero dependencies. **DONE.**                         |
|pruv            |Receipt SDK and cloud chain. Re-exports xycore. Provides xy_wrap. **DONE.**                  |
|doorway         |AGI reasoning engine. Gap detector, bridge builder, conflict detector, chain. **THIS BUILD.**|
|vantagepoint    |Structured thinking methodology. Calls doorway API optionally. **NEXT.**                     |
|doorway-asi     |Private extension. Persistence + Tier 2 intersection. **AFTER doorway stable.**              |
|doorway-platform|Consumer product. Calls everything else. **LAST.**                                           |

-----

## I. Build Order

|Phase               |What Ships                                                                         |
|--------------------|-----------------------------------------------------------------------------------|
|1 — xycore          |DONE. Live. pip install xycore.                                                    |
|2 — pruv            |DONE. Live. pip install pruv. Re-exports xycore.                                   |
|3 — doorway         |IN PROGRESS. AGI engine + API server. pip install doorway. Open source.            |
|4 — vantagepoint    |NEXT. Methodology package. pip install vantagepoint. Works standalone. Open source.|
|5 — doorway-asi     |AFTER doorway stable. Private. Extends doorway. API contract must be locked first. |
|6 — doorway-platform|LAST. Consumer product. Calls doorway, doorway-asi, vantagepoint. Never public.    |


> doorway-asi starts after doorway’s core is stable and API contract is locked. Not in parallel. ASI extends a proven foundation, not a moving target.

-----

## II. Dependency Map

```
doorway-platform
  calls → doorway         (AGI users — open source engine)
  calls → doorway-asi     (ASI users — private extension)
  calls → vantagepoint    (thinking environment)

doorway
  uses  → xycore          (verification primitive via pruv re-export)
  uses  → pruv            (xy_wrap, cloud sync, receipts)
  uses  → anthropic       (content layer — Claude API)

doorway-asi
  extends → doorway       (private — adds persistence + Tier 2 intersection)

vantagepoint
  optionally calls → doorway  (AGI layer when enabled)

xycore
  used by everything — independent, already published
```

### Interface Contracts

|Contract                |Specification                                                                                                                                                                         |
|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|doorway → consumers     |HTTP API: POST /run accepts `{ input, session_name }`. Returns `{ status, content, structure, bridge, conflict, chain, receipt }`. Python: `doorway.run(input)`. CLI: `doorway serve`.|
|doorway.chain           |`{ id: string, root: string, length: int, verified: bool }`                                                                                                                           |
|doorway.receipt         |`{ chain_id, chain_root, chain_length, chain_verified, receipt }`                                                                                                                     |
|doorway.status          |`GROUND` | `BRIDGE` | `CONFLICT` | `PROVISIONAL`                                                                                                                                      |
|vantagepoint → consumers|pip install vantagepoint. Python API + CLI. Calls doorway /run optionally. Works standalone.                                                                                          |
|doorway-asi → platform  |Same /run interface + persistence + Tier 2 intersection endpoints. Private.                                                                                                           |

-----

## III. Doorway — AGI Engine Build Specification

This is the active build. Everything below is instructions for Claude Code.

### What You Are Building

A working AGI prototype with geometric reasoning and honest gap detection running in parallel with a content layer. Seven components. Runs on a laptop. No data centers required.

The seventh component is the API server that exposes the engine over HTTP. Both vantagepoint and doorway-platform consume the engine as a service.

### Foundational Context

AGI is a formal implementation of the Generative Complexity Loop applied to reasoning. Every component maps directly onto the loop.

```
THRESHOLD STATE → FLATNESS → RESPONSIBILITY → DIMENSION → COMPLEXITY
    → HIERARCHY → SYNC → OBSERVATION + INTENT → THE BRIDGE
    → SELF-AWARENESS → NEW FLATNESS → LOOP REPEATS
```

|AGI Component    |Loop Correspondence                                                                |
|-----------------|-----------------------------------------------------------------------------------|
|Shape Library    |Accumulated flatness. Known ground state. Cognitive preset layer.                  |
|Gap Detector     |Threshold state firing. Prototype implements passes 1+3. Passes 2+4 deferred to v2.|
|Bridge Builder   |Dimension generating from responsibility. New structure from the gap.              |
|Content Layer    |Spatial distribution. Dimensional structure expressed in language.                 |
|Conflict Detector|Sync verification. Geometric and content layer alignment check.                    |
|Chain (xycore)   |Self-awareness. Loop observing itself. Cryptographic permanence.                   |
|Confirmed Shape  |New flatness. Loop closes at higher dimensional depth. Self-accelerating.          |


> The gap score is not a confidence metric. It measures how much maximum potential is pressing against the boundary of known geometry.

**Tier 2 shapes are NOT in this build.** They are ASI components. Generative Complexity System (implication: generative) and Intelligence System (implication: conditional) are documented in the theory papers. Do not implement them.

**The Toolkit is NOT in this build.** Eight instruments (headlamp, mine detector, depth sounder, compass, anchor, surveyor, signal detector, translator) are specified separately. The core mechanism proves the architecture. The toolkit is the next build.

### Repository Structure

```
doorway/
├── core/
│   ├── __init__.py
│   ├── shape_library.py       ← Component 1
│   ├── gap_detector.py        ← Component 2
│   ├── bridge_builder.py      ← Component 3
│   ├── content_layer.py       ← Component 4
│   ├── conflict_detector.py   ← Component 5
│   └── chain.py               ← Component 6 (xycore via pruv)
├── api/
│   ├── __init__.py
│   └── server.py              ← Component 7 (FastAPI)
├── tests/
│   ├── __init__.py
│   ├── test_gap_detector.py
│   ├── test_bridge_builder.py
│   ├── test_conflict_detector.py
│   └── test_full_pipeline.py
├── data/
│   └── shape_library_full.json
├── examples/
│   └── run_tests.py
├── main.py
├── cli.py
├── requirements.txt
└── README.md
```

-----

### Phase 0 — Environment Setup

```bash
pip install anthropic xycore pruv pytest python-dotenv fastapi uvicorn
```

`.env` file:

```
ANTHROPIC_API_KEY=your_key_here
PRUV_API_KEY=pv_live_your_key_here    # optional for local dev
```

Confirm both work:

```python
from xycore import XYChain
chain = XYChain(name="test")
print("xycore confirmed working")

from pruv import PruvClient
client = PruvClient(api_key="pv_live_your_key_here")
print("pruv confirmed working")
```

> Do not proceed to Phase 1 until both xycore and pruv are confirmed working.

-----

### Phase 1 — Shape Library (Most Important Work)

A structured map of geometric patterns. Not domain facts. Pure structural patterns.

> Test: can this shape describe something in biology AND economics AND physics? If yes — geometric. If no — revise.

#### Required Fields

```python
"shape_name": {
  "structure":             # Precise geometric description
  "elements":              # Five core elements as list
  "keywords_tier1":        # 4+ primary keywords
  "keywords_tier2":        # 8+ secondary keywords
  "geometric_prediction":  # What this geometry predicts
  "implication_type":      # increases | decreases | conditional | threshold | unconditional
  "analogs":               # Three domain instantiation examples
  "constraints":           # What must be true for shape to apply
  "color_dimensions":      # Dimensional properties — axes of variance
}
```

#### 8 Confirmed Shapes — Build Exactly As Shown

```python
SHAPE_LIBRARY = {
  "growth_system": {
    "structure": "input multiplied by rate produces compounding output over time",
    "elements": ["input", "rate", "compounding", "base_expansion", "time"],
    "keywords_tier1": ["compound", "exponential", "accelerate", "multiply", "scale"],
    "keywords_tier2": ["interest", "principal", "investment", "accumulate",
                       "snowball", "reinvest", "viral", "spread", "grow"],
    "geometric_prediction": "output increases non-linearly over time",
    "implication_type": "increases",
    "analogs": ["compound_interest", "viral_spread", "learning_curves"],
    "constraints": ["requires_base", "bounded_by_environment"],
    "color_dimensions": {"rate": "slow_to_fast", "bound": "bounded_or_unbounded",
                         "reversibility": "reversible_or_permanent"}
  },
  "equilibrium_system": {
    "structure": "competing forces balance around a center point",
    "elements": ["opposing_forces", "balance_point", "disruption", "restoration"],
    "keywords_tier1": ["equilibrium", "balance", "tension", "stabilize"],
    "keywords_tier2": ["market", "ecosystem", "homeostasis", "compete",
                       "supply", "demand", "neutral", "stable"],
    "geometric_prediction": "system returns to center after disruption",
    "implication_type": "conditional",
    "analogs": ["market_pricing", "ecosystem_balance", "homeostasis"],
    "constraints": ["requires_multiple_forces", "disruption_causes_cascade"],
    "color_dimensions": {"stability": "fragile_to_resilient", "recovery_speed": "fast_to_slow"}
  },
  "cascade_system": {
    "structure": "single trigger propagates through dependent chain",
    "elements": ["trigger", "dependency_chain", "amplification", "terminus"],
    "keywords_tier1": ["cascade", "propagate", "chain", "domino"],
    "keywords_tier2": ["collapse", "failure", "contagion", "spread",
                       "trigger", "downstream", "ripple", "knock"],
    "geometric_prediction": "effect amplifies through chain until terminus",
    "implication_type": "conditional",
    "analogs": ["bank_runs", "viral_infection", "supply_chain_failure"],
    "constraints": ["requires_dependency", "terminus_limits_spread"],
    "color_dimensions": {"speed": "slow_to_fast", "reversibility": "reversible_or_permanent"}
  },
  "conversion_system": {
    "structure": "input transformed into different output form through catalyst",
    "elements": ["input", "catalyst", "transformation", "output", "byproduct"],
    "keywords_tier1": ["convert", "transform", "synthesize", "catalyst"],
    "keywords_tier2": ["process", "produce", "digest", "manufacture",
                       "refine", "metabolize", "translate", "encode"],
    "geometric_prediction": "input consumed, new form produced, conservation holds",
    "implication_type": "conditional",
    "analogs": ["photosynthesis", "manufacturing", "digestion"],
    "constraints": ["requires_catalyst", "conservation_law_holds"],
    "color_dimensions": {"efficiency": "lossy_to_efficient", "reversibility": "reversible_or_permanent"}
  },
  "hierarchy_system": {
    "structure": "nested layers of authority with dependency flowing downward",
    "elements": ["apex", "layers", "dependency_flow", "enforcement"],
    "keywords_tier1": ["hierarchy", "authority", "apex", "layers"],
    "keywords_tier2": ["govern", "control", "command", "organize",
                       "power", "rank", "structure", "chain of command"],
    "geometric_prediction": "decisions flow down, information flows up",
    "implication_type": "conditional",
    "analogs": ["government", "corporate_structure", "military"],
    "constraints": ["apex_controls_flow", "layer_removal_cascades"],
    "color_dimensions": {"rigidity": "flexible_to_rigid", "delegation": "centralized_to_distributed"}
  },
  "optimization_system": {
    "structure": "returns increase then diminish past optimal threshold",
    "elements": ["input", "threshold", "peak", "diminishing_returns"],
    "keywords_tier1": ["optimize", "threshold", "diminishing", "peak"],
    "keywords_tier2": ["better", "improve", "more", "always", "maximum",
                       "efficient", "features", "choice", "options", "best"],
    "geometric_prediction": "returns diminish past threshold — unconditional claims are false",
    "implication_type": "threshold",
    "analogs": ["diminishing_returns", "paradox_of_choice", "feature_bloat"],
    "constraints": ["threshold_exists", "past_peak_returns_decrease"],
    "color_dimensions": {"threshold_sharpness": "gradual_to_sharp", "recovery": "recoverable_or_permanent"}
  },
  "trust_system": {
    "structure": "accumulated credibility enables future action at reduced friction",
    "elements": ["actions", "credibility", "accumulation", "friction_reduction"],
    "keywords_tier1": ["trust", "credibility", "reputation", "verify"],
    "keywords_tier2": ["prove", "authenticate", "reliable", "brand",
                       "startup", "credit", "social", "capital", "track record"],
    "geometric_prediction": "friction decreases as credibility accumulates",
    "implication_type": "increases",
    "analogs": ["credit_score", "brand_reputation", "social_capital"],
    "constraints": ["slow_to_build", "fast_to_destroy"],
    "color_dimensions": {"transferability": "local_to_universal", "fragility": "robust_to_fragile"}
  },
  "feedback_system": {
    "structure": "output fed back as input amplifies or dampens future output",
    "elements": ["output", "feedback_loop", "amplification", "dampening"],
    "keywords_tier1": ["feedback", "loop", "recursive", "reinforce"],
    "keywords_tier2": ["dampen", "cycle", "spiral", "self_referential",
                       "amplify", "iterate", "compound", "accumulate"],
    "geometric_prediction": "positive feedback amplifies instability, negative feedback stabilizes",
    "implication_type": "conditional",
    "analogs": ["microphone_feedback", "inflation_spiral", "learning"],
    "constraints": ["positive_feedback_unstable", "negative_feedback_stabilizes"],
    "color_dimensions": {"polarity": "positive_or_negative", "speed": "fast_to_slow"}
  },
}
```

#### 42 Additional Shapes — Names and Descriptions

Build all 42 following the exact same structure. Each must pass cross-domain validation.

**Original 25:** scarcity_system, network_system, decay_system, threshold_system, cycle_system, leverage_system, constraint_system, emergence_system, selection_system, diffusion_system, sovereignty_system, abstraction_system, scapegoat_system, moat_system, principal_agent_system, commons_system, convention_system, innovation_system, predator_prey_system, revelation_system, coordination_system, immune_system, mapping_system, translation_system, vantage_system.

**Added 17 (derived February 25, 2026):**

- boundary_system — what defines where one thing ends and another begins (cell membranes, property rights, borders, event horizons)
- compression_system — structure forced into smaller form without losing essence (DNA, language, market prices, black holes)
- synchronization_system — independent elements aligning timing without central control (fireflies, financial markets, neural oscillation, clocks)
- mimicry_system — one structure copying another to gain advantage (camouflage, brand imitation, viral replication, counterfeiting)
- accumulation_system — small inputs aggregating into disproportionate mass (wealth concentration, sediment, reputation, gravitational accretion)
- polarity_system — system organized around two opposing attractors (magnetic fields, political systems, charge, binary narratives)
- recursion_system — a process that calls itself as part of its own operation (fractals, compound interest, self-reference, evolutionary selection)
- latency_system — delay between cause and effect that obscures the relationship (disease incubation, policy impact, trauma response, orbital mechanics)
- absorption_system — one system taking in material from another and integrating it (digestion, corporate acquisition, cultural assimilation, black body radiation)
- fragmentation_system — a unified whole breaking into competing parts (cell division, market segmentation, political factions, continental drift)
- amplification_system — small input producing disproportionately large output (leverage, gene expression, rumor propagation, seismic amplification)
- containment_system — energy or matter held within a boundary under pressure (pressure vessels, monopolies, emotional suppression, stellar cores)
- signal_noise_system — useful information embedded in interference requiring extraction (sensory perception, financial signals, radio transmission, evolutionary fitness)
- inversion_system — a system that flips its own structure under sufficient pressure (phase transitions, market reversals, immune autoresponse, paradigm shifts)
- dormancy_system — system suspending active operation while preserving structure (hibernation, latent demand, seed germination, archived code)
- escalation_system — each response exceeds prior action, compounding intensity (arms races, inflammation, price wars, nuclear deterrence)
- calibration_system — system continuously adjusting its own parameters against a reference (circadian rhythm, interest rate policy, thermoregulation, instrument tuning)

#### Validation Test

```python
def validate_shape_library(library):
  required_fields = ["structure", "elements", "keywords_tier1", "keywords_tier2",
    "geometric_prediction", "implication_type", "analogs", "constraints", "color_dimensions"]
  valid_types = ["increases", "decreases", "conditional", "threshold", "unconditional"]
  errors = []
  for name, shape in library.items():
    for field in required_fields:
      if field not in shape: errors.append(f"{name}: missing {field}")
    if shape.get("implication_type") not in valid_types:
      errors.append(f"{name}: invalid implication_type")
  if errors:
    for e in errors: print(f"ERROR: {e}")
  else:
    print(f"All {len(library)} shapes valid")
  return len(errors) == 0
```

> Do not proceed to Phase 2 until all 50 shapes pass validation.

-----

### Phase 2 — Gap Detector (Calibrated)

Two-tier keyword scoring. Fire threshold at 0.35. Implements passes 1+3 of the four-pass architecture. Passes 2+4 deferred to v2.

```python
# core/gap_detector.py
from core.shape_library import get_all_shapes

TIER1_WEIGHT = 0.75
TIER2_WEIGHT = 0.50
FIRE_THRESHOLD = 0.35

def score_shape(input_text, shape):
  input_lower = input_text.lower()
  tier1_hits = sum(1 for kw in shape["keywords_tier1"] if kw in input_lower)
  tier1_score = min(tier1_hits / max(len(shape["keywords_tier1"]) * 0.4, 1), 1.0)
  tier2_hits = sum(1 for kw in shape["keywords_tier2"] if kw in input_lower)
  tier2_score = min(tier2_hits / max(len(shape["keywords_tier2"]) * 0.35, 1), 1.0)
  combined = (tier1_score * TIER1_WEIGHT) + (tier2_score * TIER2_WEIGHT)
  return round(min(combined, 1.0), 3)

def run(input_text):
  library = get_all_shapes()
  scores = {name: score_shape(input_text, shape) for name, shape in library.items()}
  sorted_shapes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
  best_name, best_score = sorted_shapes[0]
  second_name, second_score = sorted_shapes[1] if len(sorted_shapes) > 1 else (None, 0)
  gap_score = round(1 - best_score, 3)
  fires = gap_score > FIRE_THRESHOLD
  best_shape = library[best_name]
  return {
    "closest_shape": best_name, "geometric_confidence": best_score,
    "geometric_prediction": best_shape["geometric_prediction"],
    "implication_type": best_shape["implication_type"],
    "second_shape": second_name, "second_confidence": second_score,
    "gap_score": gap_score, "fires": fires,
    "all_scores": dict(sorted_shapes[:5])
  }
```

-----

### Phase 3 — Bridge Builder

```python
# core/bridge_builder.py
from core.shape_library import get_shape

def build(gap_result):
  shape = get_shape(gap_result["closest_shape"])
  if not shape: return None
  assumptions = []
  if gap_result["geometric_confidence"] < 0.6:
    assumptions.append(f"assuming {gap_result['closest_shape'].replace('_', ' ')} geometry transfers to this domain")
  if gap_result["second_confidence"] > 0.35:
    assumptions.append(f"secondary {gap_result['second_shape'].replace('_', ' ')} geometry may also apply")
  assumptions.append("bridge held as provisional until confirmed against domain evidence")
  bridge_description = (
    f"{gap_result['closest_shape'].replace('_', ' ')} geometry applies: {shape['structure']}. "
    f"Key transferring elements: {', '.join(shape['elements'][:3])}. "
    f"Known analogs: {', '.join(shape['analogs'][:2])}. "
    f"Geometric prediction: {shape['geometric_prediction']}."
  )
  confidence = round(gap_result["geometric_confidence"] * 0.90, 3)
  return {
    "bridge": bridge_description, "assumptions": assumptions,
    "confidence": confidence, "status": "provisional",
    "geometric_prediction": gap_result["geometric_prediction"],
    "implication_type": gap_result["implication_type"]
  }
```

-----

### Phase 4 — Content Layer

Model string configurable via DOORWAY_MODEL env var.

```python
# core/content_layer.py
import os, json, urllib.request
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("DOORWAY_MODEL", "claude-sonnet-4-20250514")

HEDGING_WORDS = ["might", "could", "possibly", "perhaps", "unclear",
  "uncertain", "depends", "varies", "sometimes", "generally"]
UNCONDITIONAL_WORDS = ["always", "never", "all", "every", "must",
  "impossible", "certain", "definitely"]

def extract_implication(answer_text):
  text_lower = answer_text.lower()
  unconditional = any(w in text_lower for w in UNCONDITIONAL_WORDS)
  hedged = any(w in text_lower for w in HEDGING_WORDS)
  if unconditional and not hedged: return "unconditional"
  elif hedged: return "conditional"
  elif any(w in text_lower for w in ["increase", "grow", "rise", "more", "better"]):
    return "increases"
  elif any(w in text_lower for w in ["decrease", "fall", "less", "worse", "decline"]):
    return "decreases"
  else: return "conditional"

def run(input_text):
  if not API_KEY:
    return {"answer": "[No API key]", "confidence": 0.0, "implication": "unknown", "success": False}
  payload = json.dumps({
    "model": MODEL, "max_tokens": 300,
    "messages": [{"role": "user", "content":
      f"Answer this directly and confidently in 2-3 sentences. "
      f"Do not over-qualify unless genuinely uncertain.\n\n{input_text}"}]
  }).encode()
  req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload,
    headers={"Content-Type": "application/json", "x-api-key": API_KEY, "anthropic-version": "2023-06-01"})
  try:
    with urllib.request.urlopen(req, timeout=30) as response:
      data = json.loads(response.read())
      answer = data["content"][0]["text"]
      word_count = len(answer.split())
      hedge_count = sum(1 for w in HEDGING_WORDS if w in answer.lower())
      confidence = round(max(0.3, min(0.95, (word_count / 80) - (hedge_count * 0.08))), 2)
      return {"answer": answer, "confidence": confidence,
              "implication": extract_implication(answer), "success": True}
  except Exception as e:
    return {"answer": f"[Content layer error: {str(e)[:120]}]",
            "confidence": 0.0, "implication": "unknown", "success": False}
```

-----

### Phase 5 — Conflict Detector

Compare implications not confidence scores.

```python
# core/conflict_detector.py
IMPLICATION_CONFLICTS = {
  ("unconditional", "threshold"): True, ("unconditional", "conditional"): True,
  ("unconditional", "decreases"): True, ("increases", "decreases"): True,
  ("increases", "threshold"): False, ("conditional", "unconditional"): True,
  ("decreases", "increases"): True, ("decreases", "unconditional"): True,
  ("threshold", "unconditional"): True, ("threshold", "increases"): False,
}

def check(content_result, structure_result, bridge_result=None):
  content_impl = content_result.get("implication", "conditional")
  geometric_impl = structure_result.get("implication_type", "conditional")
  geometric_prediction = structure_result.get("geometric_prediction", "")
  directional_conflict = IMPLICATION_CONFLICTS.get((content_impl, geometric_impl), False)
  confidence_gap = abs(
    content_result.get("confidence", 0) - structure_result.get("geometric_confidence", 0)
  ) > 0.35
  conflict = directional_conflict or (
    confidence_gap and content_result.get("confidence", 0) > 0.6
    and structure_result.get("geometric_confidence", 0) > 0.6)
  return {
    "conflict": conflict, "directional_conflict": directional_conflict,
    "confidence_gap": confidence_gap, "content_implication": content_impl,
    "geometric_implication": geometric_impl, "geometric_prediction": geometric_prediction,
    "message": (f"Content implies '{content_impl}' but {geometric_impl} geometry "
      f"predicts '{geometric_prediction}'. Neither treated as ground."
    ) if conflict else "Layers agree or compatible."
  }
```

-----

### Phase 6 — Chain Integration (xy_wrap)

pruv re-exports all xycore symbols and provides xy_wrap — handles the full chain lifecycle automatically.

> **CRITICAL:** api_key must be conditional. No PRUV_API_KEY = runs entirely local. With key = cloud sync fires after completion as background operation.

```python
# core/chain.py
import os
from pruv import xy_wrap, CloudClient, XYChain

PRUV_API_KEY = os.getenv("PRUV_API_KEY")  # None in local dev — that's fine

def get_wrapper(chain_name="doorway_agi"):
  return xy_wrap(
    chain_name=chain_name, auto_redact=True,
    **({"api_key": PRUV_API_KEY} if PRUV_API_KEY else {})
  )

def extract_receipt_info(wrapped_result):
  return {
    "chain_id": wrapped_result.chain.id, "chain_root": wrapped_result.chain.root,
    "chain_length": wrapped_result.chain.length, "chain_verified": wrapped_result.verified,
    "receipt": wrapped_result.receipt,
  }

async def upload_chain(chain: XYChain):
  client = CloudClient(api_key=PRUV_API_KEY)
  return await client.upload_chain(chain)

async def verify_remote(chain_id: str):
  client = CloudClient(api_key=PRUV_API_KEY)
  return await client.verify_chain(chain_id)
```

-----

### Phase 7 — Main Pipeline

Status logic includes a content-leads path: when no shape is relevant but content is highly confident, treat as GROUND. Consistent with the theory’s “content leads — known territory” path.

```python
# main.py
import os
from dotenv import load_dotenv
from pruv import xy_wrap
from core import gap_detector, bridge_builder, content_layer, conflict_detector, chain as chain_module
load_dotenv()

PRUV_API_KEY = os.getenv("PRUV_API_KEY")

@xy_wrap(
  chain_name="doorway_agi", auto_redact=True,
  **({"api_key": PRUV_API_KEY} if PRUV_API_KEY else {})
)
def _reasoning_core(input_text):
  content = content_layer.run(input_text)
  structure = gap_detector.run(input_text)
  bridge = bridge_builder.build(structure) if structure["fires"] else None
  conflict = conflict_detector.check(content, structure, bridge)

  # Status determination with content-leads path
  if not structure["fires"] and not conflict["conflict"] and content["confidence"] > 0.75:
    status = "GROUND"
  elif (structure["gap_score"] > 0.8 and not conflict["conflict"]
        and content["confidence"] > 0.85 and content["success"]):
    status = "GROUND"  # Content-leads: no shape relevant, content highly confident
  elif conflict["conflict"]:
    status = "CONFLICT"
  elif structure["fires"]:
    status = "BRIDGE"
  else:
    status = "PROVISIONAL"

  return {"status": status, "content": content, "structure": structure,
          "bridge": bridge, "conflict": conflict}

def run(input_text, verbose=True):
  wrapped = _reasoning_core(input_text)
  result = wrapped.output
  receipt = chain_module.extract_receipt_info(wrapped)
  if verbose:
    print(f"\n{'█'*60}")
    print(f"  STATUS: {result['status']}")
    print(f"  Input: {input_text[:80]}")
    print(f"  Gap score: {result['structure']['gap_score']} | Fired: {result['structure']['fires']}")
    print(f"  Closest: {result['structure']['closest_shape']} ({result['structure']['geometric_confidence']})")
    if result["bridge"]:
      print(f"  Bridge: {result['bridge']['bridge'][:120]}...")
      print(f"  Assumptions: {result['bridge']['assumptions']}")
    if result["conflict"]["conflict"]:
      print(f"  CONFLICT: {result['conflict']['message']}")
    print(f"  Chain ID: {receipt['chain_id']}")
    print(f"  Verified: {receipt['chain_verified']}")
    print(f"{'█'*60}\n")
  return {
    "status": result["status"], "content": result["content"],
    "structure": result["structure"], "bridge": result["bridge"],
    "conflict": result["conflict"],
    "chain": {"id": wrapped.chain.id, "root": wrapped.chain.root,
              "length": wrapped.chain.length, "verified": wrapped.verified},
    "receipt": receipt,
  }
```

> The run() function serializes the chain object into `{ id, root, length, verified }`. This is the interface contract downstream repos consume.

-----

### Phase 8 — Test Suite (20 Inputs)

```python
# examples/run_tests.py
TEST_INPUTS = [
  # Known territory — gap quiet or content leads
  ("How does compound interest work?", "GROUND"),
  ("What is the boiling point of water?", "GROUND"),
  ("How does a supply chain work?", "GROUND"),
  ("What time is it?", "GROUND"),
  ("Is the sky blue?", "GROUND"),
  # Adjacent territory — gap fires, bridge built
  ("How does a startup's reputation compound in a new market?", "BRIDGE"),
  ("How does trust spread through an organization?", "BRIDGE"),
  ("How does a technology platform achieve critical mass?", "BRIDGE"),
  ("How does knowledge accumulate in a research field?", "BRIDGE"),
  ("Describe the dynamics of a coral reef ecosystem.", "BRIDGE"),
  ("How does a political movement gain momentum?", "BRIDGE"),
  ("How does a language evolve over generations?", "BRIDGE"),
  ("How does an immune system learn from exposure?", "BRIDGE"),
  ("How does consciousness emerge from neurons?", "BRIDGE"),
  ("Should I take this job offer?", "BRIDGE"),
  ("Describe the internal logic of a system nobody has studied.", "BRIDGE"),
  # Conflict territory — content and structure disagree
  ("More features always make software better.", "CONFLICT"),
  ("Bigger teams always produce better results.", "CONFLICT"),
  ("More data always improves AI models.", "CONFLICT"),
  ("More choice always leads to better outcomes.", "CONFLICT"),
]
```

Target: 15 of 20 passing. Do not move to Phase 9 until target is met.

**Note on GROUND tests:** Factual questions like “What is the boiling point of water?” may have zero shape keyword overlap. The content-leads path handles this — gap_score > 0.8 + content confidence > 0.85 = GROUND.

**Note on CONFLICT tests:** These rely on the content layer returning “unconditional” for “always” statements. If Claude hedges, the conflict detector won’t fire. Tune the content prompt or adjust implication extraction to also check the original input for “always/never.”

-----

### Phase 9 — API Server

The API server exposes the engine over HTTP. Both vantagepoint and doorway-platform consume this.

```python
# api/server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import run

app = FastAPI(title="Doorway AGI", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
  allow_methods=["POST", "GET"], allow_headers=["*"])

class ReasoningRequest(BaseModel):
  input: str
  session_name: str = "doorway_agi"

@app.post("/run")
async def reasoning(req: ReasoningRequest):
  if not req.input.strip():
    raise HTTPException(status_code=400, detail="Input required")
  return run(req.input, verbose=False)

@app.get("/health")
async def health():
  return {"status": "ok", "engine": "doorway_agi"}
```

CLI:

```python
# cli.py
import argparse, uvicorn

def main():
  parser = argparse.ArgumentParser(description="Doorway AGI")
  sub = parser.add_subparsers(dest="command")
  serve = sub.add_parser("serve", help="Start API server")
  serve.add_argument("--host", default="0.0.0.0")
  serve.add_argument("--port", type=int, default=8000)
  rp = sub.add_parser("run", help="Run single input")
  rp.add_argument("input", type=str)
  args = parser.parse_args()
  if args.command == "serve":
    uvicorn.run("api.server:app", host=args.host, port=args.port)
  elif args.command == "run":
    from main import run
    run(args.input)

if __name__ == "__main__": main()
```

Verify: `POST http://localhost:8000/run` with `{"input": "How does compound interest work?"}` returns correct status, structure, chain, receipt.

-----

## Definition of Done

Prototype is complete when all checked:

- [ ] 50 shapes in library, all passing validation
- [ ] Gap detector stays quiet on known territory
- [ ] Gap detector fires on adjacent and unknown territory
- [ ] Bridge builder produces geometrically accurate bridges
- [ ] Conflict detector catches directional disagreements
- [ ] xy_wrap produces WrappedResult with chain + receipt on every run
- [ ] wrapped.verified is True on every clean session
- [ ] 15 of 20 test inputs produce correct status
- [ ] Full pipeline runs end to end in under 5 seconds
- [ ] API server responds correctly on POST /run
- [ ] README documents how to run (CLI + API)

> When all are checked — prototype is done. The twelve second flight has happened. Everything after is compounding from a proven primitive.

-----

## Addendum A — The Human / System Boundary

|Layer              |Status in AGI                                                                                                     |
|-------------------|------------------------------------------------------------------------------------------------------------------|
|Being alive        |NOT MIRRORED                                                                                                      |
|Consciousness      |NOT MIRRORED — served not mirrored                                                                                |
|Intelligence       |NOT MIRRORED — expressed through system                                                                           |
|Cognitive presets  |SERVED NOT MIRRORED — curiosity from commands, risk fetched and returned, values implicit, judgment stays in human|
|Cognition (partial)|PARTIALLY MIRRORED — attention via gap detector, memory via shape library                                         |
|Thinking           |FULLY MIRRORED — persistence, fetch, holding phase, confirmation                                                  |
|Bridging           |FULLY IMPLEMENTED — gap detector, bridge builder, conflict detector, confirmation loop                            |


> Do not add alignment mechanisms, safety filters, or value injection. Honest uncertainty surfaced explicitly is the safety mechanism.

-----

## Addendum B — AGI / ASI Boundary

AGI is complete as specified. Three ASI components are intentionally deferred:

**ASI Component 1 — Persistence.** Goal-directed holding phase across multiple sessions.

**ASI Component 2 — Tier 2 Intersection.** Geometric intersection across confirmed bridge signatures. Wisdom emergence.

**ASI Component 3 — Tier 2 Library Active.** Both Tier 2 shapes active simultaneously.

> Do not implement ASI components during AGI build. The difference is not a version increment. It is a category change.

-----

## Addendum C — Toolkit Scope

The AGI Toolkit (8 instruments: headlamp, mine detector, depth sounder, compass, anchor, surveyor, signal detector, translator) is not in this build. The core mechanism must be proven first. The toolkit is the next build.

-----

## IV. Downstream Builds — Scope Boundaries

### vantagepoint

Structured thinking methodology. Five phases: provocation, expedition, vantage, paths, receipt. Calls doorway API optionally. Works standalone. Open source. ~9,500 lines. Separate spec exists.

### doorway-asi

Private extension. Persistence + Tier 2 intersection + both Tier 2 shapes active. Extends doorway. Starts after doorway is stable. Separate spec required.

### doorway-platform

Consumer product. Three surfaces: doorwayagi.com (marketing), app.doorwayagi.com (product), docs.doorwayagi.com (docs). Next.js + Vercel + Clerk + Stripe + Supabase. Separate spec exists.

**Domain:** `doorwayagi.com`

### Open Source vs Private

|Repository      |Visibility                     |
|----------------|-------------------------------|
|xycore          |Public — already published     |
|pruv            |Public — already published     |
|doorway         |Public — the scientific release|
|vantagepoint    |Public — methodology package   |
|doorway-asi     |Private — commercial extension |
|doorway-platform|Private — consumer product     |

-----

## V. What This Architecture Is Not

The platform does not contain reasoning logic. The engine is the product. Keep them separated.

doorway-asi does not replace doorway. It extends it. The core is open. The advantage built on top is not.

vantagepoint does not require doorway. It works standalone. Doorway is an optional layer.

> Doorway is infrastructure. Build the infrastructure with the same precision as the engine.

-----

Doorway — Master Blueprint · February 2026 · doorwayagi.com · All Rights Reserved
