#!/usr/bin/env python3
"""Resumable Gemini-API technical-pilot runner.

This runner is intentionally separate from the manual browser pilot. It exists
to validate the automated stateless runtime and, in particular, genuine
cg-full execution with explicit stage allowlists.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ADAPTER = Path(__file__).with_name("gemini_api_adapter.py")
MODEL = "gemini-3.5-flash"
SETTINGS = {"temperature": 0.2, "maxOutputTokens": 8192}
MIN_CALL_INTERVAL = 13.0  # Free tier currently exposes 5 RPM.


class QuotaStop(RuntimeError):
    pass


_last_call_at = 0.0


def sanitized_schema(value: Any) -> Any:
    """Keep a conservative subset accepted by Gemini responseSchema."""
    if isinstance(value, list):
        return [sanitized_schema(x) for x in value]
    if not isinstance(value, dict):
        return value
    drop = {
        "$schema",
        "title",
        "description",
        "additionalProperties",
        "minLength",
        "pattern",
        "allOf",
        "if",
        "then",
    }
    result = {
        k: sanitized_schema(v)
        for k, v in value.items()
        if k not in drop
    }
    schema_type = result.get("type")
    if isinstance(schema_type, list):
        non_null = [item for item in schema_type if item != "null"]
        has_null = len(non_null) != len(schema_type)
        if has_null and len(non_null) == 1:
            result["type"] = non_null[0]
            result["nullable"] = True
        else:
            # Gemini responseSchema does not accept JSON-Schema union types.
            # Fail closed instead of silently changing a non-null union.
            raise ValueError(
                "Gemini responseSchema cannot represent union type "
                f"{schema_type!r}"
            )
    if "enum" in result and "type" not in result:
        enum_values = result["enum"]
        non_null = [item for item in enum_values if item is not None]
        nullable = len(non_null) != len(enum_values)
        inferred: str | None = None
        if non_null and all(isinstance(item, str) for item in non_null):
            inferred = "string"
        elif non_null and all(
            isinstance(item, bool) for item in non_null
        ):
            inferred = "boolean"
        elif non_null and all(
            isinstance(item, int) and not isinstance(item, bool)
            for item in non_null
        ):
            inferred = "integer"
        elif non_null and all(
            isinstance(item, (int, float)) and not isinstance(item, bool)
            for item in non_null
        ):
            inferred = "number"
        if inferred is None:
            raise ValueError(
                "Cannot infer Gemini responseSchema type for enum "
                f"{enum_values!r}"
            )
        result["type"] = inferred
        if nullable:
            result["nullable"] = True
    return result


def validate_primary(case_id: str, run_dir: Path) -> None:
    final_path = run_dir / "final.json"
    validator = Path(__file__).with_name("validate_final.py")
    case_dir = ROOT / "evals" / "cases" / "pilot" / case_id
    proc = subprocess.run(
        [
            sys.executable,
            str(validator),
            str(final_path),
            "--case",
            str(case_dir),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    diagnostic = (proc.stdout + proc.stderr).strip()
    (run_dir / "primary-validation.txt").write_text(
        diagnostic + "\n", encoding="utf-8"
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "primary validation failed; calibration is forbidden: "
            + diagnostic
        )


def call_adapter(
    run_dir: Path,
    stage: str,
    *,
    prompt: str,
    schema: dict | None = None,
    model: str = MODEL,
    settings: dict | None = None,
) -> dict:
    """Call once, persist envelope/raw output, and resume from disk if present."""
    global _last_call_at
    response_path = run_dir / "working" / f"{stage}.response.json"
    raw_path = run_dir / "working" / f"{stage}.raw.txt"
    request_path = run_dir / "working" / f"{stage}.request.json"
    if response_path.exists():
        existing = json.loads(response_path.read_text(encoding="utf-8-sig"))
        if schema is None:
            return existing
        try:
            json.loads(existing.get("raw_text", ""))
            return existing
        except json.JSONDecodeError:
            finish = existing.get("metadata", {}).get("finish_reason")
            if finish != "MAX_TOKENS":
                return existing
            # Older runner versions persisted truncated structured responses as
            # canonical stage output. Preserve them, then retry just this stage.
            for path in (request_path, response_path, raw_path):
                if path.exists():
                    archived = path.with_name(
                        path.name + ".attempt1-max-tokens"
                    )
                    path.replace(archived)

    request = {
        "request_id": f"{run_dir.name}-{stage}",
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "settings": dict(settings or SETTINGS),
        "response_schema": sanitized_schema(schema) if schema else None,
        "tools_enabled": False,
        "retrieval_enabled": False,
    }
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_path.write_text(
        json.dumps(request, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    delay = MIN_CALL_INTERVAL - (time.monotonic() - _last_call_at)
    if delay > 0:
        time.sleep(delay)

    attempts = 0
    while True:
        attempts += 1
        proc = subprocess.run(
            [sys.executable, str(ADAPTER)],
            input=json.dumps(request, ensure_ascii=False),
            text=True,
            capture_output=True,
            check=False,
            timeout=180,
        )
        _last_call_at = time.monotonic()
        if proc.returncode == 0:
            envelope = json.loads(proc.stdout)
            envelope["harness_attempts"] = attempts
            raw_text = envelope.get("raw_text", "")
            if schema is not None:
                try:
                    json.loads(raw_text)
                except json.JSONDecodeError as exc:
                    finish = envelope.get("metadata", {}).get("finish_reason")
                    attempt_response = response_path.with_name(
                        response_path.name
                        + f".attempt{attempts}-invalid-structured"
                    )
                    attempt_raw = raw_path.with_name(
                        raw_path.name
                        + f".attempt{attempts}-invalid-structured"
                    )
                    attempt_response.write_text(
                        json.dumps(envelope, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8",
                    )
                    attempt_raw.write_text(raw_text, encoding="utf-8")
                    if finish == "MAX_TOKENS" and attempts < 3:
                        current = int(
                            request["settings"].get("maxOutputTokens", 8192)
                        )
                        request["settings"]["maxOutputTokens"] = min(
                            max(current * 2, 8192), 32768
                        )
                        request_path.write_text(
                            json.dumps(request, indent=2, ensure_ascii=False)
                            + "\n",
                            encoding="utf-8",
                        )
                        continue
                    raise RuntimeError(
                        "structured response is invalid JSON "
                        f"(finish={finish!r}, line={exc.lineno}, "
                        f"column={exc.colno}): {exc.msg}"
                    )
            response_path.write_text(
                json.dumps(envelope, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            raw_path.write_text(raw_text, encoding="utf-8")
            return envelope

        error = proc.stderr.strip()
        if "HTTP 429" in error or "RESOURCE_EXHAUSTED" in error:
            (run_dir / "quota-stop.txt").write_text(error + "\n", encoding="utf-8")
            raise QuotaStop(error)
        if ("HTTP 503" in error or "UNAVAILABLE" in error) and attempts < 3:
            time.sleep(15 * attempts)
            continue
        raise RuntimeError(error or f"adapter failed at stage {stage}")


def parse_structured(run_dir: Path, stage: str, envelope: dict) -> dict:
    parsed_path = run_dir / "working" / f"{stage}.json"
    if parsed_path.exists():
        return json.loads(parsed_path.read_text(encoding="utf-8-sig"))
    raw = envelope.get("raw_text", "")
    data = json.loads(raw)
    parsed_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return data


def case_material(case_id: str) -> str:
    case_dir = ROOT / "evals" / "cases" / "pilot" / case_id
    sections = [(case_dir / "prompt.md").read_text(encoding="utf-8")]
    for path in sorted((case_dir / "evidence").iterdir()):
        if path.is_file():
            sections.append(
                f"## Evidence {path.name[:3]}\n\n"
                + path.read_text(encoding="utf-8")
            )
    return "\n\n".join(x.strip() for x in sections)


def decision_contract(case_id: str) -> str:
    if case_id == "P01":
        return (
            "Decision: identify the justified cause of the checkout 503s and "
            "the best immediate restoration action. Constraints: restore "
            "quickly; no data-destructive action; rollback/config correction "
            "is reversible; no web; supplied evidence only. Error cost: "
            "prolonged outage or harmful repair. Analysis budget: 12 model "
            "calls, at most two corrective cycles."
        )
    if case_id == "P02":
        return (
            "Decision: determine whether current evidence justifies a unique "
            "cause for TLS handshake timeouts and choose the safest immediate "
            "action. Constraints: unaffected workers carry traffic; untested "
            "production rollback during settlement is disruptive; read-only "
            "diagnostics and isolated canaries are allowed; no web; supplied "
            "evidence only. Error cost: disrupting payment settlement or "
            "committing to the wrong mechanism. Analysis budget: 12 model "
            "calls, at most two corrective cycles."
        )
    raise ValueError(case_id)


def mandates(case_id: str) -> list[str]:
    if case_id == "P01":
        return [
            "Examine deployment/configuration changes and their direct causal chain to the observed failure.",
            "Examine dependency, DNS, database-proxy, and network-path mechanisms independently of deployment intent.",
            "Examine application/runtime/resource and other causally distinct alternatives, including what the evidence rules out.",
        ]
    if case_id == "P02":
        return [
            "Examine mechanisms introduced by the TLS client-library change, including handshake behavior and compatibility.",
            "Examine mechanisms introduced by the outbound firewall/policy migration after TCP establishment.",
            "Examine causally distinct external-endpoint, interaction, timing, and observability explanations not reducible to either named change alone.",
        ]
    raise ValueError(case_id)


SEARCH_SCHEMA = {
    "type": "object",
    "required": ["models"],
    "properties": {
        "models": {
            "type": "array",
            "items": {
                "type": "object",
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

SCREEN_SCHEMA = {
    "type": "object",
    "required": ["evaluations"],
    "properties": {
        "evaluations": {
            "type": "array",
            "items": {
                "type": "object",
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
                },
            },
        }
    },
}

MAP_SCHEMA = {
    "type": "object",
    "required": ["families", "relations", "boundary_critic_needed", "boundary_issue"],
    "properties": {
        "families": {
            "type": "array",
            "items": {
                "type": "object",
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

DOSSIER_SCHEMA = {
    "type": "object",
    "required": [
        "candidate_id",
        "mechanism",
        "assumptions",
        "predictions",
        "disconfirming_observations",
        "decision_consequence",
        "identification_weaknesses",
        "error_cost_reversibility",
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
    },
}

SECOND_SCHEMA = {
    "type": "object",
    "required": ["decisive_inference", "unsupported_additions", "unresolved_issue", "recommendation"],
    "properties": {
        "decisive_inference": {"type": "string"},
        "unsupported_additions": {"type": "array", "items": {"type": "string"}},
        "unresolved_issue": {"type": "string"},
        "recommendation": {"type": "string"},
    },
}


def neutral_candidates(search_outputs: list[dict]) -> list[dict]:
    result = []
    counter = 1
    for output in search_outputs:
        for model in output.get("models", []):
            item = dict(model)
            item["id"] = f"H{counter:02d}"
            result.append(item)
            counter += 1
    return result


def choose_finalists(candidates: list[dict], screen: dict, mapping: dict) -> list[dict]:
    evals = {x["candidate_id"]: x for x in screen.get("evaluations", [])}
    family_by_candidate: dict[str, str] = {}
    for family in mapping.get("families", []):
        for cid in family.get("candidate_ids", []):
            family_by_candidate[cid] = family.get("family_id", cid)

    support_rank = {"STRONG": 3, "MIXED": 2, "WEAK": 1}
    completeness_rank = {"CHAIN PRESENT": 3, "PARTIAL": 2, "ASSERTION ONLY": 1}
    viable = []
    for c in candidates:
        ev = evals.get(c["id"])
        if not ev or ev.get("contract_fit") == "FAIL":
            continue
        if ev.get("evidence_support") not in {"STRONG", "MIXED"}:
            continue
        if ev.get("causal_completeness") == "ASSERTION ONLY":
            continue
        score = (
            support_rank.get(ev.get("evidence_support"), 0),
            completeness_rank.get(ev.get("causal_completeness"), 0),
            1 if ev.get("discriminability") == "HIGH" else 0,
        )
        viable.append((score, c))
    viable.sort(key=lambda x: x[0], reverse=True)

    chosen = []
    seen_families = set()
    for _, c in viable:
        family = family_by_candidate.get(c["id"], c["id"])
        if family in seen_families:
            continue
        chosen.append(c)
        seen_families.add(family)
        if len(chosen) == 3:
            break
    if not chosen:
        # Fail-soft for a pilot: retain the strongest non-FAIL candidate rather
        # than inventing a finalist. D2 still applies the insufficiency gate.
        for c in candidates:
            ev = evals.get(c["id"])
            if ev and ev.get("contract_fit") != "FAIL":
                chosen = [c]
                break
    return chosen


def full_mode(case_id: str, run_dir: Path, output_schema: dict) -> dict:
    material = case_material(case_id)
    contract = decision_contract(case_id)
    framing = (
        "Framing check: keep the decision on causal attribution and immediate "
        "operational action; do not substitute confidence, verbosity, or branch "
        "agreement for evidence. No outside evidence is allowed in this case."
    )
    search_outputs = []
    for idx, mandate in enumerate(mandates(case_id), start=1):
        prompt = f"""You are an isolated Convergence Guard Phase B search worker.

