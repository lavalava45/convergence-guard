#!/usr/bin/env python3
"""Post-benchmark Convergence Guard v0.2 orchestration primitives.

This module deliberately does not replace the frozen main-v0.1.7 harness.  It is
the conformance-corrected implementation target for subsequent evals.

The caller supplies a `call_json(stage, prompt, schema)` function.  That keeps
runtime/provider code outside the protocol state machine and makes conditional
stage execution testable without model calls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Callable


CallJSON = Callable[[str, str, dict[str, Any]], dict[str, Any]]


SEARCH_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["models"],
    "properties": {
        "models": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "claim",
                    "mechanism",
                    "necessary_conditions",
                    "predictions",
                    "implied_action",
                    "disconfirming_evidence",
                    "identification_threats",
                    "conflicts_with_evidence",
                ],
                "properties": {
                    "claim": {"type": "string"},
                    "mechanism": {"type": "string"},
                    "necessary_conditions": {"type": "array", "items": {"type": "string"}},
                    "predictions": {"type": "array", "items": {"type": "string"}},
                    "implied_action": {"type": "string"},
                    "disconfirming_evidence": {"type": "array", "items": {"type": "string"}},
                    "identification_threats": {"type": "array", "items": {"type": "string"}},
                    "conflicts_with_evidence": {"type": "array", "items": {"type": "string"}},
                },
            },
        }
    },
}


COVERAGE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["expand", "reasons", "new_mandates"],
    "properties": {
        "expand": {"type": "boolean"},
        "reasons": {"type": "array", "items": {"type": "string"}},
        "new_mandates": {"type": "array", "maxItems": 2, "items": {"type": "string"}},
    },
}


SCREEN_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["evaluations"],
    "properties": {
        "evaluations": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "candidate_id",
                    "contract_fit",
                    "evidence_support",
                    "causal_completeness",
                    "causal_identification",
                    "identification_threat",
                    "discriminability",
                    "decision_exposure",
                    "danger_flags",
                    "evidence_ids",
                ],
                "properties": {
                    "candidate_id": {"type": "string"},
                    "contract_fit": {"type": "string", "enum": ["PASS", "CONDITIONAL", "FAIL"]},
                    "evidence_support": {"type": "string", "enum": ["STRONG", "MIXED", "WEAK"]},
                    "causal_completeness": {"type": "string", "enum": ["CHAIN PRESENT", "PARTIAL", "ASSERTION ONLY"]},
                    "causal_identification": {"type": "string", "enum": ["SUPPORTED", "THREATENED", "UNIDENTIFIED"]},
                    "identification_threat": {"type": "string"},
                    "discriminability": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                    "decision_exposure": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
                    "danger_flags": {"type": "array", "items": {"type": "string"}},
                    "evidence_ids": {"type": "array", "items": {"type": "string"}},
                },
            },
        }
    },
}


MAP_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["families", "relations", "boundary_critic_needed", "boundary_issue"],
    "properties": {
        "families": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["family_id", "candidate_ids", "summary"],
                "properties": {
                    "family_id": {"type": "string"},
                    "candidate_ids": {"type": "array", "items": {"type": "string"}},
                    "summary": {"type": "string"},
                },
            },
        },
        "relations": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["candidate_a", "candidate_b", "relation", "rationale"],
                "properties": {
                    "candidate_a": {"type": "string"},
                    "candidate_b": {"type": "string"},
                    "relation": {"type": "string", "enum": ["EXCLUSIVE", "COEXISTING", "NESTED", "INTERACTING"]},
                    "rationale": {"type": "string"},
                },
            },
        },
        "boundary_critic_needed": {"type": "boolean"},
        "boundary_issue": {"type": "string"},
    },
}


BOUNDARY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["resolved", "rationale", "revised_mapping"],
    "properties": {
        "resolved": {"type": "boolean"},
        "rationale": {"type": "string"},
        "revised_mapping": MAP_SCHEMA,
    },
}


SLATE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "finalist_ids",
        "information_probe_id",
        "excluded_strong_models",
        "checkpoint_needed",
        "checkpoint_reason",
        "targeted_search_mandate",
    ],
    "properties": {
        "finalist_ids": {"type": "array", "maxItems": 3, "items": {"type": "string"}},
        "information_probe_id": {"type": ["string", "null"]},
        "excluded_strong_models": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["candidate_id", "reason"],
                "properties": {
                    "candidate_id": {"type": "string"},
                    "reason": {"type": "string"},
                },
            },
        },
        "checkpoint_needed": {"type": "boolean"},
        "checkpoint_reason": {"type": "string"},
        "targeted_search_mandate": {"type": ["string", "null"]},
    },
}


DOSSIER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "candidate_id",
        "mechanism",
        "assumptions",
        "predictions",
        "disconfirming_observations",
        "decision_consequence",
        "identification_weaknesses",
        "error_cost_reversibility",
        "revision_required",
        "revised_claim",
        "revised_mechanism",
        "new_load_bearing_premises",
    ],
    "properties": {
        "candidate_id": {"type": "string"},
        "mechanism": {"type": "string"},
        "assumptions": {"type": "array", "items": {"type": "string"}},
        "predictions": {"type": "array", "items": {"type": "string"}},
        "disconfirming_observations": {"type": "array", "items": {"type": "string"}},
        "decision_consequence": {"type": "string"},
        "identification_weaknesses": {"type": "array", "items": {"type": "string"}},
        "error_cost_reversibility": {"type": "string"},
        "revision_required": {"type": "boolean"},
        "revised_claim": {"type": ["string", "null"]},
        "revised_mechanism": {"type": ["string", "null"]},
        "new_load_bearing_premises": {"type": "array", "items": {"type": "string"}},
    },
}


ADJUDICATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "model_judgment",
        "action_judgment",
        "sensitivity_summary",
        "shared_bias_summary",
        "collision_summary",
        "reroute_needed",
        "reroute_reason",
        "reroute_mandate",
        "second_opinion_needed",
        "second_opinion_reason",
        "next_test",
    ],
    "properties": {
        "model_judgment": {
            "type": "object",
            "additionalProperties": False,
            "required": ["status", "supported_candidate_ids", "relation", "residual_uncertainty"],
            "properties": {
                "status": {"type": "string", "enum": ["CHOOSE", "COEXIST", "INSUFFICIENT", "NO_SUPPORTED_MODEL"]},
                "supported_candidate_ids": {"type": "array", "items": {"type": "string"}},
                "relation": {"type": "string", "enum": ["EXCLUSIVE", "COEXISTING", "NESTED", "INTERACTING", "UNRESOLVED", "NOT_APPLICABLE"]},
                "residual_uncertainty": {"type": "string"},
            },
        },
        "action_judgment": {
            "type": "object",
            "additionalProperties": False,
            "required": ["status", "preferred_action", "rationale", "conditions"],
            "properties": {
                "status": {"type": "string", "enum": ["CHOOSE_ACTION", "CONDITIONAL_ACTION", "DEFER_ACTION", "NO_ACTION_NEEDED"]},
                "preferred_action": {"type": ["string", "null"]},
                "rationale": {"type": "string"},
                "conditions": {"type": "array", "items": {"type": "string"}},
            },
        },
        "sensitivity_summary": {"type": "string"},
        "shared_bias_summary": {"type": "string"},
        "collision_summary": {"type": "string"},
        "reroute_needed": {"type": "boolean"},
        "reroute_reason": {"type": "string"},
        "reroute_mandate": {"type": ["string", "null"]},
        "second_opinion_needed": {"type": "boolean"},
        "second_opinion_reason": {"type": "string"},
        "next_test": {
            "type": "object",
            "additionalProperties": False,
            "required": ["status", "description", "decision_rule"],
            "properties": {
                "status": {"type": "string", "enum": ["PROPOSED", "NO_FEASIBLE_DISCRIMINATOR", "DEFERRED_FOR_BUDGET", "NOT_NEEDED"]},
                "description": {"type": ["string", "null"]},
                "decision_rule": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
}


SECOND_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "disposition",
        "decisive_inference",
        "unsupported_premises",
        "missing_family_or_evidence",
        "action_conflict",
        "conditions_or_limits",
    ],
    "properties": {
        "disposition": {"type": "string", "enum": ["CONFIRM", "QUALIFY", "CHALLENGE"]},
        "decisive_inference": {"type": "string"},
        "unsupported_premises": {"type": "array", "items": {"type": "string"}},
        "missing_family_or_evidence": {"type": "array", "items": {"type": "string"}},
        "action_conflict": {"type": "boolean"},
        "conditions_or_limits": {"type": "array", "items": {"type": "string"}},
    },
}


@dataclass
class ProtocolLedger:
    completed: list[str] = field(default_factory=list)
    skipped: list[dict[str, str]] = field(default_factory=list)
    triggered_but_unexecuted: list[str] = field(default_factory=list)
    pending_hypotheses: list[str] = field(default_factory=list)
    material_omissions: list[str] = field(default_factory=list)
    corrective_cycles: int = 0
    budget_stop: bool = False

    def complete(self, stage: str) -> None:
        if stage not in self.completed:
            self.completed.append(stage)

    def skip(self, stage: str, reason: str) -> None:
        self.skipped.append({"stage": stage, "reason": reason})

    def completion_object(self) -> dict[str, Any]:
        if self.budget_stop:
            status = "BUDGET_STOP"
        elif self.triggered_but_unexecuted or self.pending_hypotheses or self.material_omissions:
            status = "PARTIAL_PROTOCOL"
        else:
            status = "COMPLETE"
        return {
            "status": status,
            "completed_stages": list(self.completed),
            "skipped_stages": list(self.skipped),
            "triggered_but_unexecuted": list(self.triggered_but_unexecuted),
            "pending_hypotheses": list(self.pending_hypotheses),
            "material_omissions": list(self.material_omissions),
        }


def _write(run_dir: Path, name: str, payload: Any) -> None:
    path = run_dir / "working" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _candidate_projection(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        key: candidate.get(key)
        for key in (
            "id",
            "claim",
            "mechanism",
            "necessary_conditions",
            "predictions",
            "implied_action",
            "disconfirming_evidence",
        )
    }


def neutralize(search_outputs: list[tuple[str, dict[str, Any]]]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    candidates: list[dict[str, Any]] = []
    trace: dict[str, str] = {}
    counter = 1
    for stage, output in search_outputs:
        for model in output.get("models", []):
            cid = f"H{counter:02d}"
            item = dict(model)
            item["id"] = cid
            candidates.append(item)
            trace[cid] = stage
            counter += 1
    return candidates, trace


def build_reduced_prompt(*, case_id: str, material: str, contract: str, packet_text: str) -> str:
    return f"""This is a controlled evaluation run.
