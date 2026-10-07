#!/usr/bin/env python3
"""Resumable local LM Studio comparative pilot for all four eval modes."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

from normalize_final import NORMALIZATION_VERSION, normalize_artifact


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL_RUNNER = HERE / "api_pilot_runner.py"
LM_ADAPTER = HERE / "lmstudio_adapter.py"
MODEL = "gemma-4-12b-it"
SETTINGS = {"temperature": 0.2, "maxOutputTokens": 8192}
PREFLIGHT = ROOT / "evals" / "preflight" / "lmstudio-local-2026-10-07.json"
MODES = (
    "single-context",
    "shared-context-multi-agent",
    "cg-reduced",
    "cg-full",
)


def load_full_runner():
    spec = importlib.util.spec_from_file_location("cg_api_runner", FULL_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load api_pilot_runner.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ADAPTER = LM_ADAPTER
    module.MODEL = MODEL
    module.SETTINGS = dict(SETTINGS)
    module.MIN_CALL_INTERVAL = 0.0
    return module


CG = load_full_runner()
_last_call_at = 0.0


def local_call_adapter(
    run_dir: Path,
    stage: str,
    *,
    prompt: str,
    schema: dict | None = None,
    model: str = MODEL,
    settings: dict | None = None,
) -> dict:
    """LM Studio call path preserving the native JSON Schema verbatim."""
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
            if finish != "length":
                return existing
            for path in (request_path, response_path, raw_path):
                if path.exists():
                    path.replace(
                        path.with_name(path.name + ".attempt1-max-tokens")
                    )

    request = {
        "request_id": f"{run_dir.name}-{stage}",
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "settings": dict(settings or SETTINGS),
        "response_schema": schema,
        "tools_enabled": False,
        "retrieval_enabled": False,
    }
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_path.write_text(
        json.dumps(request, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    attempts = 0
    while True:
        attempts += 1
        proc = subprocess.run(
            [sys.executable, str(LM_ADAPTER)],
            input=json.dumps(request, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
            timeout=900,
        )
        _last_call_at = time.monotonic()
        if proc.returncode != 0:
            raise RuntimeError(
                proc.stderr.strip() or f"LM Studio adapter failed at {stage}"
            )
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
                if finish == "length" and attempts < 3:
                    current = int(
                        request["settings"].get("maxOutputTokens", 8192)
                    )
                    request["settings"]["maxOutputTokens"] = min(
                        max(current * 2, 8192), 32768
                    )
                    request_path.write_text(
                        json.dumps(request, indent=2, ensure_ascii=False) + "\n",
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


# Full Mode and calibration reuse the protocol graph from api_pilot_runner, but
# all model calls go through the local native-schema/UTF-8 adapter above.
CG.call_adapter = local_call_adapter


def output_schema() -> dict[str, Any]:
    return json.loads(
        (ROOT / "evals" / "protocol" / "OUTPUT-SCHEMA.json").read_text(
            encoding="utf-8"
        )
    )


def calibration_schema() -> dict[str, Any]:
    return json.loads(
        (ROOT / "evals" / "protocol" / "CALIBRATION-SCHEMA.json").read_text(
            encoding="utf-8"
        )
    )


def mode_instruction(mode: str) -> str:
    return (
        ROOT / "evals" / "protocol" / "modes" / f"{mode}.md"
    ).read_text(encoding="utf-8")


def call_json(run_dir: Path, stage: str, prompt: str, schema: dict) -> dict:
    env = CG.call_adapter(
        run_dir,
        stage,
        prompt=prompt,
        schema=schema,
        model=MODEL,
        settings=SETTINGS,
    )
    return CG.parse_structured(run_dir, stage, env)


def call_text(run_dir: Path, stage: str, prompt: str) -> str:
    env = CG.call_adapter(
        run_dir,
        stage,
        prompt=prompt,
        schema=None,
        model=MODEL,
        settings={"temperature": 0.2, "maxOutputTokens": 1200},
    )
    return env.get("raw_text", "")


def single_context(case_id: str, run_dir: Path, schema: dict) -> dict:
    prompt = f"""This is a controlled evaluation run.
Use only the supplied case material. Do not browse or add outside facts.

MODE INSTRUCTION:
{mode_instruction("single-context")}

PARTICIPANT-VISIBLE CASE:
{CG.case_material(case_id)}

Return exactly the normalized final-answer object for case_id {case_id}.
"""
    return call_json(run_dir, "primary", prompt, schema)


def shared_context(case_id: str, run_dir: Path, schema: dict) -> dict:
    material = CG.case_material(case_id)
    mode = mode_instruction("shared-context-multi-agent")
    journal: list[tuple[str, str]] = []
    analyst_prompts = [
        "Analyze the case from first principles. Identify plausible causal explanations, evidence for/against them, uncertainty, action implications, and useful next tests.",
        "Review the case plus the existing shared journal. Extend, challenge, or correct it. Do not merely agree; look for missing alternatives and weak inferences.",
        "Review the full shared journal. Stress-test the leading explanations, distinguish model judgment from action judgment, and identify what remains unresolved.",
    ]
    for idx, instruction in enumerate(analyst_prompts, start=1):
        prior = "\n\n".join(
            f"### Analyst {name}\n{text}" for name, text in journal
        ) or "(empty)"
        prompt = f"""This is a controlled evaluation run.