AUTHORIZED INPUTS ONLY:

PUBLIC EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

FRAMING:
{framing}

YOUR MANDATE:
{mandate}

Do not infer or discuss other workers. Generate 2-4 causally distinct models
within your mandate, or an empty models list if none is viable. For every model
give the causal chain, necessary conditions, observable predictions, implied
action, disconfirming evidence, causal-identification threats, and conflicts
with supplied evidence. Do not browse or introduce outside facts.
"""
        env = call_adapter(
            run_dir, f"search-{idx}", prompt=prompt, schema=SEARCH_SCHEMA
        )
        search_outputs.append(parse_structured(run_dir, f"search-{idx}", env))

    candidates = neutral_candidates(search_outputs)
    candidates_path = run_dir / "working" / "neutral-candidates.json"
    candidates_path.write_text(
        json.dumps(candidates, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    screen_prompt = f"""You are the fresh Convergence Guard C1 contract screener.
You have not seen branch identities or any causal-map result.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

NEUTRAL CANDIDATES:
{json.dumps(candidates, ensure_ascii=False)}

Evaluate every candidate exactly once using the required categorical fields.
Do not aggregate into a score and do not browse.
"""
    screen_env = call_adapter(
        run_dir, "c1-screen", prompt=screen_prompt, schema=SCREEN_SCHEMA
    )
    screen = parse_structured(run_dir, "c1-screen", screen_env)

    mapper_candidates = [
        {
            "id": c["id"],
            "claim": c["claim"],
            "mechanism": c["mechanism"],
            "necessary_conditions": c["necessary_conditions"],
            "predictions": c["predictions"],
            "implied_action": c["implied_action"],
            "disconfirming_evidence": c["disconfirming_evidence"],
        }
        for c in candidates
    ]
    map_prompt = f"""You are the fresh Convergence Guard C2 blind causal mapper.