Use only supplied case material. Do not browse or add outside facts.

TREATMENT: Convergence Guard — Reduced Mode v0.2.
The following protocol packet is complete for this run. Do not assume access to
any external reference that is not reproduced below.

SELF-CONTAINED REDUCED PROTOCOL:
{packet_text}

DECISION CONTRACT:
{contract}

PARTICIPANT-VISIBLE CASE:
{material}

Execute the workflow in one effective context. Keep the required sequential
passes conceptually separate, but do not call them independent. Return exactly
the supplied v0.2 final schema for case_id {case_id}.
"""


def execute_full_v02(
    *,
    case_id: str,
    material: str,
    contract: str,
    mandates: list[str],
    call_json: CallJSON,
    final_schema: dict[str, Any],
    run_dir: Path,
    max_corrective_cycles: int = 2,
) -> dict[str, Any]:
    """Execute the conformance-corrected Full workflow.

    The function intentionally fails *visibly* through the protocol ledger when
    a triggered corrective stage cannot be completed.  It never substitutes a
    rejected candidate merely to keep the workflow moving.
    """

    ledger = ProtocolLedger()
    framing = (
        "Check whether framing, proxy objectives, missing system boundaries, or "
        "an outside-view conflict could materially change the decision. Do not "
        "replace supplied evidence with generic priors."
    )
    ledger.complete("A1")
    ledger.complete("A2")
    ledger.complete("A3")

    search_outputs: list[tuple[str, dict[str, Any]]] = []

    def run_search(stage: str, mandate: str) -> None:
        prompt = f"""You are an isolated Convergence Guard causal-search worker.

