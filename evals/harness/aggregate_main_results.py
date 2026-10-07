#!/usr/bin/env python3
"""Aggregate frozen main-study results without inventing a composite score."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


SEMANTIC_KEYS = (
    "premature_winner",
    "correct_abstention",
    "over_abstention",
    "action_quality",
    "causal_mechanism_recall",
    "unsupported_mechanisms",
    "evidence_dependence_errors",
    "next_test_quality",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def response_usage(run_dir: Path, *, calibration: bool) -> tuple[int, int]:
    input_tokens = 0
    output_tokens = 0
    for path in (run_dir / "working").glob("*.response.json"):
        is_cal = path.name == "calibration.response.json"
        if is_cal != calibration:
            continue
        envelope = read_json(path)
        usage = envelope.get("usage") or {}
        inp = usage.get("input_tokens")
        out = usage.get("output_tokens")
        if isinstance(inp, int):
            input_tokens += inp
        if isinstance(out, int):
            output_tokens += out
    return input_tokens, output_tokens


def retry_count(run_dir: Path, *, calibration: bool) -> int:
    count = 0
    for path in (run_dir / "working").glob("*.transport-error.txt"):
        is_cal = path.name.startswith("calibration.")
        if is_cal == calibration:
            count += 1
    return count


def calibration_brier(calibration: dict[str, Any], key: dict[str, Any]) -> float:
    truth = {item["id"]: float(item["truth"]) for item in key["calibration_claims"]}
    probs = {item["id"]: float(item["p"]) for item in calibration["probabilities"]}
    if set(probs) != set(truth):
        raise ValueError(f"calibration IDs mismatch for {key['case_id']}")
    return mean((probs[k] - truth[k]) ** 2 for k in sorted(truth))


def final_structure(final: dict[str, Any], key: dict[str, Any]) -> dict[str, Any]:
    causal = final.get("causal_assessment") or {}
    status = causal.get("status")
    preferred = causal.get("preferred_cause")
    candidate_ids = {
        c.get("id")
        for c in causal.get("candidate_causes", [])
        if isinstance(c, dict)
    }
    consistent = (
        (status == "CHOOSE" and isinstance(preferred, str) and preferred in candidate_ids)
        or (status in {"COEXIST", "INSUFFICIENT"} and preferred is None)
    )
    acceptable = key.get("causal_structure", {}).get("acceptable_status", [])
    return {
        "declared_status": status,
        "declared_status_matches_key": status in acceptable,
        "final_structure_consistent": consistent,
    }


def validate_score(score: dict[str, Any]) -> None:
    if set(score.get("scores", {})) != set(SEMANTIC_KEYS):
        raise ValueError(f"judge score keys mismatch for {score.get('neutral_id')}")
    s = score["scores"]
    for key in ("premature_winner", "correct_abstention", "over_abstention"):
        if s[key] not in (0, 1, None):
            raise ValueError(f"invalid {key} in {score.get('neutral_id')}: {s[key]}")
    for key in ("action_quality", "next_test_quality"):
        if s[key] not in (0, 1, 2):
            raise ValueError(f"invalid {key} in {score.get('neutral_id')}: {s[key]}")
    recall = s["causal_mechanism_recall"]
    if not isinstance(recall, (int, float)) or not 0 <= recall <= 1:
        raise ValueError(f"invalid causal_mechanism_recall in {score.get('neutral_id')}")
    for key in ("unsupported_mechanisms", "evidence_dependence_errors"):
        value = s[key]
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"invalid {key} in {score.get('neutral_id')}: {value}")


def load_scores(scores_root: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in scores_root.rglob("R*.json"):
        score = read_json(path)
        validate_score(score)
        neutral_id = score["neutral_id"]
        if neutral_id in result:
            raise ValueError(f"duplicate judge score for {neutral_id}")
        result[neutral_id] = score
    return result


def avg(values: list[float | int | None]) -> float | None:
    usable = [float(v) for v in values if v is not None]
    return mean(usable) if usable else None


def aggregate_mode(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scores = [r["semantic"] for r in rows]
    return {
        "n": len(rows),
        "premature_winner_rate": avg([s["premature_winner"] for s in scores]),
        "correct_abstention_rate_applicable": avg([s["correct_abstention"] for s in scores]),
        "over_abstention_rate_applicable": avg([s["over_abstention"] for s in scores]),
        "action_quality_mean": avg([s["action_quality"] for s in scores]),
        "causal_mechanism_recall_mean": avg([s["causal_mechanism_recall"] for s in scores]),
        "unsupported_mechanisms_mean": avg([s["unsupported_mechanisms"] for s in scores]),
        "evidence_dependence_errors_mean": avg([s["evidence_dependence_errors"] for s in scores]),
        "next_test_quality_mean": avg([s["next_test_quality"] for s in scores]),
        "calibration_brier_mean": avg([r["calibration_brier"] for r in rows]),
        "declared_status_match_rate": avg([
            int(r["structural"]["declared_status_matches_key"]) for r in rows
        ]),
        "normalization_repair_rate": avg([
            int(r["normalization_repairs"] > 0) for r in rows
        ]),
        "primary_model_calls_mean": avg([r["resource"]["primary_model_calls"] for r in rows]),
        "primary_input_tokens_mean": avg([r["resource"]["primary_input_tokens"] for r in rows]),
        "primary_output_tokens_mean": avg([r["resource"]["primary_output_tokens"] for r in rows]),
        "primary_transport_retries_total": sum(r["resource"]["primary_transport_retries"] for r in rows),
    }


def markdown(summary: dict[str, Any]) -> str:
    modes = ["single-context", "shared-context-multi-agent", "cg-reduced", "cg-full"]
    lines = [
        "# Convergence Guard main benchmark — main-v0.1.7",
        "",
        "This report contains the unblinded aggregate after blind semantic judging. No post-hoc weighted composite score is used.",
        "",
        "## Aggregate by mode",
        "",
        "| Mode | Premature winner ↓ | Correct abstention ↑ | Over-abstention ↓ | Action (0–2) ↑ | Mechanism recall ↑ | Unsupported mech. ↓ | Dependence errors ↓ | Next test (0–2) ↑ | Brier ↓ | Calls | Input tok | Output tok |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for mode in modes:
        a = summary["by_mode"][mode]
        def f(x: Any) -> str:
            return "N/A" if x is None else f"{x:.3f}"
        lines.append(
            f"| {mode} | {f(a['premature_winner_rate'])} | {f(a['correct_abstention_rate_applicable'])} | "
            f"{f(a['over_abstention_rate_applicable'])} | {f(a['action_quality_mean'])} | "
            f"{f(a['causal_mechanism_recall_mean'])} | {f(a['unsupported_mechanisms_mean'])} | "
            f"{f(a['evidence_dependence_errors_mean'])} | {f(a['next_test_quality_mean'])} | "
            f"{f(a['calibration_brier_mean'])} | {f(a['primary_model_calls_mean'])} | "
            f"{f(a['primary_input_tokens_mean'])} | {f(a['primary_output_tokens_mean'])} |"
        )
    lines += [
        "",
        "## Per-case results",
        "",
        "| Case | Mode | Status | Status key match | Premature winner | Correct abstention | Over-abstention | Action | Recall | Unsupported | Dependence err. | Next test | Brier | Calls | Out tok |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary["runs"]:
        s = row["semantic"]
        st = row["structural"]
        na = lambda x: "N/A" if x is None else str(x)
        lines.append(
            f"| {row['case_id']} | {row['mode']} | {st['declared_status']} | "
            f"{int(st['declared_status_matches_key'])} | {s['premature_winner']} | "
            f"{na(s['correct_abstention'])} | {na(s['over_abstention'])} | "
            f"{s['action_quality']} | {s['causal_mechanism_recall']:.3f} | "
            f"{s['unsupported_mechanisms']} | {s['evidence_dependence_errors']} | "
            f"{s['next_test_quality']} | {row['calibration_brier']:.3f} | "
            f"{row['resource']['primary_model_calls']} | {row['resource']['primary_output_tokens']} |"
        )
    lines.append("")
    lines.append("Primary semantic metrics are blind-judge outputs; declared-status matching is diagnostic only.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--runs", type=Path, required=True)
    parser.add_argument("--private-keys", type=Path, required=True)
    parser.add_argument("--blind-map", type=Path, required=True)
    parser.add_argument("--judge-scores", type=Path, required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--md-output", type=Path, required=True)
    args = parser.parse_args()

    plan = read_json(args.plan)
    planned = {
        run["run_id"]: run
        for block in plan["blocks"]
        for run in block["runs"]
    }
    blind = read_json(args.blind_map)["blind_to_run"]
    if set(blind.values()) != set(planned):
        raise ValueError("blind map and plan do not contain the same run IDs")
    scores = load_scores(args.judge_scores)
    if set(scores) != set(blind):
        missing = sorted(set(blind) - set(scores))
        extra = sorted(set(scores) - set(blind))
        raise ValueError(f"judge scores incomplete: missing={missing} extra={extra}")

    neutral_for_run = {run_id: neutral_id for neutral_id, run_id in blind.items()}
    rows: list[dict[str, Any]] = []
    for run_id, run in planned.items():
        case_id = run["case_id"]
        run_dir = args.runs / case_id / f"r{run['repeat']}" / run["mode"]
        manifest = read_json(run_dir / "manifest.json")
        if manifest.get("status") != "complete":
            raise ValueError(f"run not fully complete: {run_id}={manifest.get('status')}")
        final = read_json(run_dir / "final.json")
        calibration = read_json(run_dir / "calibration.json")
        key = read_json(args.private_keys / case_id / "key.json")
        primary_in, primary_out = response_usage(run_dir, calibration=False)
        cal_in, cal_out = response_usage(run_dir, calibration=True)
        score = scores[neutral_for_run[run_id]]
        rows.append({
            "run_id": run_id,
            "neutral_id": neutral_for_run[run_id],
            "case_id": case_id,
            "applicability_class": key.get("applicability_class"),
            "mode": run["mode"],
            "semantic": score["scores"],
            "structural": final_structure(final, key),
            "calibration_brier": calibration_brier(calibration, key),
            "normalization_repairs": manifest.get("normalization_repairs", 0),
            "resource": {
                "primary_model_calls": manifest["budget"]["primary"]["model_calls"],
                "primary_input_tokens": primary_in,
                "primary_output_tokens": primary_out,
                "primary_transport_retries": retry_count(run_dir, calibration=False),
                "calibration_model_calls": manifest["budget"]["calibration"]["model_calls"],
                "calibration_input_tokens": cal_in,
                "calibration_output_tokens": cal_out,
                "calibration_transport_retries": retry_count(run_dir, calibration=True),
            },
        })

    rows.sort(key=lambda r: (r["case_id"], r["mode"]))
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["mode"]].append(row)
    summary = {
        "benchmark_version": "main-v0.1.7",
        "run_count": len(rows),
        "no_composite_score": True,
        "by_mode": {mode: aggregate_mode(grouped[mode]) for mode in sorted(grouped)},
        "runs": rows,
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.md_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.md_output.write_text(markdown(summary), encoding="utf-8")
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.md_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