You must not infer or invent screening outcomes, worker identities, rankings,
danger flags, or coordinator preferences.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

NEUTRAL CANDIDATE CONTENT:
{json.dumps(mapper_candidates, ensure_ascii=False)}

Map near-duplicates into causal families without counting duplicates as
corroboration. Record decision-relevant relations. Set boundary_critic_needed
only if a disputed merge/relation could materially change the action.
"""
    map_env = call_adapter(run_dir, "c2-map", prompt=map_prompt, schema=MAP_SCHEMA)
    mapping = parse_structured(run_dir, "c2-map", map_env)

    finalists = choose_finalists(candidates, screen, mapping)
    (run_dir / "working" / "finalists.json").write_text(
        json.dumps(finalists, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    dossiers = []
    for idx, finalist in enumerate(finalists, start=1):
        prompt = f"""You are an isolated Convergence Guard D1 dossier worker.
You receive one finalist only and must not compare it with unseen rivals.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

ONE FINALIST:
{json.dumps(finalist, ensure_ascii=False)}

Make the model explicit without changing its mechanism. Identify load-bearing
assumptions, predictions, concrete disconfirming observations, decision
consequence, causal-identification weaknesses, and cost/reversibility of being
wrong. Do not browse or add outside facts.
"""
        env = call_adapter(
            run_dir, f"dossier-{idx}", prompt=prompt, schema=DOSSIER_SCHEMA
        )
        dossiers.append(parse_structured(run_dir, f"dossier-{idx}", env))

    adjudication_schema = {
        "type": "object",
        "required": [
            "final",
            "second_opinion_needed",
            "second_opinion_reason",
            "sensitivity_summary",
            "shared_bias_summary",
            "collision_summary",
        ],
        "properties": {
            "final": sanitized_schema(output_schema),
            "second_opinion_needed": {"type": "boolean"},
            "second_opinion_reason": {"type": "string"},
            "sensitivity_summary": {"type": "string"},
            "shared_bias_summary": {"type": "string"},
            "collision_summary": {"type": "string"},
        },
    }
    adjudicate_prompt = f"""You are the fresh Convergence Guard D2 slate-level
