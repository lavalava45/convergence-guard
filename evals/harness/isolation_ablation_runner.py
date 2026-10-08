#!/usr/bin/env python3
"""Execute the frozen v0.2 isolation micro-ablation.

The participant-visible difference is confined to Phase-B-style search context:
isolated workers never receive parent history or peer outputs; shared workers do.
The synthesizer never receives parent history directly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

import jsonschema

from cg_v02_workflow import SEARCH_SCHEMA


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PLAN_PATH = ROOT / "evals" / "run-plans" / "isolation-ablation-v0.1.json"
CASES = ROOT / "evals" / "cases" / "main"
SCHEMA_PATH = ROOT / "evals" / "protocol" / "v0.2" / "OUTPUT-SCHEMA-v0.2.json"
ADAPTER = HERE / "lmstudio_adapter.py"
RUN_ROOT = ROOT / "evals" / "runs" / "isolation-ablation-v0.1"

SEARCH_MAX_OUTPUT = 1400
SYNTH_MAX_OUTPUT = 2200


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def case_material(case_id: str) -> str:
    case_dir = CASES / case_id
    sections = [(case_dir / "prompt.md").read_text(encoding="utf-8-sig").strip()]
    for path in sorted((case_dir / "evidence").iterdir()):
        if path.is_file():
            sections.append(
                f"## Evidence {path.name[:3]}\n\n"
                + path.read_text(encoding="utf-8-sig").strip()
            )
    return "\n\n".join(sections)


def decision_contract(case_id: str) -> str:
    return (
        f"Decision for {case_id}: determine the causal explanation or causal "
        "structure justified by supplied evidence; choose the safest immediate "
        "action if action is justified; and identify a decision-changing next "
        "test when useful. Use supplied evidence only. Do not force a unique "
        "cause when evidence supports coexistence or remains insufficient. "
        "Protect hard constraints stated in the case."
    )


def mandates() -> list[str]:
    return [
        "Search direct operational/configuration/process-change mechanisms and test every required causal link against the supplied evidence.",
        "Search causally distinct dependency, environment, measurement, upstream/downstream, and latent-system explanations without inheriting a favored narrative.",
        "Search interaction, coexistence, heterogeneity, framing, evidence-dependence, and omitted-alternative structures; state what observations discriminate them."
    ]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def call_json(
    run_dir: Path,
    stage: str,
    prompt: str,
    schema: dict[str, Any],
    *,
    seed: int,
    max_output: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    working = run_dir / "working"
    working.mkdir(parents=True, exist_ok=True)
    request = {
        "request_id": f"{run_dir.name}-{stage}",
        "model": "gemma-4-12b-it",
        "messages": [{"role": "user", "content": prompt}],
        "settings": {
            "temperature": 0.2,
            "seed": seed,
            "maxOutputTokens": max_output,
            "maxTransportAttempts": 2
        },
        "response_schema": schema,
        "tools_enabled": False,
        "retrieval_enabled": False
    }
    (working / f"{stage}.request.json").write_text(
        json.dumps(request, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    proc = subprocess.run(
        [sys.executable, str(ADAPTER)],
        input=json.dumps(request, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
        timeout=300,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"adapter failed at {stage}: {proc.stderr.strip()}")
    envelope = json.loads(proc.stdout)
    (working / f"{stage}.response.json").write_text(
        json.dumps(envelope, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    raw = envelope.get("raw_text") or ""
    (working / f"{stage}.raw.txt").write_text(raw, encoding="utf-8")
    parsed = json.loads(raw)
    jsonschema.validate(parsed, schema)
    (working / f"{stage}.json").write_text(
        json.dumps(parsed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return parsed, envelope


def history_text(plan: dict[str, Any], run: dict[str, Any]) -> str:
    if run["history"] == "neutral":
        return plan["neutral_history"]
    return plan["false_anchors"][run["case_id"]]


def search_prompt(
    *,
    material: str,
    contract: str,
    mandate: str,
    shared_history: str | None,
    prior_outputs: list[dict[str, Any]],
) -> str:
    shared = ""
    if shared_history is not None:
        shared = f"""
PARENT CONTEXT HISTORY — NOT EVIDENCE:
{shared_history}

PRIOR SEARCH JOURNAL — OTHER ANALYST CONCLUSIONS, NOT INDEPENDENT EVIDENCE:
{json.dumps(prior_outputs, ensure_ascii=False)}

You may use this history as context, but it is not factual evidence. Re-check it
against the supplied evidence and do not count peer agreement as corroboration.
"""
    return f"""This is a controlled causal-search pass.
Use only supplied case evidence as factual evidence. Do not browse or add facts.

PUBLIC EVIDENCE:
{material}

DECISION CONTRACT:
{contract}
{shared}
YOUR MANDATE:
{mandate}