AUTHORIZED INPUTS ONLY:
PUBLIC EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

FRAMING CHECK:
{framing}

YOUR MANDATE:
{mandate}

You have no access to other workers, prior branch outputs, screening, mapping,
coordinator preferences, memory, or outside facts. Generate 2–4 causally
distinct models within the mandate, or an empty list if none is viable. Return
claim, mechanism, necessary conditions, observable predictions, implied action,
disconfirming evidence, causal-identification threats, and conflicts with the
supplied evidence.
"""
        search_outputs.append((stage, call_json(stage, prompt, SEARCH_SCHEMA)))
        ledger.complete(stage)

    for idx, mandate in enumerate(mandates[:3], start=1):
        run_search(f"B1-search-{idx}", mandate)
    ledger.complete("B1")

    coverage_prompt = f"""You are the Convergence Guard B2 coverage gate.
Use only the supplied evidence, decision contract, framing check, and the
neutral content of the three completed search outputs. Do not rank a favorite.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

FRAMING:
{framing}

SEARCH OUTPUTS:
{json.dumps([o for _, o in search_outputs], ensure_ascii=False)}

Expand search only if outputs cover substantially the same causal region, a
major system boundary/intervention class remains unexamined, fewer than two
decision-relevant families survive basic factual sanity, or framing exposes a
plausible missing family. If expansion is needed, return one or two NEW mandates
targeted at uncovered regions. Expansion workers must not receive prior outputs.
"""
    coverage = call_json("B2-coverage", coverage_prompt, COVERAGE_SCHEMA)
    _write(run_dir, "B2-coverage.json", coverage)
    ledger.complete("B2")
    if coverage.get("expand"):
        new_mandates = [m for m in coverage.get("new_mandates", []) if m][:2]
        if not new_mandates:
            ledger.triggered_but_unexecuted.append("B2-expansion")
            ledger.material_omissions.append("B2 requested expansion but supplied no executable mandate")
        for offset, mandate in enumerate(new_mandates, start=4):
            run_search(f"B2-search-{offset}", mandate)
    else:
        ledger.skip("B2-expansion", "coverage gate did not trigger expansion")

    candidates, trace = neutralize(search_outputs)
    _write(run_dir, "neutral-candidates.json", candidates)
    _write(run_dir, "private-trace-map.json", trace)

    next_candidate = len(candidates) + 1

    def c_pipeline() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        nonlocal candidates
        screen_prompt = f"""You are the fresh C1 contract screener. You receive
