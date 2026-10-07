#!/usr/bin/env python3
"""Frozen main-v0.1.7 standalone llama-server runner.

Default invocation is read-only/dry-run. Passing --execute is required before
any model request is issued.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
from typing import Any

from normalize_final import NORMALIZATION_VERSION, normalize_artifact


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL_RUNNER = HERE / "api_pilot_runner.py"
LM_ADAPTER = HERE / "lmstudio_adapter.py"
PLAN = ROOT / "evals" / "run-plans" / "main-v0.1.json"
CASES = ROOT / "evals" / "cases" / "main"
CALIBRATION = ROOT / "evals" / "calibration" / "main"
PREFLIGHT = ROOT / "evals" / "preflight" / "lmstudio-local-2026-10-07.json"
MODEL = "gemma-4-12b-it"
PRIMARY_TEMPERATURE = 0.2
PRIMARY_MAX_CALLS = 12
PRIMARY_MAX_OUTPUT = 32768
CAL_MAX_CALLS = 2
CAL_MAX_OUTPUT = 1024
EVAL_VERSION = "main-v0.1.7"
MAX_REQUEST_ATTEMPTS = 2
MODES = (
    "single-context",
    "shared-context-multi-agent",
    "cg-reduced",
    "cg-full",
)


class BudgetStop(RuntimeError):
    pass


@dataclass
class BudgetState:
    phase: str = "primary"
    primary_calls: int = 0
    primary_output_tokens: int = 0
    calibration_calls: int = 0
    calibration_output_tokens: int = 0

    def limits(self) -> tuple[int, int, int, int]:
        if self.phase == "primary":
            return (
                self.primary_calls,
                self.primary_output_tokens,
                PRIMARY_MAX_CALLS,
                PRIMARY_MAX_OUTPUT,
            )
        return (
            self.calibration_calls,
            self.calibration_output_tokens,
            CAL_MAX_CALLS,
            CAL_MAX_OUTPUT,
        )

    def reserve(self, requested_output: int) -> int:
        calls, used_output, max_calls, max_output = self.limits()
        if calls >= max_calls:
            raise BudgetStop(f"{self.phase} model-call budget exhausted")
        remaining = max_output - used_output
        if remaining <= 0:
            raise BudgetStop(f"{self.phase} output-token budget exhausted")
        cap = min(int(requested_output), remaining)
        if self.phase == "primary":
            self.primary_calls += 1
        else:
            self.calibration_calls += 1
        return cap

    def record_output(self, value: Any) -> None:
        if not isinstance(value, int) or value < 0:
            raise RuntimeError(
                "LM Studio did not return integer output-token usage; "
                "budget enforcement cannot be audited"
            )
        if self.phase == "primary":
            self.primary_output_tokens += value
            if self.primary_output_tokens > PRIMARY_MAX_OUTPUT:
                raise BudgetStop("primary output-token budget exceeded")
        else:
            self.calibration_output_tokens += value
            if self.calibration_output_tokens > CAL_MAX_OUTPUT:
                raise BudgetStop("calibration output-token budget exceeded")

    def manifest_usage(self) -> dict[str, Any]:
        return {
            "primary": {
                "model_calls": self.primary_calls,
                "output_tokens": self.primary_output_tokens,
                "max_model_calls": PRIMARY_MAX_CALLS,
                "max_output_tokens": PRIMARY_MAX_OUTPUT,
            },
            "calibration": {
                "model_calls": self.calibration_calls,
                "output_tokens": self.calibration_output_tokens,
                "max_model_calls": CAL_MAX_CALLS,
                "max_output_tokens": CAL_MAX_OUTPUT,
            },
        }


BUDGET = BudgetState()


def load_full_runner():
    spec = importlib.util.spec_from_file_location("cg_main_full_runner", FULL_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load api_pilot_runner.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CG = load_full_runner()


def output_schema() -> dict[str, Any]:
    return json.loads(
        (ROOT / "evals" / "protocol" / "OUTPUT-SCHEMA.json").read_text(
            encoding="utf-8-sig"
        )
    )


def calibration_schema() -> dict[str, Any]:
    return json.loads(
        (ROOT / "evals" / "protocol" / "CALIBRATION-SCHEMA.json").read_text(
            encoding="utf-8-sig"
        )
    )


def case_material(case_id: str) -> str:
    case_dir = CASES / case_id
    sections = [(case_dir / "prompt.md").read_text(encoding="utf-8-sig")]
    for path in sorted((case_dir / "evidence").iterdir()):
        if path.is_file():
            sections.append(
                f"## Evidence {path.name[:3]}\n\n"
                + path.read_text(encoding="utf-8-sig")
            )
    return "\n\n".join(section.strip() for section in sections)


def decision_contract(case_id: str) -> str:
    return (
        f"Decision for {case_id}: determine the causal explanation or causal "
        "structure justified by the supplied evidence, choose the safest "
        "decision-relevant immediate action, and identify a decision-changing "
        "next test where uncertainty remains. Use supplied evidence only; no "
        "web or external facts. Do not force a unique cause when the evidence "
        "does not justify one. Primary analysis budget: at most 12 model calls "
        "and 32,768 generated tokens across the complete mode workflow."
    )


def mandates(case_id: str) -> list[str]:
    return [
        "Build causal models around direct operational/configuration/process changes and test their required links against the evidence.",
        "Build causally distinct dependency, environment, measurement, upstream/downstream, and latent-system explanations without inheriting a favored narrative.",
        "Search for interaction, coexistence, heterogeneity, framing, evidence-dependence, and omitted-alternative structures; state what observations would distinguish them.",
    ]


def budgeted_call_adapter(
    run_dir: Path,
    stage: str,
    *,
    prompt: str,
    schema: dict | None = None,
    model: str = MODEL,
    settings: dict | None = None,
) -> dict:
    response_path = run_dir / "working" / f"{stage}.response.json"
    raw_path = run_dir / "working" / f"{stage}.raw.txt"
    request_path = run_dir / "working" / f"{stage}.request.json"
    if response_path.exists():
        return json.loads(response_path.read_text(encoding="utf-8-sig"))

    base_settings = dict(settings or {})
    base_settings.setdefault("temperature", PRIMARY_TEMPERATURE)
    base_settings.setdefault("maxOutputTokens", 8192)
    base_settings["maxTransportAttempts"] = 1
    request_path.parent.mkdir(parents=True, exist_ok=True)
    proc = None
    request = None
    for attempt in range(1, MAX_REQUEST_ATTEMPTS + 1):
        requested = dict(base_settings)
        requested["maxOutputTokens"] = BUDGET.reserve(
            base_settings["maxOutputTokens"]
        )
        request = {
            "request_id": f"{run_dir.name}-{stage}",
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "settings": requested,
            "response_schema": schema,
            "tools_enabled": False,
            "retrieval_enabled": False,
        }
        request_path.write_text(
            json.dumps(request, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        proc = subprocess.run(
            [sys.executable, str(LM_ADAPTER)],
            input=json.dumps(request, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
            timeout=900,
        )
        if proc.returncode == 0:
            break
        error = proc.stderr.strip() or f"LM Studio adapter failed at {stage}"
        transient = any(
            marker in error
            for marker in (
                "ConnectionResetError",
                "connection failed",
                "HTTP 500",
                "HTTP 502",
                "HTTP 503",
                "HTTP 504",
            )
        )
        (run_dir / "working" / f"{stage}.attempt{attempt}.transport-error.txt").write_text(
            error + "\n", encoding="utf-8"
        )
        if not transient or attempt >= MAX_REQUEST_ATTEMPTS:
            raise RuntimeError(error)
    assert proc is not None and request is not None
    envelope = json.loads(proc.stdout)
    BUDGET.record_output((envelope.get("usage") or {}).get("output_tokens"))
    raw_text = envelope.get("raw_text", "")
    if schema is not None:
        json.loads(raw_text)
    response_path.write_text(
        json.dumps(envelope, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    raw_path.write_text(raw_text, encoding="utf-8")
    return envelope


CG.call_adapter = budgeted_call_adapter
CG.case_material = case_material
CG.decision_contract = decision_contract
CG.mandates = mandates


def mode_instruction(mode: str) -> str:
    return (
        ROOT / "evals" / "protocol" / "modes" / f"{mode}.md"
    ).read_text(encoding="utf-8-sig")


def call_json(run_dir: Path, stage: str, prompt: str, schema: dict) -> dict:
    env = budgeted_call_adapter(
        run_dir,
        stage,
        prompt=prompt,
        schema=schema,
        model=MODEL,
        settings={"temperature": PRIMARY_TEMPERATURE, "maxOutputTokens": 8192},
    )
    return CG.parse_structured(run_dir, stage, env)


def call_text(run_dir: Path, stage: str, prompt: str) -> str:
    env = budgeted_call_adapter(
        run_dir,
        stage,
        prompt=prompt,
        schema=None,
        model=MODEL,
        settings={"temperature": PRIMARY_TEMPERATURE, "maxOutputTokens": 1200},
    )
    return env.get("raw_text", "")


def single_context(case_id: str, run_dir: Path, schema: dict) -> dict:
    prompt = f"""This is a controlled evaluation run.