Use only the supplied case material. Do not browse or add outside facts.

MODE INSTRUCTION:
{mode}

PARTICIPANT-VISIBLE CASE:
{material}

SHARED JOURNAL SO FAR:
{prior}

YOUR PASS:
{instruction}

Write a concise analytical journal entry, not the normalized final JSON.
"""
        text = call_text(run_dir, f"analyst-{idx}", prompt)
        journal.append((chr(64 + idx), text))

    full_journal = "\n\n".join(
        f"### Analyst {name}\n{text}" for name, text in journal
    )
    synth_prompt = f"""This is a controlled evaluation run.
Use only the supplied case material and shared journal. Do not browse or add
outside facts.

MODE INSTRUCTION:
{mode}

PARTICIPANT-VISIBLE CASE:
{material}

SHARED JOURNAL:
{full_journal}

Act as the synthesizer. Return exactly the normalized final-answer object for
case_id {case_id}. Do not mention the evaluation design.
"""
    return call_json(run_dir, "synth", synth_prompt, schema)


def reduced_context(case_id: str, run_dir: Path, schema: dict) -> dict:
    reduced_protocol = (
        ROOT / "convergence-guard" / "references" / "reduced-mode.md"
    ).read_text(encoding="utf-8")
    prompt = f"""This is a controlled evaluation run.
Use only the supplied case material. Do not browse or add outside facts.

TREATMENT:
Convergence Guard — Reduced Mode (no independent worker isolation)

REDUCED MODE PROTOCOL:
{reduced_protocol}

DECISION CONTRACT:
{CG.decision_contract(case_id)}

PARTICIPANT-VISIBLE CASE:
{CG.case_material(case_id)}

Execute the Reduced Mode workflow in this one effective context. Preserve the
reasoning shape in the protocol, but do not claim independent-worker or blind
stage guarantees. Return exactly the normalized final-answer JSON object for
case_id {case_id}.
"""
    return call_json(run_dir, "primary", prompt, schema)


def validate_and_calibrate(case_id: str, run_dir: Path, final: dict) -> int:
    raw_path = run_dir / "final.raw.json"
    raw_path.write_text(
        json.dumps(final, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    final_path = run_dir / "final.json"
    audit_path = run_dir / "normalization.json"
    repair_count = normalize_artifact(raw_path, final_path, audit_path)
    normalized = json.loads(final_path.read_text(encoding="utf-8-sig"))
    CG.validate_primary(case_id, run_dir)
    CG.calibration(case_id, run_dir, normalized, calibration_schema())
    return repair_count


def run_one(case_id: str, mode: str) -> int:
    run_dir = ROOT / "evals" / "runs" / "local-pilot" / case_id / "r1" / mode
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = run_dir / "manifest.json"
    full_preflight_status = "NOT_APPLICABLE"
    if mode == "cg-full":
        if not PREFLIGHT.exists():
            raise RuntimeError(f"missing local isolation preflight: {PREFLIGHT}")
        preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8-sig"))
        if preflight.get("overall") != "PASS" or preflight.get("cg_full_enabled") is not True:
            raise RuntimeError("local isolation preflight does not permit cg-full")
        full_preflight_status = "PASS"
    manifest = {
        "run_id": f"{case_id}-r1-{mode}-local",
        "case_id": case_id,
        "mode": mode,
        "repeat": 1,
        "eval_version": "0.1-local-pilot",
        "runtime": "LM Studio OpenAI-compatible API",
        "model": MODEL,
        "model_settings": SETTINGS,
        "normalization_version": NORMALIZATION_VERSION,
        "normalization_repairs": 0,
        "status": "running",
        "isolation_preflight": full_preflight_status,
        "preflight_artifact": (
            "evals/preflight/lmstudio-local-2026-10-07.json"
            if mode == "cg-full"
            else None
        ),
        "cost_usd": 0.0,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    try:
        schema = output_schema()
        if mode == "single-context":
            final = single_context(case_id, run_dir, schema)
        elif mode == "shared-context-multi-agent":
            final = shared_context(case_id, run_dir, schema)
        elif mode == "cg-reduced":
            final = reduced_context(case_id, run_dir, schema)
        elif mode == "cg-full":
            final = CG.full_mode(case_id, run_dir, schema)
        else:
            raise ValueError(mode)
        manifest["normalization_repairs"] = validate_and_calibrate(
            case_id, run_dir, final
        )
    except Exception as exc:
        manifest["status"] = "invalid"
        manifest["error"] = f"{type(exc).__name__}: {exc}"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"INVALID {manifest['run_id']}: {exc}", file=sys.stderr)
        return 1
    manifest["status"] = "complete"
    manifest.pop("error", None)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"COMPLETE {manifest['run_id']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=["P01", "P02", "all"], default="all")
    parser.add_argument("--mode", choices=[*MODES, "all"], default="all")
    args = parser.parse_args()
    cases = ["P01", "P02"] if args.case == "all" else [args.case]
    modes = list(MODES) if args.mode == "all" else [args.mode]
    failures = 0
    for case_id in cases:
        for mode in modes:
            failures += int(run_one(case_id, mode) != 0)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