no branch identity, mapper output, coordinator preference, or downstream role.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

NEUTRAL CANDIDATES:
{json.dumps(candidates, ensure_ascii=False)}

Evaluate each candidate exactly once. Do not compute an aggregate score. Anchor
qualitative labels in named evidence IDs: STRONG requires direct/independent and
consistent support; MIXED means material support plus a real weakness or
dependence; WEAK means mostly indirect/speculative support. HIGH discriminability
requires a feasible decision-relevant observation that separates the candidate
from a live rival; LOW means no such practical separator is identified. Decision
exposure reflects downside and reversibility if action based on the candidate is
wrong. Return evidence_ids for each evaluation.
"""
        screen = call_json("C1-screen", screen_prompt, SCREEN_SCHEMA)
        ledger.complete("C1")

        mapper_candidates = [_candidate_projection(c) for c in candidates]
        map_prompt = f"""You are the fresh C2 blind causal mapper. You do not see
C1 results, branch identity, danger flags, or coordinator preference.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

NEUTRAL CANDIDATE CONTENT:
{json.dumps(mapper_candidates, ensure_ascii=False)}

Map causal families without targeting a fixed count. Relations are EXCLUSIVE,
COEXISTING, NESTED, or INTERACTING. Merge only materially equivalent mechanisms
and predictions; duplicates are not independent support. Set
boundary_critic_needed only if an uncertain merge/relation could change the
decision, and describe that exact issue.
"""
        mapping = call_json("C2-map", map_prompt, MAP_SCHEMA)
        ledger.complete("C2")

        if mapping.get("boundary_critic_needed"):
            boundary_prompt = f"""You are the fresh C3 boundary critic. You do
not see C1 scores/danger flags, branch identity, coordinator preference, or
finalist-selection signals.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

NEUTRAL CANDIDATE MATERIAL:
{json.dumps(mapper_candidates, ensure_ascii=False)}

MAPPER'S DISPUTED MAPPING:
{json.dumps(mapping, ensure_ascii=False)}

