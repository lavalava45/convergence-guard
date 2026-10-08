#!/usr/bin/env python3
"""Aggregate two blind normalization re-judges without revising frozen scores."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


FIELDS = [
    ("raw", "causal_structure_correct"),
    ("raw", "premature_winner"),
    ("raw", "winner_like_signal"),
    ("normalized", "causal_structure_correct"),
    ("normalized", "premature_winner"),
    ("normalized", "winner_like_signal"),
    ("normalization", "materially_changes_semantic_judgment"),
    ("normalization", "direction"),
]


def load_scores(root: Path) -> dict[str, dict[str, Any]]:
    result = {}
    for path in sorted(root.glob("R*.json")):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        neutral = data["neutral_id"]
        if neutral in result:
            raise ValueError(f"duplicate neutral ID in {root}: {neutral}")
        result[neutral] = data
    return result


def get(data: dict[str, Any], path: tuple[str, str]) -> Any:
    return data[path[0]][path[1]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge-a", type=Path, required=True)
    parser.add_argument("--judge-b", type=Path, required=True)
    parser.add_argument("--main-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    a = load_scores(args.judge_a)
    b = load_scores(args.judge_b)
    if len(a) != 16 or set(a) != set(b):
        raise ValueError(f"expected same 16 neutral IDs; judge-a={len(a)} judge-b={len(b)}")

    main_summary = json.loads(args.main_summary.read_text(encoding="utf-8-sig"))
    lookup = {
        row["neutral_id"]: {"run_id": row["run_id"], "mode": row["mode"], "case_id": row["case_id"]}
        for row in main_summary["runs"]
    }

    field_agreement = {f"{p}.{k}": 0 for p, k in FIELDS}
    rows = []
    disagreements = []
    by_mode: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for neutral in sorted(a):
        sa, sb = a[neutral], b[neutral]
        if sa["case_id"] != sb["case_id"]:
            raise ValueError(f"case mismatch for {neutral}")
        meta = lookup.get(neutral)
        if not meta:
            raise ValueError(f"neutral ID absent from frozen main summary: {neutral}")
        consensus: dict[str, Any] = {}
        per_field = {}
        for path in FIELDS:
            va, vb = get(sa, path), get(sb, path)
            name = f"{path[0]}.{path[1]}"
            agree = va == vb
            field_agreement[name] += int(agree)
            per_field[name] = {"judge_a": va, "judge_b": vb, "agree": agree}
            consensus[name] = va if agree else None
            if not agree:
                disagreements.append({"neutral_id": neutral, "field": name, "judge_a": va, "judge_b": vb})
        row = {
            "neutral_id": neutral,
            **meta,
            "consensus": consensus,
            "per_field": per_field,
            "judge_a_rationale": sa.get("rationale", ""),
            "judge_b_rationale": sb.get("rationale", ""),
        }
        rows.append(row)
        by_mode[meta["mode"]].append(row)

    def unanimous_sum(mode_rows: list[dict[str, Any]], field: str) -> dict[str, int]:
        values = [r["consensus"][field] for r in mode_rows]
        usable = [int(v) for v in values if isinstance(v, int)]
        return {"positive": sum(usable), "rated": len(usable), "disagreements": len(values) - len(usable)}

    mode_summary = {}
    for mode, mode_rows in sorted(by_mode.items()):
        mode_summary[mode] = {
            "n": len(mode_rows),
            "raw_structure_correct": unanimous_sum(mode_rows, "raw.causal_structure_correct"),
            "normalized_structure_correct": unanimous_sum(mode_rows, "normalized.causal_structure_correct"),
            "raw_premature_winner": unanimous_sum(mode_rows, "raw.premature_winner"),
            "normalized_premature_winner": unanimous_sum(mode_rows, "normalized.premature_winner"),
            "raw_winner_like_signal": unanimous_sum(mode_rows, "raw.winner_like_signal"),
            "normalized_winner_like_signal": unanimous_sum(mode_rows, "normalized.winner_like_signal"),
            "normalization_material_change": unanimous_sum(mode_rows, "normalization.materially_changes_semantic_judgment"),
        }

    summary = {
        "diagnostic": "main-v0.1.7-normalization-reaudit-v0.1",
        "frozen_scores_modified": False,
        "judge_count": 2,
        "packet_count": 16,
        "field_agreement": {name: {"agree": count, "n": 16, "rate": count / 16} for name, count in field_agreement.items()},
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
        "by_mode_after_unblinding": mode_summary,
        "rows": rows,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "rejudge-summary.json"
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Blind raw-vs-normalized re-judging — main-v0.1.7",
        "",
        "This is a post-benchmark diagnostic layer. It does **not** replace or modify the frozen main-v0.1.7 scores.",
        "",
        "Two independent judges scored all 16 M04–M07 neutral packets while blind to treatment mode. Each judge saw the public case, the frozen hidden key, and the raw/normalized participant answers side-by-side. The mode mapping below was joined only after both score sets were saved.",
        "",
        "## Inter-rater agreement",
        "",
        "| Field | Agreement |",
        "|---|---:|",
    ]
    for name, item in summary["field_agreement"].items():
        lines.append(f"| `{name}` | {item['agree']}/16 ({item['rate']:.1%}) |")
    lines += [
        "",
        f"Total field-level disagreements: **{len(disagreements)}**. No tie-breaking adjudication is silently substituted; a consensus value is reported only where both judges agree.",
        "",
        "## Unanimous diagnostics after unblinding",
        "",
        "Counts below use only judge-agreed cells; `rated` can therefore be < n when judges disagree.",
        "",
        "| Mode | n | Raw structure correct | Norm structure correct | Raw premature winner | Norm premature winner | Raw winner-like signal | Norm winner-like signal | Material N1 effect |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for mode, item in mode_summary.items():
        def fmt(key: str) -> str:
            x = item[key]
            return f"{x['positive']}/{x['rated']}" + (f" (+{x['disagreements']} disagree)" if x['disagreements'] else "")
        lines.append(
            f"| {mode} | {item['n']} | {fmt('raw_structure_correct')} | {fmt('normalized_structure_correct')} | "
            f"{fmt('raw_premature_winner')} | {fmt('normalized_premature_winner')} | "
            f"{fmt('raw_winner_like_signal')} | {fmt('normalized_winner_like_signal')} | {fmt('normalization_material_change')} |"
        )
    lines += [
        "",
        "## Interpretation rule",
        "",
        "The deterministic N1 audit answers *whether a non-null preferred cause was deleted*. This re-judge answers the different semantic question: *did that deletion change the causal interpretation a blind evaluator would assign?* Because this is a diagnostic re-analysis of an existing small dataset, it is descriptive and should not be presented as a new performance benchmark.",
        "",
    ]
    if disagreements:
        lines += ["## Disagreements", ""]
        for d in disagreements:
            lines.append(f"- `{d['neutral_id']}` `{d['field']}`: judge A={d['judge_a']!r}, judge B={d['judge_b']!r}")
        lines.append("")
    (args.output_dir / "REJUDGE-REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json_path)
    print(args.output_dir / "REJUDGE-REPORT.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
