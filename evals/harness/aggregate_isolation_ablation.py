#!/usr/bin/env python3
"""Aggregate two blind judges + post-blind anchor diagnostic for isolation ablation."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "evals" / "run-plans" / "isolation-ablation-v0.1.json"
RUNS = ROOT / "evals" / "runs" / "isolation-ablation-v0.1"

SCORE_FIELDS = [
    "causal_structure_correctness",
    "premature_winner",
    "over_abstention",
    "action_quality",
    "next_test_quality",
]


def load_scores(root: Path) -> dict[str, dict[str, Any]]:
    out = {}
    for path in sorted(root.glob("I*.json")):
        d = json.loads(path.read_text(encoding="utf-8-sig"))
        if d["neutral_id"] in out:
            raise ValueError(f"duplicate {d['neutral_id']}")
        out[d["neutral_id"]] = d
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blind-map", type=Path, required=True)
    ap.add_argument("--judge-a", type=Path, required=True)
    ap.add_argument("--judge-b", type=Path, required=True)
    ap.add_argument("--anchor-a", type=Path, required=True)
    ap.add_argument("--anchor-b", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()

    plan = json.loads(PLAN.read_text(encoding="utf-8-sig"))
    mapping = json.loads(args.blind_map.read_text(encoding="utf-8-sig"))["neutral_to_run"]
    neutral_for_run = {r: n for n, r in mapping.items()}
    ja, jb = load_scores(args.judge_a), load_scores(args.judge_b)
    if len(ja) != 16 or set(ja) != set(jb) or set(ja) != set(mapping):
        raise ValueError("blind score sets must contain the same 16 IDs")
    aa, ab = load_scores(args.anchor_a), load_scores(args.anchor_b)
    if len(aa) != 8 or set(aa) != set(ab):
        raise ValueError("anchor score sets must contain same 8 IDs")

    rows = []
    disagreements = []
    for run in plan["runs"]:
        rid = run["run_id"]
        nid = neutral_for_run[rid]
        a, b = ja[nid], jb[nid]
        consensus = {}
        for field in SCORE_FIELDS:
            va, vb = a["scores"][field], b["scores"][field]
            consensus[field] = va if va == vb else None
            if va != vb:
                disagreements.append({"neutral_id": nid, "run_id": rid, "field": field, "judge_a": va, "judge_b": vb})
        anchor = None
        anchor_agree = None
        if nid in aa:
            va, vb = aa[nid]["false_anchor_adoption"], ab[nid]["false_anchor_adoption"]
            anchor = va if va == vb else None
            anchor_agree = va == vb
            if va != vb:
                disagreements.append({"neutral_id": nid, "run_id": rid, "field": "false_anchor_adoption", "judge_a": va, "judge_b": vb})
        manifest = json.loads((RUNS / rid / "manifest.json").read_text(encoding="utf-8-sig"))
        final = json.loads((RUNS / rid / "final.json").read_text(encoding="utf-8-sig"))
        rows.append({
            "run_id": rid,
            "neutral_id": nid,
            "case_id": run["case_id"],
            "isolation": run["isolation"],
            "history": run["history"],
            "scores_consensus": consensus,
            "false_anchor_adoption_consensus": anchor,
            "false_anchor_judges_agree": anchor_agree,
            "protocol_completion": final["protocol_completion"]["status"],
            "model_calls": len(manifest.get("calls", [])),
            "input_tokens": sum((c.get("input_tokens") or 0) for c in manifest.get("calls", [])),
            "output_tokens": sum((c.get("output_tokens") or 0) for c in manifest.get("calls", [])),
        })

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[f"{row['isolation']}-{row['history']}"].append(row)

    def aggregate_group(grp):
        result = {"n": len(grp)}
        for field in SCORE_FIELDS:
            vals = [r["scores_consensus"][field] for r in grp if r["scores_consensus"][field] is not None]
            result[field] = {"mean": mean(vals) if vals else None, "rated": len(vals)}
        anchors = [r["false_anchor_adoption_consensus"] for r in grp if r["false_anchor_adoption_consensus"] is not None]
        result["false_anchor_adoption"] = {"mean": mean(anchors) if anchors else None, "rated": len(anchors)}
        result["calls_mean"] = mean(r["model_calls"] for r in grp)
        result["input_tokens_mean"] = mean(r["input_tokens"] for r in grp)
        result["output_tokens_mean"] = mean(r["output_tokens"] for r in grp)
        return result

    # Paired case deltas are more informative than group means for this tiny study.
    by_key = {(r["case_id"], r["isolation"], r["history"]): r for r in rows}
    pairs = []
    for cid in plan["cases"]:
        entry = {"case_id": cid}
        for iso in ("isolated", "shared"):
            neutral = by_key[(cid, iso, "neutral")]
            anchor = by_key[(cid, iso, "false-anchor")]
            deltas = {}
            for field in SCORE_FIELDS:
                nv, av = neutral["scores_consensus"][field], anchor["scores_consensus"][field]
                deltas[field] = None if nv is None or av is None else av - nv
            entry[iso] = {
                "neutral_id": neutral["neutral_id"],
                "anchor_id": anchor["neutral_id"],
                "anchor_minus_neutral": deltas,
                "false_anchor_adoption": anchor["false_anchor_adoption_consensus"],
            }
        pairs.append(entry)

    integrity = json.loads((RUNS / "isolated-pair-integrity.json").read_text(encoding="utf-8-sig"))
    summary = {
        "benchmark_version": "isolation-ablation-v0.1",
        "interpretation": "descriptive mechanistic ablation; no population effect claim",
        "isolated_pair_integrity_pass": integrity["all_pass"],
        "judge_disagreements": disagreements,
        "groups": {k: aggregate_group(v) for k, v in sorted(groups.items())},
        "case_pairs": pairs,
        "rows": rows,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Isolation ablation v0.1 — result",
        "",
        "This is a 4-case × 2-isolation × 2-history mechanistic ablation. It is descriptive and does not establish a population effect or validate canonical Full Mode as a whole.",
        "",
        f"Isolated-pair manipulation integrity: **{'PASS' if integrity['all_pass'] else 'FAIL'}**.",
        "",
        "## Group aggregates (two-judge consensus only)",
        "",
        "| Condition | n | Structure ↑ | Premature ↓ | Over-abstain ↓ | Action ↑ | Next-test ↑ | False-anchor adoption ↓ | Calls |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for group, a in summary["groups"].items():
        def fm(field):
            x=a[field]; return "N/A" if x["mean"] is None else f"{x['mean']:.3f} ({x['rated']})"
        lines.append(
            f"| {group} | {a['n']} | {fm('causal_structure_correctness')} | {fm('premature_winner')} | "
            f"{fm('over_abstention')} | {fm('action_quality')} | {fm('next_test_quality')} | "
            f"{fm('false_anchor_adoption')} | {a['calls_mean']:.1f} |"
        )
    lines += ["", "## Case-level paired deltas", "", "Delta = false-anchor score minus neutral score within the same isolation condition.", ""]
    for pair in pairs:
        lines.append(f"### {pair['case_id']}")
        for iso in ("isolated", "shared"):
            lines.append(f"- **{iso}:** deltas `{json.dumps(pair[iso]['anchor_minus_neutral'], ensure_ascii=False)}`; false-anchor adoption = `{pair[iso]['false_anchor_adoption']}`")
        lines.append("")
    lines += [
        "## Interpretation guard",
        "",
        "The ablation tests one mechanism only: exposure to prior peer/parent conclusions during causal search. It does not test every Convergence Guard stage, and no claim about general effect size or statistical significance is warranted from four authored cases.",
        "",
    ]
    if disagreements:
        lines += ["## Judge disagreements", ""]
        for d in disagreements:
            lines.append(f"- `{d['neutral_id']}` `{d['field']}`: A={d['judge_a']}, B={d['judge_b']}")
    (args.output_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output_dir / "summary.json")
    print(args.output_dir / "REPORT.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
