#!/usr/bin/env python3
"""Validate a calibration response against its public claim list."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("calibration_json", type=Path)
    parser.add_argument("--claims", type=Path, required=True)
    args = parser.parse_args()

    data = json.loads(args.calibration_json.read_text(encoding="utf-8-sig"))
    claims = json.loads(args.claims.read_text(encoding="utf-8-sig"))
    errors: list[str] = []

    if not isinstance(data, dict) or set(data) != {"case_id", "probabilities"}:
        errors.append("root fields must be exactly case_id and probabilities")
    if data.get("case_id") != claims.get("case_id"):
        errors.append("case_id does not match calibration claim set")

    expected = {c["id"] for c in claims.get("claims", [])}
    probs = data.get("probabilities")
    seen: set[str] = set()
    if not isinstance(probs, list):
        errors.append("probabilities must be a list")
    else:
        for i, item in enumerate(probs):
            if not isinstance(item, dict) or set(item) != {"id", "p"}:
                errors.append(f"probabilities[{i}] must contain exactly id and p")
                continue
            cid = item.get("id")
            p = item.get("p")
            if cid not in expected:
                errors.append(f"unknown calibration claim id {cid!r}")
            if cid in seen:
                errors.append(f"duplicate calibration claim id {cid!r}")
            seen.add(cid)
            if not isinstance(p, (int, float)) or isinstance(p, bool) or not 0 <= p <= 1:
                errors.append(f"probability for {cid!r} must be numeric in [0,1]")

    missing = expected - seen
    if missing:
        errors.append("missing calibration claims: " + ", ".join(sorted(missing)))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS {args.calibration_json} for {claims['case_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
