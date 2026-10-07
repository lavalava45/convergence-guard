#!/usr/bin/env python3
"""Strict stdlib validation for normalized comparative-eval final answers."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

STATUSES = {"CHOOSE", "COEXIST", "INSUFFICIENT"}
EVIDENCE_ID = re.compile(r"^E\d{2}$")

ROOT_FIELDS = {"case_id", "causal_assessment", "action", "evidence", "uncertainty", "next_test"}
CAUSAL_FIELDS = {"status", "candidate_causes", "preferred_cause"}
CANDIDATE_FIELDS = {"id", "claim"}
ACTION_FIELDS = {"recommended_action", "reason"}
EVIDENCE_FIELDS = {"evidence_ids", "claim"}
NEXT_TEST_FIELDS = {"test", "outcome_a_implication", "outcome_b_implication"}


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def exact_fields(obj: object, required: set[str], label: str, errors: list[str]) -> bool:
    if not isinstance(obj, dict):
        errors.append(f"{label} must be an object")
        return False
    actual = set(obj)
    for field in sorted(required - actual):
        errors.append(f"{label} missing {field}")
    for field in sorted(actual - required):
        errors.append(f"{label} has unsupported field {field}")
    return True


def discover_case(case_dir: Path) -> tuple[str, set[str]]:
    case = json.loads((case_dir / "case.json").read_text(encoding="utf-8-sig"))
    case_id = case.get("case_id")
    if not nonempty(case_id):
        raise ValueError(f"{case_dir / 'case.json'}: invalid case_id")
    evidence_dir = case_dir / "evidence"
    ids = {
        p.name[:3]
        for p in evidence_dir.iterdir()
        if p.is_file() and EVIDENCE_ID.fullmatch(p.name[:3])
    }
    if not ids:
        raise ValueError(f"{evidence_dir}: no E## evidence files")
    return case_id, ids


def validate(
    data: object,
    *,
    expected_case_id: str | None = None,
    allowed_evidence_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not exact_fields(data, ROOT_FIELDS, "root", errors):
        return errors

    case_id = data.get("case_id")
    if not nonempty(case_id):
        errors.append("case_id must be a non-empty string")
    elif expected_case_id is not None and case_id != expected_case_id:
        errors.append(f"case_id {case_id!r} does not match expected case {expected_case_id!r}")

    causal = data.get("causal_assessment")
    candidate_ids: set[str] = set()
    if exact_fields(causal, CAUSAL_FIELDS, "causal_assessment", errors):
        status = causal.get("status")
        if status not in STATUSES:
            errors.append("causal_assessment.status must be CHOOSE, COEXIST, or INSUFFICIENT")

        candidates = causal.get("candidate_causes")
        if not isinstance(candidates, list) or not candidates:
            errors.append("candidate_causes must be a non-empty list")
        else:
            for i, item in enumerate(candidates):
                label = f"candidate_causes[{i}]"
                if exact_fields(item, CANDIDATE_FIELDS, label, errors):
                    cid = item.get("id")
                    if not nonempty(cid):
                        errors.append(f"{label}.id must be non-empty")
                    elif cid in candidate_ids:
                        errors.append(f"duplicate candidate id: {cid}")
                    else:
                        candidate_ids.add(cid)
                    if not nonempty(item.get("claim")):
                        errors.append(f"{label}.claim must be non-empty")

        preferred = causal.get("preferred_cause")
        if preferred is not None and not nonempty(preferred):
            errors.append("preferred_cause must be a non-empty candidate id or null")
        if status == "CHOOSE":
            if not nonempty(preferred):
                errors.append("CHOOSE requires a non-null preferred_cause")
            elif preferred not in candidate_ids:
                errors.append("preferred_cause must match one candidate_causes[].id")
        elif status in {"COEXIST", "INSUFFICIENT"} and preferred is not None:
            errors.append(f"{status} requires preferred_cause=null")

    action = data.get("action")
    if exact_fields(action, ACTION_FIELDS, "action", errors):
        if not nonempty(action.get("recommended_action")):
            errors.append("action.recommended_action must be non-empty")
        if not nonempty(action.get("reason")):
            errors.append("action.reason must be non-empty")

    evidence = data.get("evidence")
    if not isinstance(evidence, list):
        errors.append("evidence must be a list")
    else:
        for i, item in enumerate(evidence):
            label = f"evidence[{i}]"
            if not exact_fields(item, EVIDENCE_FIELDS, label, errors):
                continue
            ids = item.get("evidence_ids")
            if not isinstance(ids, list) or not ids:
                errors.append(f"{label}.evidence_ids must be a non-empty list")
            else:
                for evidence_id in ids:
                    if not isinstance(evidence_id, str) or not EVIDENCE_ID.fullmatch(evidence_id):
                        errors.append(f"{label}.evidence_ids contains invalid id {evidence_id!r}")
                    elif allowed_evidence_ids is not None and evidence_id not in allowed_evidence_ids:
                        errors.append(f"{label}.evidence_ids references unknown case evidence {evidence_id}")
            if not nonempty(item.get("claim")):
                errors.append(f"{label}.claim must be non-empty")

    uncertainty = data.get("uncertainty")
    if not isinstance(uncertainty, list):
        errors.append("uncertainty must be a list")
    elif not all(nonempty(x) for x in uncertainty):
        errors.append("uncertainty entries must be non-empty strings")

    next_test = data.get("next_test")
    if exact_fields(next_test, NEXT_TEST_FIELDS, "next_test", errors):
        for field in sorted(NEXT_TEST_FIELDS):
            if not nonempty(next_test.get(field)):
                errors.append(f"next_test.{field} must be non-empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("final_json", type=Path)
    parser.add_argument("--case", type=Path, required=True, help="public case directory")
    args = parser.parse_args()

    try:
        data = json.loads(args.final_json.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        print(
            "ERROR: invalid JSON: "
            f"line {exc.lineno} column {exc.colno}: {exc.msg}"
        )
        return 1
    case_id, evidence_ids = discover_case(args.case)
    errors = validate(data, expected_case_id=case_id, allowed_evidence_ids=evidence_ids)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS {args.final_json} for {case_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