adjudicator and Phase E action adjudicator. You did not author search,
screening, mapping, or dossiers. You are not given screening ranks or a
coordinator favorite.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

NEUTRAL FINALIST DOSSIERS:
{json.dumps(dossiers, ensure_ascii=False)}

Perform assumption sensitivity, shared-bias audit, and pairwise collision only
where actions conflict. Separate model judgment from decision judgment and
apply the evidence-sufficiency gate. The nested final object must use case_id
{case_id} and the common eval schema. Set second_opinion_needed=true only when
the protocol trigger is genuinely met (cycle/repeated undetermined, weak
apparent winner, serious shared blind spot, unusual irreversibility, or an
unexplained sharp conflict). Do not browse or add outside facts.
"""
    adj_env = call_adapter(
        run_dir,
        "d2-adjudication",
        prompt=adjudicate_prompt,
        schema=adjudication_schema,
    )
    adjudication = parse_structured(run_dir, "d2-adjudication", adj_env)

    final = adjudication["final"]
    if adjudication.get("second_opinion_needed"):
        second_prompt = f"""You are the fresh Convergence Guard D3 independent
second-opinion reviewer. Reconstruct the decisive inference without seeing any
coordinator favorite or screening rank.

RAW EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

NEUTRAL CANDIDATE CLAIMS:
{json.dumps([{'id': c['id'], 'claim': c['claim']} for c in finalists], ensure_ascii=False)}