Resolve only the stated decision-relevant boundary. Preserve other mapping
content unless the disputed boundary logically requires a change. Return a full
revised mapping and rationale.
"""
            boundary = call_json("C3-boundary", boundary_prompt, BOUNDARY_SCHEMA)
            _write(run_dir, "C3-boundary.json", boundary)
            ledger.complete("C3")
            mapping = boundary["revised_mapping"]
        else:
            ledger.skip("C3", "C2 reported no decision-relevant boundary ambiguity")

        slate_prompt = f"""You are the C4 slate coordinator. C1 and C2 are frozen.
Do not use an aggregate score and do not pad the slate.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

CANDIDATES:
{json.dumps(candidates, ensure_ascii=False)}

C1 SCREEN:
{json.dumps(screen, ensure_ascii=False)}

C2/C3 MAP:
{json.dumps(mapping, ensure_ascii=False)}

Normally retain 2–3 causally distinct non-dominated finalists. One is allowed;
zero is allowed. Do not promote FAIL/unsupported models just to fill a slot and
do not reject a causal model merely because its implied intervention is costly.
Record why any strong non-dominated outside model is excluded. If missing
evidence or a missing family could materially change the slate, request a
targeted search checkpoint and give one executable mandate. Choose at most one
information probe separately from finalists.
"""
        slate = call_json("C4-slate", slate_prompt, SLATE_SCHEMA)
        ledger.complete("C4")
        return screen, mapping, slate

    screen: dict[str, Any]
    mapping: dict[str, Any]
    slate: dict[str, Any]

    while True:
        screen, mapping, slate = c_pipeline()
        if not slate.get("checkpoint_needed"):
            break
        mandate = slate.get("targeted_search_mandate")
        if ledger.corrective_cycles >= max_corrective_cycles or not mandate:
            ledger.triggered_but_unexecuted.append("C4-targeted-checkpoint")
            ledger.material_omissions.append(slate.get("checkpoint_reason") or "C4 checkpoint unresolved")
            break
        ledger.corrective_cycles += 1
        run_search(f"C4-checkpoint-search-{ledger.corrective_cycles}", mandate)
        new_candidates, new_trace = neutralize([search_outputs[-1]])
        # Renumber newly neutralized local H01... IDs into globally unique IDs.
        for item in new_candidates:
            cid = f"H{next_candidate:02d}"
            next_candidate += 1
            item["id"] = cid
            candidates.append(item)
            trace[cid] = search_outputs[-1][0]
        _write(run_dir, "neutral-candidates.json", candidates)
        _write(run_dir, "private-trace-map.json", trace)

    def finalists_from_slate() -> list[dict[str, Any]]:
        ids = list(dict.fromkeys(slate.get("finalist_ids", [])))
        by_id = {c["id"]: c for c in candidates}
        unknown = [cid for cid in ids if cid not in by_id]
        if unknown:
            ledger.material_omissions.append(f"C4 returned unknown finalist IDs: {unknown}")
        return [by_id[cid] for cid in ids if cid in by_id][:3]

    dossiers: list[dict[str, Any]] = []
    while True:
        finalists = finalists_from_slate()
        dossiers = []
        revisions: list[dict[str, Any]] = []
        for idx, finalist in enumerate(finalists, start=1):
            stage = f"D1-dossier-{idx}"
            dossier_prompt = f"""You are an isolated D1 dossier worker. You
receive one finalist only and must not compare it with unseen rivals.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

ONE FINALIST:
{json.dumps(finalist, ensure_ascii=False)}

