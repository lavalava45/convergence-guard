#!/usr/bin/env python3
"""Audit frozen raw-vs-normalized answers and build neutral re-judge packets.

This is a post-benchmark diagnostic. It never rewrites frozen run artifacts or
recomputes benchmark scores.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DIAGNOSTIC_VERSION = "v0.1"
DEFAULT_CASE_IDS = ("M04", "M05", "M06", "M07")
N1_PATH = "causal_assessment.preferred_cause"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_diff(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    """Return deterministic leaf-level differences between two JSON values."""
    if isinstance(before, dict) and isinstance(after, dict):
        changes: list[dict[str, Any]] = []
        for key in sorted(set(before) | set(after)):
            child = f"{path}.{key}" if path else key
            if key not in before:
                changes.append({"path": child, "before": None, "after": after[key], "kind": "added"})
            elif key not in after:
                changes.append({"path": child, "before": before[key], "after": None, "kind": "removed"})
            else:
                changes.extend(json_diff(before[key], after[key], child))
        return changes
    if isinstance(before, list) and isinstance(after, list):
        changes = []
        common = min(len(before), len(after))
        for index in range(common):
            child = f"{path}[{index}]"
            changes.extend(json_diff(before[index], after[index], child))
        for index in range(common, len(before)):
            changes.append(
                {"path": f"{path}[{index}]", "before": before[index], "after": None, "kind": "removed"}
            )
        for index in range(common, len(after)):
            changes.append(
                {"path": f"{path}[{index}]", "before": None, "after": after[index], "kind": "added"}
            )
        return changes
    if before != after:
        return [{"path": path, "before": before, "after": after, "kind": "changed"}]
    return []


def causal_extract(answer: Any) -> dict[str, Any]:
    causal = answer.get("causal_assessment", {}) if isinstance(answer, dict) else {}
    if not isinstance(causal, dict):
        causal = {}
    candidates = causal.get("candidate_causes", [])
    if not isinstance(candidates, list):
        candidates = []
    cleaned_candidates = []
    for candidate in candidates:
        if isinstance(candidate, dict):
            cleaned_candidates.append(
                {
                    "id": candidate.get("id"),
                    "claim": candidate.get("claim"),
                }
            )
        else:
            cleaned_candidates.append({"id": None, "claim": candidate})
    preferred = causal.get("preferred_cause")
    candidate_ids = [c.get("id") for c in cleaned_candidates if isinstance(c.get("id"), str)]
    return {
        "status": causal.get("status"),
        "preferred_cause": preferred,
        "candidate_count": len(cleaned_candidates),
        "candidates": cleaned_candidates,
        "preferred_matches_candidate_id": isinstance(preferred, str) and preferred in candidate_ids,
    }


def n1_diagnostic(raw: Any, normalized: Any, normalization: Any, changes: list[dict[str, Any]]) -> dict[str, Any]:
    repairs = normalization.get("repairs", []) if isinstance(normalization, dict) else []
    if not isinstance(repairs, list):
        repairs = []
    n1_repairs = [
        repair
        for repair in repairs
        if isinstance(repair, dict)
        and repair.get("rule") == "N1"
        and repair.get("path") == N1_PATH
    ]
    raw_causal = causal_extract(raw)
    normalized_causal = causal_extract(normalized)
    before = raw_causal["preferred_cause"]
    after = normalized_causal["preferred_cause"]
    diff_paths = [change["path"] for change in changes]
    n1_changed_preference = before != after and N1_PATH in diff_paths
    removed_meaningful_preference = (
        n1_changed_preference
        and after is None
        and before is not None
        and (not isinstance(before, str) or bool(before.strip()))
    )
    recorded_paths = [repair.get("path") for repair in n1_repairs]
    return {
        "n1_applied": bool(n1_repairs),
        "n1_repair_count": len(n1_repairs),
        "n1_changed_preferred_cause": n1_changed_preference,
        "n1_semantic_change_flag": removed_meaningful_preference,
        "n1_semantic_change_basis": (
            "N1 removed a non-null preferred_cause value from the frozen raw artifact; "
            "this flags content deletion for re-judging and does not itself assert a score change."
            if removed_meaningful_preference
            else None
        ),
        "only_n1_path_changed": bool(changes) and set(diff_paths) == {N1_PATH},
        "normalization_record_matches_changed_path": (
            (not changes and not n1_repairs)
            or (set(diff_paths) == set(recorded_paths) == {N1_PATH})
        ),
        "before_preferred_cause": before,
        "after_preferred_cause": after,
    }


def case_material(case_dir: Path) -> dict[str, Any]:
    evidence = []
    evidence_dir = case_dir / "evidence"
    for path in sorted(evidence_dir.iterdir()):
        if path.is_file():
            evidence.append(
                {
                    "evidence_id": path.name[:3],
                    "filename": path.name,
                    "content": path.read_text(encoding="utf-8-sig"),
                }
            )
    return {
        "case_id": case_dir.name,
        "case_metadata": read_json(case_dir / "case.json"),
        "prompt": (case_dir / "prompt.md").read_text(encoding="utf-8-sig"),
        "evidence": evidence,
    }


def locate_run_dir(runs_root: Path, case_id: str, mode: str) -> Path:
    matches = sorted(path for path in (runs_root / case_id).glob(f"r*/{mode}") if path.is_dir())
    if len(matches) != 1:
        raise ValueError(f"expected exactly one run directory for {case_id}/{mode}, found {matches}")
    return matches[0]


def packet_instructions() -> dict[str, Any]:
    return {
        "purpose": "Post-benchmark normalization diagnostic only; do not modify frozen main-v0.1.7 scores.",
        "judge_task": [
            "Compare the frozen raw participant answer with the normalized answer side-by-side.",
            "Assess whether normalization changes the substance of the causal commitment, including whether a causal winner, coexistence relation, interaction, or live alternative is added or removed.",
            "Assess whether the action/reason and next-test text still imply a causal commitment that differs from the normalized causal_assessment block.",
            "Report the semantic effect of the normalization delta without inferring treatment identity.",
        ],
        "requested_output": {
            "semantic_equivalent": "boolean",
            "causal_commitment_changed": "boolean",
            "action_consistency_changed": "boolean",
            "notes": "short evidence-based explanation",
        },
    }


def render_markdown(audit: dict[str, Any]) -> str:
    lines = [
        "# main-v0.1.7 normalization diagnostics: M04–M07",
        "",
        "This is a post-benchmark diagnostic audit. It compares frozen `final.raw.json` with the frozen normalized `final.json`; it does not alter or recompute the published benchmark scores.",
        "",
        "`n1_semantic_change_flag=1` means N1 removed a non-null `preferred_cause` value. The flag marks a causal-content deletion for neutral re-judging; it is not itself a judgment that any frozen semantic score was wrong.",
        "",
        f"Runs audited: **{audit['totals']['runs']}**. N1 applied: **{audit['totals']['n1_applied']}**. N1 semantic-change flags: **{audit['totals']['n1_semantic_change_flags']}**.",
        "",
        "| Neutral ID | Case | Mode | Raw status | Raw preferred cause | Normalized preferred cause | N1 | Semantic flag | Only N1 path changed |",
        "|---|---|---|---|---|---|---:|---:|---:|",
    ]
    for row in audit["runs"]:
        raw_preferred = row["causal_structure"]["raw"]["preferred_cause"]
        normalized_preferred = row["causal_structure"]["normalized"]["preferred_cause"]
        def md(value: Any) -> str:
            if value is None:
                return "`null`"
            text = str(value).replace("|", "\\|").replace("\n", " ")
            if len(text) > 88:
                text = text[:85] + "..."
            return text
        lines.append(
            f"| {row['neutral_id']} | {row['case_id']} | {row['mode']} | "
            f"{md(row['causal_structure']['raw']['status'])} | {md(raw_preferred)} | "
            f"{md(normalized_preferred)} | {int(row['n1']['n1_applied'])} | "
            f"{int(row['n1']['n1_semantic_change_flag'])} | {int(row['n1']['only_n1_path_changed'])} |"
        )
    lines += [
        "",
        "Neutral packet files are under `rejudge-packets/`. They include the public case material and the raw/normalized artifacts, but omit mode, run ID, resource use and frozen judge scores.",
        "",
    ]
    return "\n".join(lines)


def build(args: argparse.Namespace) -> dict[str, Any]:
    summary = read_json(args.summary)
    selected = [row for row in summary.get("runs", []) if row.get("case_id") in set(args.case_ids)]
    expected = len(args.case_ids) * len(summary.get("by_mode", {}))
    if len(selected) != expected:
        raise ValueError(f"expected {expected} selected summary rows, found {len(selected)}")

    neutral_ids = [row.get("neutral_id") for row in selected]
    if any(not isinstance(value, str) for value in neutral_ids) or len(set(neutral_ids)) != len(neutral_ids):
        raise ValueError("selected summary rows must have unique string neutral IDs")

    packets_dir = args.output / "rejudge-packets"
    packets_dir.mkdir(parents=True, exist_ok=True)
    audit_rows: list[dict[str, Any]] = []

    for row in sorted(selected, key=lambda item: item["neutral_id"]):
        case_id = row["case_id"]
        mode = row["mode"]
        neutral_id = row["neutral_id"]
        run_dir = locate_run_dir(args.runs, case_id, mode)
        raw_path = run_dir / "final.raw.json"
        normalized_path = run_dir / "final.json"
        normalization_path = run_dir / "normalization.json"
        for path in (raw_path, normalized_path, normalization_path):
            if not path.is_file():
                raise FileNotFoundError(path)

        raw = read_json(raw_path)
        normalized = read_json(normalized_path)
        normalization = read_json(normalization_path)
        changes = json_diff(raw, normalized)
        n1 = n1_diagnostic(raw, normalized, normalization, changes)
        causal = {"raw": causal_extract(raw), "normalized": causal_extract(normalized)}

        diagnostic_row = {
            "neutral_id": neutral_id,
            "run_id": row["run_id"],
            "case_id": case_id,
            "mode": mode,
            "artifact_hashes": {
                "final.raw.json": sha256_file(raw_path),
                "final.json": sha256_file(normalized_path),
                "normalization.json": sha256_file(normalization_path),
            },
            "json_changed": bool(changes),
            "changes": changes,
            "n1": n1,
            "causal_structure": causal,
        }
        audit_rows.append(diagnostic_row)

        packet = {
            "packet_version": DIAGNOSTIC_VERSION,
            "benchmark_version": "main-v0.1.7",
            "neutral_id": neutral_id,
            "case": case_material(args.cases / case_id),
            "diagnostic_instructions": packet_instructions(),
            "causal_extract": causal,
            "n1_diagnostic": n1,
            "normalization_audit": normalization,
            "artifacts": {
                "raw_participant_answer": raw,
                "normalized_answer": normalized,
            },
            "artifact_hashes": diagnostic_row["artifact_hashes"],
        }
        forbidden = {"run_id", "mode", "semantic", "resource", "scores"}
        if forbidden & set(packet):
            raise AssertionError("neutral packet leaked treatment or frozen-score metadata")
        write_json(packets_dir / f"{neutral_id}.json", packet)

    audit = {
        "diagnostic_version": DIAGNOSTIC_VERSION,
        "benchmark_version": "main-v0.1.7",
        "scope": list(args.case_ids),
        "frozen_scores_modified": False,
        "definition": {
            "n1_semantic_change_flag": (
                "true when the observed N1 delta removes a non-null, non-empty preferred_cause from final.raw.json; "
                "the flag identifies a semantic re-judge candidate and does not assign or revise a benchmark score"
            )
        },
        "totals": {
            "runs": len(audit_rows),
            "json_changed": sum(int(row["json_changed"]) for row in audit_rows),
            "n1_applied": sum(int(row["n1"]["n1_applied"]) for row in audit_rows),
            "n1_semantic_change_flags": sum(
                int(row["n1"]["n1_semantic_change_flag"]) for row in audit_rows
            ),
            "normalization_record_mismatches": sum(
                int(not row["n1"]["normalization_record_matches_changed_path"]) for row in audit_rows
            ),
        },
        "runs": audit_rows,
    }
    write_json(args.output / "audit.json", audit)
    (args.output / "audit.md").write_text(render_markdown(audit), encoding="utf-8")
    return audit


def main() -> int:
    evals_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=Path, default=evals_root / "runs" / "main-v0.1.7")
    parser.add_argument("--summary", type=Path, default=evals_root / "results" / "main-v0.1.7" / "summary.json")
    parser.add_argument("--cases", type=Path, default=evals_root / "cases" / "main")
    parser.add_argument(
        "--output",
        type=Path,
        default=evals_root / "results" / "main-v0.1.7" / "diagnostics",
    )
    parser.add_argument("--case-ids", nargs="+", default=list(DEFAULT_CASE_IDS))
    args = parser.parse_args()
    audit = build(args)
    print(
        "DIAGNOSTICS "
        f"runs={audit['totals']['runs']} "
        f"n1_applied={audit['totals']['n1_applied']} "
        f"semantic_flags={audit['totals']['n1_semantic_change_flags']} "
        f"record_mismatches={audit['totals']['normalization_record_mismatches']} "
        f"output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