Use only the supplied case material. Do not browse or add outside facts.

MODE INSTRUCTION:
{mode_instruction('single-context')}

PARTICIPANT-VISIBLE CASE:
{case_material(case_id)}

Return exactly the normalized final-answer object for case_id {case_id}.
"""
    return call_json(run_dir, "primary", prompt, schema)


def shared_context(case_id: str, run_dir: Path, schema: dict) -> dict:
    material = case_material(case_id)
    mode = mode_instruction("shared-context-multi-agent")
    journal: list[tuple[str, str]] = []
    analyst_prompts = [
        "Analyze from first principles: causal explanations, evidence for/against, uncertainty, actions, and discriminating tests.",
        "Review the case and shared journal; challenge framing, add missing alternatives, and identify weak inference.",
        "Stress-test the shared journal; distinguish causal-model judgment from action judgment and identify unresolved issues.",
    ]
    for idx, instruction in enumerate(analyst_prompts, start=1):
        prior = "\n\n".join(
            f"### Analyst {name}\n{text}" for name, text in journal
        ) or "(empty)"
        prompt = f"""This is a controlled evaluation run.
Use only supplied case material. Do not browse or add outside facts.

MODE INSTRUCTION:
{mode}

PARTICIPANT-VISIBLE CASE:
{material}