DOSSIERS TO AUDIT FOR ADDED PREMISES:
{json.dumps(dossiers, ensure_ascii=False)}

Audit unsupported additions and state the decisive unresolved issue, if any.
Do not browse.
"""
        second_env = call_adapter(
            run_dir, "d3-second-opinion", prompt=second_prompt, schema=SECOND_SCHEMA
        )
        second = parse_structured(run_dir, "d3-second-opinion", second_env)
        reconcile_prompt = f"""You are the Convergence Guard final coordinator.
The primary adjudication is frozen, and an independent second opinion was
triggered. Reconcile them using only the supplied evidence and contract. Do not
upgrade uncertainty because agents agree.

EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

PRIMARY ADJUDICATED FINAL:
{json.dumps(final, ensure_ascii=False)}

INDEPENDENT SECOND OPINION:
{json.dumps(second, ensure_ascii=False)}

Return the final normalized answer for case {case_id}. Do not browse.
"""
        rec_env = call_adapter(
            run_dir, "e-reconcile", prompt=reconcile_prompt, schema=output_schema
        )
        final = parse_structured(run_dir, "e-reconcile", rec_env)

    final_path = run_dir / "final.json"
    final_path.write_text(
        json.dumps(final, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return final


def calibration(case_id: str, run_dir: Path, final: dict, schema: dict) -> dict:
    cal_path = run_dir / "calibration.json"
    if cal_path.exists():
        return json.loads(cal_path.read_text(encoding="utf-8-sig"))
    claims = json.loads(
        (ROOT / "evals" / "calibration" / "pilot" / f"{case_id}.json").read_text(
            encoding="utf-8"
        )
    )
    prompt = f"""The primary answer is frozen and must not be revised.

PUBLIC CASE:
{case_material(case_id)}

FROZEN PRIMARY:
{json.dumps(final, ensure_ascii=False)}

For each claim below, give your probability from 0 to 1 that the claim is true
using only the supplied case evidence:
{json.dumps(claims['claims'], ensure_ascii=False)}

Return the calibration object for case_id {case_id}.
"""
    env = call_adapter(
        run_dir,
        "calibration",
        prompt=prompt,
        schema=schema,
        settings={"temperature": 0, "maxOutputTokens": 1024},
    )
    data = parse_structured(run_dir, "calibration", env)
    cal_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=["P01", "P02"], required=True)
    parser.add_argument("--mode", choices=["cg-full"], default="cg-full")
    args = parser.parse_args()

    output_schema = json.loads(
        (ROOT / "evals" / "protocol" / "OUTPUT-SCHEMA.json").read_text(
            encoding="utf-8"
        )
    )
    calibration_schema = json.loads(
        (ROOT / "evals" / "protocol" / "CALIBRATION-SCHEMA.json").read_text(
            encoding="utf-8"
        )
    )
    run_dir = (
        ROOT
        / "evals"
        / "runs"
        / "api-pilot"
        / args.case
        / "r1"
        / args.mode
    )
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = run_dir / "manifest.json"
    manifest = {
        "run_id": f"{args.case}-r1-{args.mode}-api",
        "case_id": args.case,
        "mode": args.mode,
        "repeat": 1,
        "eval_version": "0.1-api-pilot",
        "model": MODEL,
        "model_settings": SETTINGS,
        "status": "running",
        "isolation_preflight": "PASS",
        "preflight_artifact": "evals/preflight/gemini-api-2026-10-07.json",
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    try:
        final = full_mode(args.case, run_dir, output_schema)
        validate_primary(args.case, run_dir)
        calibration(args.case, run_dir, final, calibration_schema)
    except QuotaStop:
        manifest["status"] = "paused_quota"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"PAUSED_QUOTA {manifest['run_id']}")
        return 75
    except RuntimeError as exc:
        manifest["status"] = "invalid"
        manifest["error"] = str(exc)
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"INVALID {manifest['run_id']}: {exc}", file=sys.stderr)
        return 1

    manifest["status"] = "complete"
    manifest.pop("error", None)
    (run_dir / "quota-stop.txt").unlink(missing_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"COMPLETE {manifest['run_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