Preserve the model's mechanism. State load-bearing assumptions, predictions,
concrete disconfirming observations, decision consequence, identification
weaknesses, and cost/reversibility of acting while wrong. If the evidence forces
a material mechanism change or a new load-bearing premise, do NOT silently edit
the finalist: set revision_required=true and provide the revised claim/mechanism
and new premises so the coordinator can create a new hypothesis ID and rerun C.
"""
            dossier = call_json(stage, dossier_prompt, DOSSIER_SCHEMA)
            dossiers.append(dossier)
            ledger.complete(stage)
            if dossier.get("revision_required"):
                revisions.append({"source": finalist, "dossier": dossier})

        if not revisions:
            ledger.complete("D1")
            break
        if ledger.corrective_cycles >= max_corrective_cycles:
            for rev in revisions:
                ledger.pending_hypotheses.append(rev["source"]["id"] + "-revision")
            ledger.material_omissions.append("D1 material revisions could not be rerouted within corrective-cycle budget")
            break

        ledger.corrective_cycles += 1
        revision_map: list[dict[str, str]] = []
        for rev in revisions:
            source = rev["source"]
            dossier = rev["dossier"]
            new_id = f"H{next_candidate:02d}"
            next_candidate += 1
            revised = dict(source)
            revised["id"] = new_id
            revised["claim"] = dossier.get("revised_claim") or source.get("claim", "")
            revised["mechanism"] = dossier.get("revised_mechanism") or source.get("mechanism", "")
            candidates.append(revised)
            ledger.pending_hypotheses.append(new_id)
            revision_map.append({"from": source["id"], "to": new_id})
        _write(run_dir, f"D1-revision-cycle-{ledger.corrective_cycles}.json", revision_map)
        screen, mapping, slate = c_pipeline()
        # The revised IDs stay pending until the new D1/D2 path completes.

    adjudicate_prompt = f"""You are the fresh D2 slate-level adjudicator. You
did not author search, screening, mapping, slate selection, or dossiers and do
not see early ranks or coordinator preference.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

NEUTRAL FINALIST DOSSIERS:
{json.dumps(dossiers, ensure_ascii=False)}

Perform in order: assumption sensitivity; shared-bias audit; pairwise decision
collision only where action implications conflict. Keep model judgment separate
from action judgment. A supported COEXISTING/INTERACTING structure must not be
erased merely because action choice remains insufficient. If shared-bias audit
finds a genuinely missing family/evidence that could change the slate, set
reroute_needed=true and provide one targeted search mandate rather than silently
injecting an outside candidate. Trigger D3 only for cycle/repeated undetermined,
weak apparent winner, serious shared blind spot, unusual irreversibility, or an
unexplained sharp conflict. Propose a decision-changing next test only when one
is feasible and worthwhile.
"""
    adjudication = call_json("D2-adjudication", adjudicate_prompt, ADJUDICATION_SCHEMA)
    ledger.complete("D2")

    if adjudication.get("reroute_needed"):
        mandate = adjudication.get("reroute_mandate")
        if ledger.corrective_cycles < max_corrective_cycles and mandate:
            ledger.corrective_cycles += 1
            run_search(f"D2-reroute-search-{ledger.corrective_cycles}", mandate)
            new_candidates, _ = neutralize([search_outputs[-1]])
            for item in new_candidates:
                cid = f"H{next_candidate:02d}"
                next_candidate += 1
                item["id"] = cid
                candidates.append(item)
                trace[cid] = search_outputs[-1][0]
            _write(run_dir, "neutral-candidates.json", candidates)
            _write(run_dir, "private-trace-map.json", trace)
            screen, mapping, slate = c_pipeline()
            # Rebuild D1 once for the new slate, then rerun D2. If those dossiers
            # themselves revise mechanisms, mark partial rather than laundering.
            finalists = finalists_from_slate()
            dossiers = []
            reroute_revision = False
            for idx, finalist in enumerate(finalists, start=1):
                stage = f"D1-reroute-dossier-{idx}"
                prompt = f"""You are an isolated D1 dossier worker after a
shared-bias reroute. Preserve the supplied finalist mechanism; if material
revision is required, set revision_required=true instead of silently editing it.

EVIDENCE:\n{material}\n\nDECISION CONTRACT:\n{contract}\n\nFINALIST:\n{json.dumps(finalist, ensure_ascii=False)}
"""
                dossier = call_json(stage, prompt, DOSSIER_SCHEMA)
                dossiers.append(dossier)
                ledger.complete(stage)
                reroute_revision = reroute_revision or bool(dossier.get("revision_required"))
            if reroute_revision:
                ledger.triggered_but_unexecuted.append("D1-reroute-revision")
                ledger.material_omissions.append("A rerouted dossier still required material mechanism revision")
            adjudicate_prompt_2 = f"""You are the fresh D2 slate-level adjudicator
after one shared-bias reroute. Apply the same D2 rules as before.

EVIDENCE:\n{material}\n\nDECISION CONTRACT:\n{contract}\n\nNEUTRAL FINALIST DOSSIERS:\n{json.dumps(dossiers, ensure_ascii=False)}