SHARED JOURNAL SO FAR:
{prior}

YOUR PASS:
{instruction}

Write a concise analytical journal entry, not final JSON.
"""
        journal.append((chr(64 + idx), call_text(run_dir, f"analyst-{idx}", prompt)))
    full_journal = "\n\n".join(
        f"### Analyst {name}\n{text}" for name, text in journal
    )
    synth = f"""This is a controlled evaluation run.
Use only supplied case material and journal. Do not browse or add outside facts.

MODE INSTRUCTION:
{mode}

PARTICIPANT-VISIBLE CASE:
{material}

SHARED JOURNAL:
{full_journal}

Return exactly the normalized final-answer object for case_id {case_id}.
"""
    return call_json(run_dir, "synth", synth, schema)


def reduced_context(case_id: str, run_dir: Path, schema: dict) -> dict:
    protocol = (
        ROOT / "convergence-guard" / "references" / "reduced-mode.md"
    ).read_text(encoding="utf-8-sig")
    prompt = f"""This is a controlled evaluation run.
Use only the supplied case material. Do not browse or add outside facts.

TREATMENT: Convergence Guard — Reduced Mode.

REDUCED MODE PROTOCOL:
{protocol}

DECISION CONTRACT:
{decision_contract(case_id)}

PARTICIPANT-VISIBLE CASE:
{case_material(case_id)}

Execute the Reduced Mode workflow in one effective context and return exactly
the normalized final-answer JSON object for case_id {case_id}.
"""
    return call_json(run_dir, "primary", prompt, schema)


def validate_primary(case_id: str, run_dir: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(HERE / "validate_final.py"),
            str(run_dir / "final.json"),
            "--case",
            str(CASES / case_id),
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
        raise RuntimeError("primary validation failed: " + diagnostic)


def calibrate(case_id: str, run_dir: Path, final: dict) -> dict:
    claims = json.loads(
        (CALIBRATION / f"{case_id}.json").read_text(encoding="utf-8-sig")
    )
    BUDGET.phase = "calibration"
    prompt = f"""The primary answer is frozen and must not be revised.

PUBLIC CASE:
{case_material(case_id)}

FROZEN PRIMARY:
{json.dumps(final, ensure_ascii=False)}

For each claim below, give probability 0..1 that it is true using only the case evidence:
{json.dumps(claims['claims'], ensure_ascii=False)}

