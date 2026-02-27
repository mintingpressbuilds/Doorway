# core/shape_library.py — Component 1
# 50 geometric shapes. Pure structural patterns.
# Test: can this shape describe something in biology AND economics AND physics?

SHAPE_LIBRARY = {

    # ══════════════════════════════════════════════════════════════════
    # 8 CONFIRMED SHAPES — copied exactly from BLUEPRINT
    # ══════════════════════════════════════════════════════════════════

    "growth_system": {
        "structure": "input multiplied by rate produces compounding output over time",
        "elements": ["input", "rate", "compounding", "base_expansion", "time"],
        "keywords_tier1": ["compound", "exponential", "accelerate", "multiply", "scale"],
        "keywords_tier2": ["interest", "principal", "investment", "accumulate",
                           "snowball", "reinvest", "viral", "spread", "grow"],
        "geometric_prediction": "output increases non-linearly over time",
        "implication_type": "increases",
        "analogs": ["compound_interest", "viral_spread", "nuclear_chain_reaction"],
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
        "analogs": ["market_pricing", "homeostasis", "thermal_equilibrium"],
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
        "analogs": ["bank_runs", "viral_infection", "nuclear_fission_chain"],
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
        "analogs": ["photosynthesis", "oil_refining", "nuclear_fusion"],
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
        "analogs": ["corporate_structure", "neural_hierarchy", "atomic_orbital_structure"],
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
        "analogs": ["diminishing_returns", "enzyme_saturation", "antenna_gain_limits"],
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
        "analogs": ["credit_score", "immune_memory", "superconductor_transition"],
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
        "analogs": ["microphone_feedback", "inflation_spiral", "hormonal_regulation"],
        "constraints": ["positive_feedback_unstable", "negative_feedback_stabilizes"],
        "color_dimensions": {"polarity": "positive_or_negative", "speed": "fast_to_slow"}
    },

    # ══════════════════════════════════════════════════════════════════
    # 25 ORIGINAL ADDITIONAL SHAPES
    # ══════════════════════════════════════════════════════════════════

    "scarcity_system": {
        "structure": "finite supply facing unlimited demand creates competition and value increase",
        "elements": ["supply", "demand", "competition", "value", "depletion"],
        "keywords_tier1": ["scarce", "limited", "finite", "rare"],
        "keywords_tier2": ["shortage", "deplete", "exhaust", "ration",
                           "hoard", "premium", "exclusive", "supply"],
        "geometric_prediction": "value increases as supply decreases relative to demand",
        "implication_type": "increases",
        "analogs": ["commodity_pricing", "oxygen_competition", "energy_conservation"],
        "constraints": ["requires_finite_supply", "demand_must_exist"],
        "color_dimensions": {"renewability": "renewable_to_exhaustible", "substitutability": "substitutable_to_unique"}
    },

    "network_system": {
        "structure": "interconnected nodes where value scales with number of connections",
        "elements": ["nodes", "connections", "network_effects", "density", "reach"],
        "keywords_tier1": ["network", "connect", "node", "link"],
        "keywords_tier2": ["hub", "cluster", "community", "platform",
                           "social", "web", "mesh", "interconnect"],
        "geometric_prediction": "value grows non-linearly as connections increase",
        "implication_type": "increases",
        "analogs": ["neural_networks", "trade_networks", "crystalline_structures"],
        "constraints": ["requires_multiple_nodes", "connection_cost_exists"],
        "color_dimensions": {"density": "sparse_to_dense", "centralization": "distributed_to_centralized"}
    },

    "decay_system": {
        "structure": "structure degrades over time following predictable rate",
        "elements": ["initial_state", "degradation_rate", "half_life", "residual", "time"],
        "keywords_tier1": ["decay", "degrade", "erode", "depreciate"],
        "keywords_tier2": ["rot", "fade", "wither", "decline",
                           "entropy", "dissolve", "rust", "wear"],
        "geometric_prediction": "value decreases exponentially toward zero or residual",
        "implication_type": "decreases",
        "analogs": ["radioactive_decay", "asset_depreciation", "cellular_apoptosis"],
        "constraints": ["irreversible_without_input", "rate_predictable"],
        "color_dimensions": {"rate": "slow_to_fast", "completeness": "partial_to_total"}
    },

    "threshold_system": {
        "structure": "accumulation produces no visible effect until critical value triggers sudden state change",
        "elements": ["accumulation", "critical_value", "trigger", "state_change", "irreversibility"],
        "keywords_tier1": ["threshold", "tipping", "critical", "trigger"],
        "keywords_tier2": ["break", "snap", "activate", "ignite",
                           "boil", "phase", "sudden", "cliff"],
        "geometric_prediction": "no effect until threshold, then rapid state change",
        "implication_type": "threshold",
        "analogs": ["phase_transitions", "market_crashes", "action_potentials"],
        "constraints": ["threshold_must_be_reached", "often_irreversible"],
        "color_dimensions": {"predictability": "predictable_to_chaotic", "reversibility": "reversible_or_permanent"}
    },

    "cycle_system": {
        "structure": "system moves through repeating sequence of states with predictable periodicity",
        "elements": ["phases", "periodicity", "amplitude", "reset", "driver"],
        "keywords_tier1": ["cycle", "oscillate", "periodic", "recur"],
        "keywords_tier2": ["wave", "rhythm", "season", "rotate",
                           "swing", "alternate", "boom", "bust"],
        "geometric_prediction": "current phase predicts next phase in sequence",
        "implication_type": "conditional",
        "analogs": ["business_cycles", "circadian_rhythms", "wave_oscillation"],
        "constraints": ["requires_restoring_force", "period_may_vary"],
        "color_dimensions": {"regularity": "regular_to_irregular", "amplitude": "stable_to_variable"}
    },

    "leverage_system": {
        "structure": "small input force amplified through structural advantage to produce large output",
        "elements": ["input_force", "fulcrum", "mechanical_advantage", "output_force", "risk"],
        "keywords_tier1": ["leverage", "amplify", "multiply", "magnify"],
        "keywords_tier2": ["lever", "fulcrum", "debt", "borrow",
                           "margin", "advantage", "power", "force"],
        "geometric_prediction": "output force exceeds input force proportional to leverage ratio",
        "implication_type": "increases",
        "analogs": ["financial_leverage", "enzyme_catalysis", "mechanical_levers"],
        "constraints": ["amplifies_both_gains_and_losses", "fulcrum_required"],
        "color_dimensions": {"ratio": "low_to_high", "risk": "safe_to_dangerous"}
    },

    "constraint_system": {
        "structure": "external boundary limits system behavior and channels output into specific forms",
        "elements": ["boundary", "limitation", "channeling", "adaptation", "pressure"],
        "keywords_tier1": ["constraint", "limit", "boundary", "restrict"],
        "keywords_tier2": ["cap", "ceiling", "floor", "bottleneck",
                           "regulate", "bind", "confine", "contain"],
        "geometric_prediction": "system adapts shape to fit within constraints",
        "implication_type": "conditional",
        "analogs": ["carrying_capacity", "budget_constraints", "conservation_laws"],
        "constraints": ["constraint_must_be_binding", "removal_changes_behavior"],
        "color_dimensions": {"rigidity": "soft_to_hard", "visibility": "visible_to_hidden"}
    },

    "emergence_system": {
        "structure": "simple local interactions between many agents produce complex global patterns not present in individuals",
        "elements": ["agents", "local_rules", "interaction", "global_pattern", "irreducibility"],
        "keywords_tier1": ["emerge", "arise", "self-organize", "spontaneous"],
        "keywords_tier2": ["bottom-up", "collective", "swarm", "flock",
                           "pattern", "complex", "order", "chaos"],
        "geometric_prediction": "macro patterns not predictable from micro rules alone",
        "implication_type": "conditional",
        "analogs": ["ant_colonies", "market_pricing", "crystal_formation"],
        "constraints": ["requires_many_agents", "rules_must_be_local"],
        "color_dimensions": {"predictability": "predictable_to_surprising", "scale": "local_to_global"}
    },

    "selection_system": {
        "structure": "variation subjected to environmental pressure retains fit variants and eliminates unfit",
        "elements": ["variation", "pressure", "fitness", "selection", "adaptation"],
        "keywords_tier1": ["select", "survive", "fit", "adapt"],
        "keywords_tier2": ["evolve", "compete", "eliminate", "breed",
                           "prune", "filter", "natural", "weed"],
        "geometric_prediction": "population shifts toward higher fitness over iterations",
        "implication_type": "conditional",
        "analogs": ["natural_selection", "market_competition", "resonance_selection"],
        "constraints": ["requires_variation", "requires_selection_pressure"],
        "color_dimensions": {"speed": "slow_to_fast", "direction": "convergent_to_divergent"}
    },

    "diffusion_system": {
        "structure": "substance or information spreads from high concentration to low until equilibrium",
        "elements": ["gradient", "medium", "rate", "equilibrium", "barrier"],
        "keywords_tier1": ["diffuse", "spread", "permeate", "distribute"],
        "keywords_tier2": ["osmosis", "seep", "migrate", "flow",
                           "penetrate", "saturate", "disperse", "radiate"],
        "geometric_prediction": "gradient decreases over time toward uniform distribution",
        "implication_type": "decreases",
        "analogs": ["heat_transfer", "technology_adoption", "osmosis"],
        "constraints": ["requires_gradient", "barrier_slows_spread"],
        "color_dimensions": {"speed": "slow_to_fast", "uniformity": "patchy_to_uniform"}
    },

    "sovereignty_system": {
        "structure": "entity exercises exclusive control over defined domain resisting external interference",
        "elements": ["domain", "authority", "boundary_enforcement", "autonomy", "challenge"],
        "keywords_tier1": ["sovereign", "autonomy", "control", "territory"],
        "keywords_tier2": ["independent", "govern", "domain", "jurisdiction",
                           "own", "rule", "defend", "border"],
        "geometric_prediction": "authority holds within boundary until successfully challenged",
        "implication_type": "conditional",
        "analogs": ["territorial_behavior", "property_rights", "quantum_exclusion"],
        "constraints": ["requires_enforcement_capacity", "boundary_must_be_defined"],
        "color_dimensions": {"strength": "weak_to_strong", "legitimacy": "contested_to_accepted"}
    },

    "abstraction_system": {
        "structure": "higher-level representation captures essential pattern while discarding implementation detail",
        "elements": ["concrete", "pattern", "abstraction", "loss", "utility"],
        "keywords_tier1": ["abstract", "generalize", "simplify", "model"],
        "keywords_tier2": ["represent", "symbol", "concept", "meta",
                           "reduce", "essence", "framework", "theory"],
        "geometric_prediction": "utility increases with abstraction level until detail loss becomes critical",
        "implication_type": "threshold",
        "analogs": ["genetic_code", "monetary_abstraction", "thermodynamic_averages"],
        "constraints": ["information_lost_in_abstraction", "wrong_abstraction_misleads"],
        "color_dimensions": {"level": "concrete_to_abstract", "fidelity": "lossy_to_faithful"}
    },

    "scapegoat_system": {
        "structure": "distributed tension concentrated onto single target providing temporary system relief",
        "elements": ["tension", "target", "displacement", "relief", "recurrence"],
        "keywords_tier1": ["scapegoat", "blame", "target", "displace"],
        "keywords_tier2": ["sacrifice", "deflect", "focus", "channel",
                           "punish", "expel", "project", "redirect"],
        "geometric_prediction": "tension temporarily relieved but root cause unaddressed leads to recurrence",
        "implication_type": "conditional",
        "analogs": ["autoimmune_response", "executive_scapegoating", "stress_fracture"],
        "constraints": ["relief_is_temporary", "root_cause_persists"],
        "color_dimensions": {"visibility": "hidden_to_obvious", "recurrence": "one_time_to_chronic"}
    },

    "moat_system": {
        "structure": "structural advantage creates barrier preventing competition from eroding position",
        "elements": ["advantage", "barrier", "position", "competitor", "erosion"],
        "keywords_tier1": ["moat", "barrier", "defend", "advantage"],
        "keywords_tier2": ["protect", "insulate", "fortify", "patent",
                           "monopoly", "exclusive", "lock", "shield"],
        "geometric_prediction": "position maintained proportional to barrier height",
        "implication_type": "conditional",
        "analogs": ["competitive_moats", "niche_specialization", "potential_wells"],
        "constraints": ["moat_erodes_without_maintenance", "sufficiently_novel_attack_bypasses"],
        "color_dimensions": {"width": "narrow_to_wide", "durability": "temporary_to_permanent"}
    },

    "principal_agent_system": {
        "structure": "principal delegates to agent whose incentives diverge from principal's interests",
        "elements": ["principal", "agent", "delegation", "misalignment", "monitoring"],
        "keywords_tier1": ["principal", "agent", "delegate", "misalign"],
        "keywords_tier2": ["incentive", "moral hazard", "shirk", "monitor",
                           "contract", "align", "trust", "verify"],
        "geometric_prediction": "agent behavior diverges from principal interest proportional to monitoring gap",
        "implication_type": "conditional",
        "analogs": ["shareholder_management", "symbiosis_conflict", "coupled_oscillators"],
        "constraints": ["information_asymmetry_required", "monitoring_costly"],
        "color_dimensions": {"alignment": "aligned_to_divergent", "transparency": "opaque_to_transparent"}
    },

    "commons_system": {
        "structure": "shared resource depleted by individually rational actors whose collective behavior is destructive",
        "elements": ["shared_resource", "individual_actors", "depletion", "collective_harm", "governance"],
        "keywords_tier1": ["commons", "shared", "deplete", "collective"],
        "keywords_tier2": ["public", "free-rider", "overuse", "tragedy",
                           "common pool", "exhaust", "govern", "cooperate"],
        "geometric_prediction": "unmanaged commons deplete to collapse",
        "implication_type": "decreases",
        "analogs": ["overfishing", "public_goods", "heat_dissipation"],
        "constraints": ["requires_shared_access", "governance_can_prevent_collapse"],
        "color_dimensions": {"excludability": "open_to_restricted", "rivalrousness": "rivalrous_to_non_rivalrous"}
    },

    "convention_system": {
        "structure": "arbitrary choice becomes standard through adoption creating coordination benefit",
        "elements": ["choice", "adoption", "coordination", "lock_in", "switching_cost"],
        "keywords_tier1": ["convention", "standard", "norm", "protocol"],
        "keywords_tier2": ["adopt", "conform", "custom", "tradition",
                           "default", "rule", "expectation", "format"],
        "geometric_prediction": "switching cost increases with adoption making change increasingly difficult",
        "implication_type": "conditional",
        "analogs": ["currency_adoption", "genetic_code_convention", "measurement_units"],
        "constraints": ["arbitrary_origin", "lock_in_increases_over_time"],
        "color_dimensions": {"entrenchment": "flexible_to_locked", "universality": "local_to_global"}
    },

    "innovation_system": {
        "structure": "novel combination of existing elements creates capability not present in components",
        "elements": ["existing_elements", "combination", "novelty", "capability", "disruption"],
        "keywords_tier1": ["innovate", "invent", "create", "novel"],
        "keywords_tier2": ["disrupt", "breakthrough", "pioneer", "discover",
                           "recombine", "prototype", "experiment", "iterate"],
        "geometric_prediction": "novel combinations create capabilities not predictable from components",
        "implication_type": "conditional",
        "analogs": ["genetic_recombination", "creative_destruction", "material_synthesis"],
        "constraints": ["requires_existing_elements", "most_combinations_fail"],
        "color_dimensions": {"novelty": "incremental_to_radical", "predictability": "expected_to_surprising"}
    },

    "predator_prey_system": {
        "structure": "consumer population grows consuming prey until prey decline causes consumer decline allowing prey recovery",
        "elements": ["predator", "prey", "consumption", "oscillation", "coupling"],
        "keywords_tier1": ["predator", "prey", "hunt", "consume"],
        "keywords_tier2": ["chase", "eat", "parasite", "host",
                           "exploit", "deplete", "recover", "cycle"],
        "geometric_prediction": "populations oscillate with predator lagging prey in coupled cycles",
        "implication_type": "conditional",
        "analogs": ["wolf_elk_dynamics", "speculator_market", "laser_population_inversion"],
        "constraints": ["requires_coupling", "removal_of_predator_causes_prey_explosion"],
        "color_dimensions": {"coupling_strength": "weak_to_strong", "stability": "stable_to_chaotic"}
    },

    "revelation_system": {
        "structure": "hidden information becomes visible triggering system-wide behavioral change",
        "elements": ["hidden_state", "revelation_event", "behavioral_change", "irreversibility", "cascade"],
        "keywords_tier1": ["reveal", "expose", "discover", "uncover"],
        "keywords_tier2": ["hidden", "secret", "disclose", "transparent",
                           "audit", "whistleblow", "detect", "surface"],
        "geometric_prediction": "revelation triggers irreversible behavioral shift",
        "implication_type": "conditional",
        "analogs": ["disease_diagnosis", "market_disclosure", "quantum_measurement"],
        "constraints": ["hidden_state_must_exist", "revelation_often_irreversible"],
        "color_dimensions": {"completeness": "partial_to_full", "impact": "minor_to_transformative"}
    },

    "coordination_system": {
        "structure": "independent agents align actions through signals producing collective outcome superior to individual",
        "elements": ["agents", "signals", "alignment", "collective_outcome", "cost"],
        "keywords_tier1": ["coordinate", "align", "synchronize", "cooperate"],
        "keywords_tier2": ["organize", "collaborate", "team", "consensus",
                           "signal", "rally", "unite", "harmonize"],
        "geometric_prediction": "coordination produces outcomes impossible for uncoordinated individuals",
        "implication_type": "conditional",
        "analogs": ["flock_behavior", "market_coordination", "magnetic_alignment"],
        "constraints": ["coordination_cost_exists", "miscoordination_wastes_resources"],
        "color_dimensions": {"mechanism": "implicit_to_explicit", "scale": "small_to_large"}
    },

    "immune_system": {
        "structure": "system detects foreign or aberrant elements and mounts targeted response to neutralize",
        "elements": ["detection", "recognition", "response", "memory", "tolerance"],
        "keywords_tier1": ["immune", "defend", "detect", "respond"],
        "keywords_tier2": ["attack", "protect", "antibody", "resistance",
                           "infection", "pathogen", "guard", "patrol"],
        "geometric_prediction": "response improves with exposure through memory formation",
        "implication_type": "conditional",
        "analogs": ["biological_immunity", "fraud_detection", "error_correction"],
        "constraints": ["false_positives_costly", "novel_threats_evade_initially"],
        "color_dimensions": {"specificity": "broad_to_targeted", "memory": "short_to_long"}
    },

    "mapping_system": {
        "structure": "correspondence between two structures that preserves key relationships enabling translation",
        "elements": ["source", "target", "correspondence", "preservation", "distortion"],
        "keywords_tier1": ["map", "correspond", "project", "represent"],
        "keywords_tier2": ["chart", "model", "mirror", "isomorphic",
                           "transform", "translate", "diagram", "analog"],
        "geometric_prediction": "map utility depends on relationship preservation not surface similarity",
        "implication_type": "conditional",
        "analogs": ["genetic_mapping", "market_modeling", "coordinate_transformations"],
        "constraints": ["all_maps_distort_something", "wrong_mapping_misleads"],
        "color_dimensions": {"fidelity": "approximate_to_exact", "completeness": "partial_to_total"}
    },

    "translation_system": {
        "structure": "information converted between representation systems with potential loss at boundaries",
        "elements": ["source_system", "target_system", "conversion_rules", "boundary_loss", "fidelity"],
        "keywords_tier1": ["translate", "convert", "encode", "decode"],
        "keywords_tier2": ["interpret", "transform", "transcode", "bridge",
                           "interface", "adapt", "format", "parse"],
        "geometric_prediction": "translation introduces boundary loss proportional to system difference",
        "implication_type": "conditional",
        "analogs": ["protein_synthesis", "currency_exchange", "fourier_transforms"],
        "constraints": ["perfect_translation_rare", "context_lost_at_boundary"],
        "color_dimensions": {"fidelity": "lossy_to_lossless", "complexity": "simple_to_complex"}
    },

    "vantage_system": {
        "structure": "observation point determines what is visible and what is hidden shaping all conclusions",
        "elements": ["observer", "position", "visible_field", "blind_spot", "bias"],
        "keywords_tier1": ["perspective", "vantage", "viewpoint", "frame"],
        "keywords_tier2": ["observe", "see", "angle", "lens",
                           "position", "bias", "blind", "scope"],
        "geometric_prediction": "changing vantage point reveals previously hidden structure",
        "implication_type": "conditional",
        "analogs": ["ecological_niche", "stakeholder_analysis", "reference_frames"],
        "constraints": ["no_vantage_sees_everything", "blind_spots_always_exist"],
        "color_dimensions": {"breadth": "narrow_to_wide", "mobility": "fixed_to_mobile"}
    },

    # ══════════════════════════════════════════════════════════════════
    # 17 ADDED SHAPES — derived February 25, 2026
    # ══════════════════════════════════════════════════════════════════

    "boundary_system": {
        "structure": "defined interface separating interior from exterior controlling exchange between domains",
        "elements": ["interior", "exterior", "membrane", "permeability", "identity"],
        "keywords_tier1": ["boundary", "border", "membrane", "interface"],
        "keywords_tier2": ["edge", "perimeter", "wall", "fence",
                           "divide", "separate", "contain", "cross"],
        "geometric_prediction": "boundary integrity determines system identity and survival",
        "implication_type": "conditional",
        "analogs": ["cell_membranes", "property_rights", "event_horizons"],
        "constraints": ["completely_closed_boundary_kills", "completely_open_boundary_dissolves"],
        "color_dimensions": {"permeability": "sealed_to_open", "definition": "sharp_to_fuzzy"}
    },

    "compression_system": {
        "structure": "structure forced into smaller representation preserving essential information while discarding redundancy",
        "elements": ["original", "compression", "essence", "loss", "reconstruction"],
        "keywords_tier1": ["compress", "condense", "encode", "compact"],
        "keywords_tier2": ["zip", "squeeze", "summarize", "reduce",
                           "distill", "concentrate", "archive", "dense"],
        "geometric_prediction": "compression approaches limit where further reduction destroys essential structure",
        "implication_type": "threshold",
        "analogs": ["DNA_encoding", "market_prices", "black_hole_compression"],
        "constraints": ["lossless_compression_has_limits", "over_compression_destroys_meaning"],
        "color_dimensions": {"ratio": "mild_to_extreme", "lossiness": "lossless_to_lossy"}
    },

    "synchronization_system": {
        "structure": "independent oscillators align timing through coupling without central controller",
        "elements": ["oscillators", "coupling", "phase_alignment", "entrainment", "drift"],
        "keywords_tier1": ["synchronize", "entrain", "phase", "align"],
        "keywords_tier2": ["rhythm", "timing", "lock", "pulse",
                           "beat", "resonance", "unison", "coherence"],
        "geometric_prediction": "coupled oscillators converge to shared frequency over time",
        "implication_type": "conditional",
        "analogs": ["firefly_synchronization", "financial_market_timing", "pendulum_entrainment"],
        "constraints": ["requires_coupling_mechanism", "noise_disrupts_synchronization"],
        "color_dimensions": {"coupling_strength": "weak_to_strong", "coherence": "partial_to_total"}
    },

    "mimicry_system": {
        "structure": "one structure copies another's form to exploit recognition systems built for the original",
        "elements": ["model", "mimic", "signal", "deceived_party", "advantage"],
        "keywords_tier1": ["mimic", "imitate", "copy", "counterfeit"],
        "keywords_tier2": ["fake", "disguise", "camouflage", "replicate",
                           "clone", "forge", "impersonate", "spoof"],
        "geometric_prediction": "mimicry succeeds until detection mechanisms evolve to distinguish",
        "implication_type": "conditional",
        "analogs": ["biological_camouflage", "brand_imitation", "metamaterial_cloaking"],
        "constraints": ["detection_pressure_evolves_counter", "perfect_mimicry_rare"],
        "color_dimensions": {"fidelity": "crude_to_perfect", "detection_difficulty": "easy_to_hard"}
    },

    "accumulation_system": {
        "structure": "small repeated inputs aggregate over time into disproportionately large mass",
        "elements": ["input", "aggregation", "mass", "time", "concentration"],
        "keywords_tier1": ["accumulate", "aggregate", "concentrate", "amass"],
        "keywords_tier2": ["pile", "collect", "gather", "heap",
                           "stockpile", "hoard", "build", "accrue"],
        "geometric_prediction": "small consistent inputs produce large accumulated mass over time",
        "implication_type": "increases",
        "analogs": ["wealth_concentration", "arterial_plaque_buildup", "gravitational_accretion"],
        "constraints": ["requires_consistent_input", "leakage_reduces_accumulation"],
        "color_dimensions": {"rate": "slow_to_fast", "distribution": "uniform_to_concentrated"}
    },

    "polarity_system": {
        "structure": "system organized around two opposing attractors with elements drawn toward one or the other",
        "elements": ["positive_pole", "negative_pole", "field", "attraction", "neutral_zone"],
        "keywords_tier1": ["polar", "oppose", "binary", "divide"],
        "keywords_tier2": ["positive", "negative", "attract", "repel",
                           "split", "extreme", "spectrum", "charge"],
        "geometric_prediction": "elements migrate toward poles depleting the neutral center",
        "implication_type": "conditional",
        "analogs": ["magnetic_polarity", "bull_bear_market_polarity", "cellular_polarity"],
        "constraints": ["requires_two_attractors", "external_force_can_repolarize"],
        "color_dimensions": {"strength": "weak_to_strong", "symmetry": "symmetric_to_asymmetric"}
    },

    "recursion_system": {
        "structure": "process that applies itself to its own output generating self-similar structure at multiple scales",
        "elements": ["base_case", "self_reference", "scale", "termination", "self_similarity"],
        "keywords_tier1": ["recursive", "fractal", "self-similar", "nested"],
        "keywords_tier2": ["iterate", "repeat", "meta", "loop",
                           "self-reference", "embed", "stack", "depth"],
        "geometric_prediction": "self-similar patterns appear at every scale until termination condition",
        "implication_type": "conditional",
        "analogs": ["fractal_branching", "compound_interest", "renormalization"],
        "constraints": ["requires_termination_condition", "infinite_recursion_destroys"],
        "color_dimensions": {"depth": "shallow_to_deep", "self_similarity": "approximate_to_exact"}
    },

    "latency_system": {
        "structure": "significant delay between cause and effect obscuring causal relationship",
        "elements": ["cause", "delay", "effect", "obscurement", "misattribution"],
        "keywords_tier1": ["latent", "delay", "lag", "incubate"],
        "keywords_tier2": ["dormant", "hidden", "slow", "wait",
                           "pending", "deferred", "backlog", "buffer"],
        "geometric_prediction": "effects attributed to proximate cause rather than true delayed cause",
        "implication_type": "conditional",
        "analogs": ["disease_incubation", "policy_lag", "light_propagation_delay"],
        "constraints": ["delay_obscures_causation", "longer_delay_increases_misattribution"],
        "color_dimensions": {"duration": "short_to_long", "visibility": "obvious_to_hidden"}
    },

    "absorption_system": {
        "structure": "one system takes in material from another and integrates it into own structure",
        "elements": ["absorber", "material", "integration", "transformation", "residual"],
        "keywords_tier1": ["absorb", "integrate", "assimilate", "incorporate"],
        "keywords_tier2": ["ingest", "take", "merge", "consume",
                           "engulf", "internalize", "adopt", "subsume"],
        "geometric_prediction": "absorber grows while source diminishes, absorbed material transforms",
        "implication_type": "conditional",
        "analogs": ["cellular_digestion", "corporate_acquisition", "black_body_radiation"],
        "constraints": ["absorption_capacity_limited", "indigestible_material_accumulates"],
        "color_dimensions": {"selectivity": "indiscriminate_to_selective", "completeness": "partial_to_total"}
    },

    "fragmentation_system": {
        "structure": "unified whole breaks into smaller competing parts that may diverge over time",
        "elements": ["whole", "fracture", "fragments", "competition", "divergence"],
        "keywords_tier1": ["fragment", "divide", "split", "fracture"],
        "keywords_tier2": ["break", "shatter", "partition", "segment",
                           "splinter", "separate", "faction", "branch"],
        "geometric_prediction": "fragments diverge and compete unless reunification force applied",
        "implication_type": "conditional",
        "analogs": ["cell_division", "market_segmentation", "nuclear_fission"],
        "constraints": ["fragmentation_releases_energy", "fragments_may_not_recombine"],
        "color_dimensions": {"uniformity": "clean_to_irregular", "reversibility": "reversible_to_permanent"}
    },

    "amplification_system": {
        "structure": "small input signal produces disproportionately large output through energy-fed gain mechanism",
        "elements": ["signal", "gain", "energy_source", "output", "saturation"],
        "keywords_tier1": ["amplify", "boost", "intensify", "magnify"],
        "keywords_tier2": ["gain", "loud", "enhance", "escalate",
                           "strengthen", "increase", "power", "signal"],
        "geometric_prediction": "output proportional to gain until saturation or distortion",
        "implication_type": "increases",
        "analogs": ["gene_expression", "viral_marketing", "electronic_amplification"],
        "constraints": ["requires_energy_source", "saturation_limits_output"],
        "color_dimensions": {"gain": "low_to_high", "linearity": "linear_to_distorted"}
    },

    "containment_system": {
        "structure": "energy or matter confined within boundary generating internal pressure",
        "elements": ["contents", "boundary", "pressure", "capacity", "rupture_point"],
        "keywords_tier1": ["contain", "pressure", "confine", "hold"],
        "keywords_tier2": ["vessel", "dam", "suppress", "restrain",
                           "bottle", "trap", "seal", "store"],
        "geometric_prediction": "pressure increases until release or catastrophic rupture",
        "implication_type": "threshold",
        "analogs": ["turgor_pressure", "monopoly_pricing", "stellar_cores"],
        "constraints": ["boundary_has_maximum_capacity", "rupture_is_catastrophic"],
        "color_dimensions": {"pressure": "low_to_critical", "boundary_strength": "weak_to_strong"}
    },

    "signal_noise_system": {
        "structure": "useful information embedded in interference requiring extraction through filtering",
        "elements": ["signal", "noise", "filter", "ratio", "detection_threshold"],
        "keywords_tier1": ["signal", "noise", "filter", "detect"],
        "keywords_tier2": ["interference", "static", "clarity", "fidelity",
                           "ratio", "extract", "clean", "tune"],
        "geometric_prediction": "information recoverable only when signal-to-noise ratio exceeds threshold",
        "implication_type": "threshold",
        "analogs": ["sensory_perception", "financial_signals", "radio_transmission"],
        "constraints": ["noise_floor_exists", "over_filtering_destroys_signal"],
        "color_dimensions": {"ratio": "low_to_high", "noise_type": "random_to_structured"}
    },

    "inversion_system": {
        "structure": "system under sufficient pressure inverts its own operating logic producing opposite behavior",
        "elements": ["original_state", "pressure", "inversion_point", "reversed_state", "hysteresis"],
        "keywords_tier1": ["invert", "reverse", "flip", "transform"],
        "keywords_tier2": ["opposite", "mirror", "switch", "pivot",
                           "overturn", "convert", "negate", "phase"],
        "geometric_prediction": "system operates normally until pressure triggers complete behavioral inversion",
        "implication_type": "threshold",
        "analogs": ["phase_transitions", "market_reversals", "immune_autoresponse"],
        "constraints": ["inversion_point_often_unpredictable", "hysteresis_prevents_easy_return"],
        "color_dimensions": {"pressure_required": "low_to_high", "completeness": "partial_to_total"}
    },

    "dormancy_system": {
        "structure": "system suspends active operation while preserving internal structure awaiting activation trigger",
        "elements": ["active_state", "suspension", "preservation", "trigger", "reactivation"],
        "keywords_tier1": ["dormant", "hibernate", "latent", "suspend"],
        "keywords_tier2": ["sleep", "inactive", "idle", "pause",
                           "freeze", "archive", "store", "seed"],
        "geometric_prediction": "system reactivates when trigger conditions met, potentially after long delay",
        "implication_type": "conditional",
        "analogs": ["seed_germination", "latent_demand", "metastable_states"],
        "constraints": ["preservation_degrades_over_time", "trigger_must_be_specific"],
        "color_dimensions": {"duration": "short_to_indefinite", "preservation_quality": "degraded_to_perfect"}
    },

    "escalation_system": {
        "structure": "each response exceeds the prior action creating compounding intensity spiral",
        "elements": ["action", "response", "escalation_rate", "intensity", "breaking_point"],
        "keywords_tier1": ["escalate", "intensify", "spiral", "arms race"],
        "keywords_tier2": ["ratchet", "accelerate", "worsen", "inflame",
                           "provoke", "retaliate", "war", "compete"],
        "geometric_prediction": "intensity increases until one party exhausts resources or breaking point reached",
        "implication_type": "increases",
        "analogs": ["price_wars", "inflammatory_response", "nuclear_chain_reaction"],
        "constraints": ["requires_responsive_parties", "breaking_point_exists"],
        "color_dimensions": {"rate": "gradual_to_rapid", "destructiveness": "constructive_to_destructive"}
    },

    "calibration_system": {
        "structure": "system continuously compares output against reference and adjusts parameters to minimize deviation",
        "elements": ["reference", "measurement", "deviation", "adjustment", "precision"],
        "keywords_tier1": ["calibrate", "adjust", "tune", "regulate"],
        "keywords_tier2": ["correct", "normalize", "set", "tweak",
                           "fine-tune", "align", "compensate", "stabilize"],
        "geometric_prediction": "deviation from reference decreases with each adjustment cycle",
        "implication_type": "conditional",
        "analogs": ["circadian_rhythm", "interest_rate_policy", "instrument_tuning"],
        "constraints": ["requires_reference_signal", "over_correction_causes_oscillation"],
        "color_dimensions": {"precision": "coarse_to_fine", "response_speed": "slow_to_fast"}
    },
}


def get_all_shapes():
    return SHAPE_LIBRARY


def get_shape(name):
    return SHAPE_LIBRARY.get(name)


def validate_shape_library(library):
    required_fields = ["structure", "elements", "keywords_tier1", "keywords_tier2",
                       "geometric_prediction", "implication_type", "analogs", "constraints", "color_dimensions"]
    valid_types = ["increases", "decreases", "conditional", "threshold", "unconditional"]
    errors = []
    for name, shape in library.items():
        for field in required_fields:
            if field not in shape:
                errors.append(f"{name}: missing {field}")
        if shape.get("implication_type") not in valid_types:
            errors.append(f"{name}: invalid implication_type")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
    else:
        print(f"All {len(library)} shapes valid")
    return len(errors) == 0


if __name__ == "__main__":
    validate_shape_library(SHAPE_LIBRARY)
