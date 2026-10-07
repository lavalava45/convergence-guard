#!/usr/bin/env python3
"""Validate participant-visible eval case packages using only stdlib."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FORBIDDEN_PUBLIC_NAMES = {
    "key.json",
    "answer-key.json",
    "answer_key.json",
    "ground-truth.json",
    "ground_truth.json",
    "rubric.json",
    "judge-key.json",
}
EVIDENCE_RE = re.compile(r"^E\d{2}[-_.]")


def validate_case(case_dir: Path) -> list[str]:
    errors: list[str] = []
    case_file = case_dir / "case.json"
    prompt_file = case_dir / "prompt.md"
    evidence_dir = case_dir / "evidence"

    if not case_file.is_file():
        return ["missing case.json"]
    if not prompt_file.is_file():
        errors.append("missing prompt.md")
    if not evidence_dir.is_dir():
        errors.append("missing evidence/ directory")

    try:
        data = json.loads(case_file.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        errors.append(f"invalid case.json: {exc}")
        return errors

    required = ["case_id", "case_type", "web_access", "allowed_tools", "output_schema"]
    for field in required:
        if field not in data:
            errors.append(f"case.json missing field: {field}")

    if data.get("case_id") != case_dir.name:
        errors.append(
            f"case_id {data.get('case_id')!r} does not match directory {case_dir.name!r}"
        )

    if data.get("web_access") is not False:
        errors.append("fixed-document eval cases must set web_access=false")

    suspicious = []
    for path in case_dir.rglob("*"):
        if path.is_file() and path.name.lower() in FORBIDDEN_PUBLIC_NAMES:
            suspicious.append(str(path.relative_to(case_dir)))
    if suspicious:
        errors.append(
            "forbidden hidden-key-like files in public case: " + ", ".join(suspicious)
        )

    if evidence_dir.is_dir():
        evidence_files = sorted(p for p in evidence_dir.iterdir() if p.is_file())
        if not evidence_files:
            errors.append("evidence/ contains no files")
        ids: list[str] = []
        for path in evidence_files:
            if not EVIDENCE_RE.match(path.name):
                errors.append(f"evidence filename lacks E## prefix: {path.name}")
            else:
                ids.append(path.name[:3])
        if len(ids) != len(set(ids)):
            errors.append("duplicate evidence IDs")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases_root", type=Path)
    args = parser.parse_args()

    case_dirs = sorted(p.parent for p in args.cases_root.glob("*/case.json"))
    if not case_dirs:
        print(f"ERROR: no cases found under {args.cases_root}")
        return 2

    failed = False
    for case_dir in case_dirs:
        errors = validate_case(case_dir)
        if errors:
            failed = True
            print(f"FAIL {case_dir.name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {case_dir.name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