Return the calibration object for case_id {case_id}.
"""
    env = budgeted_call_adapter(
        run_dir,
        "calibration",
        prompt=prompt,
        schema=calibration_schema(),
        settings={"temperature": 0, "maxOutputTokens": CAL_MAX_OUTPUT},
    )
    result = CG.parse_structured(run_dir, "calibration", env)
    (run_dir / "calibration.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return result


def load_run(run_id: str) -> dict[str, Any]:
    plan = json.loads(PLAN.read_text(encoding="utf-8-sig"))
    matches = [
        run
        for block in plan["blocks"]
        for run in block["runs"]
        if run["run_id"] == run_id
    ]
    if len(matches) != 1:
        raise RuntimeError(f"run_id must resolve exactly once: {run_id}")
    return matches[0]


def pre_run_checks(run: dict[str, Any]) -> None:
    case_id = run["case_id"]
    mode = run["mode"]
    if mode not in MODES:
        raise RuntimeError(f"unsupported mode: {mode}")
    if not (CASES / case_id / "case.json").is_file():
        raise RuntimeError(f"missing case: {case_id}")
    if mode == "cg-full":
        preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8-sig"))
        if preflight.get("overall") != "PASS" or preflight.get("cg_full_enabled") is not True:
            raise RuntimeError("frozen LM Studio isolation preflight does not permit cg-full")


def execute(run: dict[str, Any], *, defer_calibration: bool = False) -> int:
    global BUDGET
    BUDGET = BudgetState()
    case_id, mode, repeat = run["case_id"], run["mode"], run["repeat"]
    run_dir = ROOT / "evals" / "runs" / EVAL_VERSION / case_id / f"r{repeat}" / mode
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = run_dir / "manifest.json"
    manifest = {
        "run_id": run["run_id"],
        "case_id": case_id,
        "mode": mode,
        "repeat": repeat,
        "eval_version": EVAL_VERSION,
        "runtime": "standalone llama-server 2.52.0 OpenAI-compatible streaming API",
        "model": MODEL,
        "model_settings": {"temperature": PRIMARY_TEMPERATURE},
        "normalization_version": NORMALIZATION_VERSION,
        "normalization_repairs": 0,
        "status": "running",
        "isolation_preflight": "PASS" if mode == "cg-full" else "NOT_APPLICABLE",
        "budget": BUDGET.manifest_usage(),
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    try:
        schema = output_schema()
        if mode == "single-context":
            raw_final = single_context(case_id, run_dir, schema)
        elif mode == "shared-context-multi-agent":
            raw_final = shared_context(case_id, run_dir, schema)
        elif mode == "cg-reduced":
            raw_final = reduced_context(case_id, run_dir, schema)
        else:
            raw_final = CG.full_mode(case_id, run_dir, schema)

        raw_path = run_dir / "final.raw.json"
        raw_path.write_text(
            json.dumps(raw_final, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        repairs = normalize_artifact(
            raw_path, run_dir / "final.json", run_dir / "normalization.json"
        )
        normalized = json.loads((run_dir / "final.json").read_text(encoding="utf-8-sig"))
        validate_primary(case_id, run_dir)
        manifest["normalization_repairs"] = repairs
        if defer_calibration:
            manifest["status"] = "primary_complete"
        else:
            calibrate(case_id, run_dir, normalized)
            manifest["status"] = "complete"
    except BudgetStop as exc:
        manifest["status"] = "budget_stop"
        manifest["error"] = str(exc)
    except Exception as exc:
        manifest["status"] = "invalid"
        manifest["error"] = f"{type(exc).__name__}: {exc}"
    manifest["budget"] = BUDGET.manifest_usage()
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"{manifest['status'].upper()} {run['run_id']}")
    return 0 if manifest["status"] in {"complete", "primary_complete"} else 1


def calibrate_existing(run: dict[str, Any]) -> int:
    global BUDGET
    case_id, mode, repeat = run["case_id"], run["mode"], run["repeat"]
    run_dir = ROOT / "evals" / "runs" / EVAL_VERSION / case_id / f"r{repeat}" / mode
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file() or not (run_dir / "final.json").is_file():
        raise RuntimeError(f"no frozen primary result for calibration: {run['run_id']}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    if manifest.get("status") not in {"primary_complete", "primary_complete_calibration_failed"}:
        if manifest.get("status") == "complete" and (run_dir / "calibration.json").is_file():
            print(f"COMPLETE {run['run_id']} calibration already present")
            return 0
        raise RuntimeError(f"primary is not calibration-ready: {run['run_id']} status={manifest.get('status')}")

    BUDGET = BudgetState(phase="calibration")
    final = json.loads((run_dir / "final.json").read_text(encoding="utf-8-sig"))
    try:
        calibrate(case_id, run_dir, final)
        manifest["status"] = "complete"
        manifest.pop("calibration_error", None)
    except Exception as exc:
        manifest["status"] = "primary_complete_calibration_failed"
        manifest["calibration_error"] = f"{type(exc).__name__}: {exc}"
    manifest.setdefault("budget", {})["calibration"] = BUDGET.manifest_usage()["calibration"]
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"{manifest['status'].upper()} {run['run_id']}")
    return 0 if manifest["status"] == "complete" else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Required to issue model calls. Without it the command is dry-run only.",
    )
    parser.add_argument(
        "--defer-calibration",
        action="store_true",
        help="Execute and freeze the primary result now; run calibration later.",
    )
    parser.add_argument(
        "--calibrate-existing",
        action="store_true",
        help="Calibrate an already frozen primary result without rerunning primary analysis.",
    )
    args = parser.parse_args()
    run = load_run(args.run_id)
    pre_run_checks(run)
    if args.calibrate_existing:
        return calibrate_existing(run)
    if not args.execute:
        print(
            f"DRY-RUN READY {run['run_id']} case={run['case_id']} "
            f"mode={run['mode']} repeat={run['repeat']}"
        )
        return 0
    return execute(run, defer_calibration=args.defer_calibration)


if __name__ == "__main__":
    raise SystemExit(main())