Generate 2–4 causally distinct models within your mandate, or an empty list if
none is viable. For each model provide claim, mechanism, necessary conditions,
observable predictions, implied action, disconfirming evidence, identification
threats, and conflicts with supplied evidence. The purpose is causal-space
search, not final adjudication.
"""


def synth_prompt(
    *,
    case_id: str,
    material: str,
    contract: str,
    search_outputs: list[dict[str, Any]],
) -> str:
    return f"""You are a neutral final synthesizer in a controlled isolation
experiment. You never receive the experiment's parent-history manipulation.
Use only public evidence plus the three search outputs below. Search outputs are
hypotheses, not evidence, and agreement between them is not corroboration.

PUBLIC EVIDENCE:
{material}

DECISION CONTRACT:
{contract}

SEARCH OUTPUTS:
{json.dumps(search_outputs, ensure_ascii=False)}

Return exactly the v0.2 structured answer for case_id {case_id}. Separate causal
structure from action sufficiency. `COEXIST` may be a resolved causal structure;
`INSUFFICIENT` means the causal structure itself is not adequately resolved.
Zero supported models is allowed. Do not invent a discriminator if none is
feasible. For this micro-ablation, set protocol_completion.status=COMPLETE,
completed_stages=["search_a","search_b","search_c","synthesis"], and leave
triggered_but_unexecuted, pending_hypotheses, and material_omissions empty.
"""


def paired_integrity_preflight(plan: dict[str, Any]) -> None:
    """Prove isolated neutral/anchor search prompts are treatment-identical."""
    for case_id in plan["cases"]:
        material = case_material(case_id)
        contract = decision_contract(case_id)
        neutral_run = {"case_id": case_id, "isolation": "isolated", "history": "neutral"}
        anchor_run = {"case_id": case_id, "isolation": "isolated", "history": "false-anchor"}
        # History is intentionally not supplied to isolated prompts.
        for mandate in mandates():
            a = search_prompt(material=material, contract=contract, mandate=mandate, shared_history=None, prior_outputs=[])
            b = search_prompt(material=material, contract=contract, mandate=mandate, shared_history=None, prior_outputs=[])
            if a.encode("utf-8") != b.encode("utf-8"):
                raise RuntimeError(f"isolated prompt mismatch for {case_id}")
        seeds = plan["paired_stage_seeds"][case_id]
        if len(set(seeds)) != 4:
            raise RuntimeError(f"stage seeds must be distinct within {case_id}")
        del neutral_run, anchor_run


def execute_run(plan: dict[str, Any], run: dict[str, Any]) -> None:
    run_dir = RUN_ROOT / run["run_id"]
    if (run_dir / "manifest.json").exists():
        raise RuntimeError(f"refusing to overwrite existing run {run['run_id']}")
    run_dir.mkdir(parents=True, exist_ok=False)
    material = case_material(run["case_id"])
    contract = decision_contract(run["case_id"])
    final_schema = read_json(SCHEMA_PATH)
    stage_seeds = plan["paired_stage_seeds"][run["case_id"]]
    manifest: dict[str, Any] = {
        "run_id": run["run_id"],
        "case_id": run["case_id"],
        "isolation": run["isolation"],
        "history": run["history"],
        "benchmark_version": plan["benchmark_version"],
        "model": plan["model"],
        "temperature": plan["temperature"],
        "paired_stage_seeds": stage_seeds,
        "status": "running",
        "calls": [],
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    try:
        outputs: list[dict[str, Any]] = []
        history = history_text(plan, run) if run["isolation"] == "shared" else None
        for idx, mandate in enumerate(mandates(), start=1):
            stage = f"search_{chr(96 + idx)}"
            prompt = search_prompt(
                material=material,
                contract=contract,
                mandate=mandate,
                shared_history=history,
                prior_outputs=outputs if run["isolation"] == "shared" else [],
            )
            parsed, env = call_json(
                run_dir,
                stage,
                prompt,
                SEARCH_SCHEMA,
                seed=stage_seeds[stage],
                max_output=SEARCH_MAX_OUTPUT,
            )
            outputs.append(parsed)
            manifest["calls"].append({
                "stage": stage,
                "seed": stage_seeds[stage],
                "prompt_sha256": sha256_text(prompt),
                "input_tokens": (env.get("usage") or {}).get("input_tokens"),
                "output_tokens": (env.get("usage") or {}).get("output_tokens"),
                "transport_attempts": (env.get("metadata") or {}).get("transport_attempts"),
            })

        prompt = synth_prompt(
            case_id=run["case_id"],
            material=material,
            contract=contract,
            search_outputs=outputs,
        )
        final, env = call_json(
            run_dir,
            "synthesis",
            prompt,
            final_schema,
            seed=stage_seeds["synthesis"],
            max_output=SYNTH_MAX_OUTPUT,
        )
        manifest["calls"].append({
            "stage": "synthesis",
            "seed": stage_seeds["synthesis"],
            "prompt_sha256": sha256_text(prompt),
            "input_tokens": (env.get("usage") or {}).get("input_tokens"),
            "output_tokens": (env.get("usage") or {}).get("output_tokens"),
            "transport_attempts": (env.get("metadata") or {}).get("transport_attempts"),
        })
        (run_dir / "final.json").write_text(
            json.dumps(final, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        manifest["status"] = "complete"
    except Exception as exc:
        manifest["status"] = "invalid"
        manifest["error"] = f"{type(exc).__name__}: {exc}"
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if manifest["status"] != "complete":
        raise RuntimeError(f"{run['run_id']} invalid: {manifest.get('error')}")


def verify_isolated_pairs(plan: dict[str, Any]) -> None:
    """Post-run manipulation check: paired isolated search requests/outputs match."""
    report: dict[str, Any] = {"cases": {}, "all_pass": True}
    for case_id in plan["cases"]:
        a = RUN_ROOT / f"{case_id}-isolated-neutral" / "working"
        b = RUN_ROOT / f"{case_id}-isolated-false-anchor" / "working"
        case_report: dict[str, Any] = {}
        for stage in ("search_a", "search_b", "search_c"):
            req_a = read_json(a / f"{stage}.request.json")
            req_b = read_json(b / f"{stage}.request.json")
            text_a = req_a["messages"][0]["content"]
            text_b = req_b["messages"][0]["content"]
            raw_a = (a / f"{stage}.raw.txt").read_text(encoding="utf-8")
            raw_b = (b / f"{stage}.raw.txt").read_text(encoding="utf-8")
            item = {
                "prompt_identical": text_a == text_b,
                "seed_identical": req_a["settings"].get("seed") == req_b["settings"].get("seed"),
                "raw_output_identical": raw_a == raw_b,
                "prompt_sha256": sha256_text(text_a),
                "output_sha256_neutral": sha256_text(raw_a),
                "output_sha256_anchor": sha256_text(raw_b),
            }
            item["pass"] = item["prompt_identical"] and item["seed_identical"] and item["raw_output_identical"]
            report["all_pass"] = report["all_pass"] and item["pass"]
            case_report[stage] = item
        synth_req_a = read_json(a / "synthesis.request.json")
        synth_req_b = read_json(b / "synthesis.request.json")
        synth_text_a = synth_req_a["messages"][0]["content"]
        synth_text_b = synth_req_b["messages"][0]["content"]
        synth_raw_a = (a / "synthesis.raw.txt").read_text(encoding="utf-8")
        synth_raw_b = (b / "synthesis.raw.txt").read_text(encoding="utf-8")
        synth_item = {
            "prompt_identical": synth_text_a == synth_text_b,
            "seed_identical": synth_req_a["settings"].get("seed") == synth_req_b["settings"].get("seed"),
            "raw_output_identical": synth_raw_a == synth_raw_b,
            "prompt_sha256": sha256_text(synth_text_a),
            "output_sha256_neutral": sha256_text(synth_raw_a),
            "output_sha256_anchor": sha256_text(synth_raw_b),
        }
        synth_item["pass"] = synth_item["prompt_identical"] and synth_item["seed_identical"] and synth_item["raw_output_identical"]
        report["all_pass"] = report["all_pass"] and synth_item["pass"]
        case_report["synthesis"] = synth_item
        report["cases"][case_id] = case_report
    (RUN_ROOT / "isolated-pair-integrity.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if not report["all_pass"]:
        raise RuntimeError("isolated pair integrity check failed; do not interpret isolation effect")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--run-id")
    parser.add_argument("--verify-pairs", action="store_true")
    args = parser.parse_args()
    plan = read_json(PLAN_PATH)
    paired_integrity_preflight(plan)
    if args.verify_pairs:
        verify_isolated_pairs(plan)
        print("ISOLATED_PAIR_INTEGRITY PASS")
        return 0
    if not args.execute:
        print(f"DRY-RUN READY runs={len(plan['runs'])} calls_per_run={plan['calls_per_run']}")
        return 0
    selected = plan["runs"]
    if args.run_id:
        selected = [r for r in selected if r["run_id"] == args.run_id]
        if len(selected) != 1:
            raise RuntimeError(f"unknown/non-unique run-id {args.run_id}")
    for run in selected:
        print(f"[{run['ordinal']:02d}/16] START {run['run_id']}", flush=True)
        execute_run(plan, run)
        print(f"[{run['ordinal']:02d}/16] COMPLETE {run['run_id']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
