#!/usr/bin/env python3
"""Fail closed unless a runtime preflight is sufficient for cg-full."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = {
    "parent_transcript",
    "sibling_outputs",
    "prior_worker_history",
    "account_project_memory",
    "retrieval",
    "filesystem_tools",
    "coordinator_handoff",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("preflight", type=Path)
    args = parser.parse_args()

    data = json.loads(args.preflight.read_text(encoding="utf-8-sig"))
    errors: list[str] = []

    if data.get("overall") != "PASS":
        errors.append(f"overall must be PASS, got {data.get('overall')!r}")
    if data.get("cg_full_enabled") is not True:
        errors.append("cg_full_enabled must be true")

    checks = data.get("checks")
    if not isinstance(checks, dict):
        errors.append("checks must be an object")
        checks = {}

    missing = sorted(REQUIRED - set(checks))
    if missing:
        errors.append("missing checks: " + ", ".join(missing))

    for name in sorted(REQUIRED & set(checks)):
        item = checks[name]
        status = item.get("status") if isinstance(item, dict) else None
        if status != "PASS":
            errors.append(f"{name} must be PASS, got {status!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PASS {args.preflight}: cg-full runtime gate satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