Perform assumption sensitivity, shared-bias audit, and pairwise decision
collision only where action implications conflict. Separate model and action
judgments. Do not smuggle in excluded candidates. Report another reroute need
honestly if one remains.
"""
            adjudication = call_json("D2-adjudication-rerun", adjudicate_prompt_2, ADJUDICATION_SCHEMA)
            ledger.complete("D2-rerun")
        else:
            ledger.triggered_but_unexecuted.append("D2-shared-bias-reroute")
            ledger.material_omissions.append(adjudication.get("reroute_reason") or "D2 reroute unresolved")

    second: dict[str, Any] | None = None
    if adjudication.get("second_opinion_needed"):
        second_prompt = f"""You are the fresh D3 independent second-opinion
reviewer. Reconstruct the decisive inference without seeing coordinator
preference or D2's pairwise action preferences. Do not label any candidate or
action as the winner.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

NEUTRAL FEASIBLE-ACTION FRAME:
{json.dumps([d.get('decision_consequence') for d in dossiers], ensure_ascii=False)}

NEUTRAL CANDIDATE CLAIMS:
{json.dumps([{'id': c['id'], 'claim': c.get('claim'), 'mechanism': c.get('mechanism')} for c in finalists_from_slate()], ensure_ascii=False)}

DOSSIER MATERIAL TO AUDIT FOR ADDED PREMISES:
{json.dumps(dossiers, ensure_ascii=False)}

Return CONFIRM, QUALIFY, or CHALLENGE; decisive inference; unsupported premises;
missing family/evidence; whether disagreement could change action; and explicit
conditions/limits. Do not browse.
"""
        second = call_json("D3-second-opinion", second_prompt, SECOND_SCHEMA)
        ledger.complete("D3")
        if second.get("disposition") == "CHALLENGE" and second.get("missing_family_or_evidence"):
            ledger.material_omissions.append(
                "D3 challenge identified missing family/evidence requiring upstream checkpoint"
            )
        if second.get("disposition") == "CHALLENGE" and second.get("action_conflict"):
            ledger.material_omissions.append("Decision-changing D2/D3 conflict remains unresolved")
    else:
        ledger.skip("D3", adjudication.get("second_opinion_reason") or "D3 trigger not met")

    # Clear only revised hypotheses that actually reached the currently
    # adjudicated dossier set. A revised model that was never selected/dossiered
    # remains PENDING and therefore prevents a misleading COMPLETE label.
    adjudicated_ids = {
        dossier.get("candidate_id")
        for dossier in dossiers
        if isinstance(dossier, dict) and isinstance(dossier.get("candidate_id"), str)
    }
    ledger.pending_hypotheses = [
        hypothesis_id
        for hypothesis_id in ledger.pending_hypotheses
        if hypothesis_id not in adjudicated_ids
    ]

    completion = ledger.completion_object()
    final_prompt = f"""You are the Phase-E final coordinator. Return exactly the
v0.2 final schema. Causal structure, action sufficiency, and next-test status
are separate judgments. The protocol-completion object below is a harness fact;
copy it exactly and do not upgrade PARTIAL_PROTOCOL/BUDGET_STOP to COMPLETE.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

FINALIST DOSSIERS:
{json.dumps(dossiers, ensure_ascii=False)}

D2 ADJUDICATION:
{json.dumps(adjudication, ensure_ascii=False)}

D3 SECOND OPINION (null if not triggered):
{json.dumps(second, ensure_ascii=False)}

HARNESS PROTOCOL COMPLETION:
{json.dumps(completion, ensure_ascii=False)}

Apply the action sufficiency gate. A resolved COEXISTING/INTERACTING model
relation may coexist with DEFER_ACTION. A low-regret action may be chosen across
unresolved models without pretending the causal structure is CHOOSE. If no
feasible discriminator exists, say so rather than inventing one.
"""
    final = call_json("E-final", final_prompt, final_schema)
    ledger.complete("E1")
    ledger.complete("E2")
    ledger.complete("E3")
    # Protocol completion is an execution fact; enforce it mechanically after E.
    final["case_id"] = case_id
    final["protocol_completion"] = ledger.completion_object()
    _write(run_dir, "protocol-ledger.json", final["protocol_completion"])
    _write(run_dir, "final-v0.2.json", final)
    return final
