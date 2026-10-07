#!/usr/bin/env python3
"""Deterministic treatment-independent final-answer normalization."""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
from typing import Any

NORMALIZATION_VERSION = "v0.1"


def normalize(data: Any) -> tuple[Any, list[dict[str, Any]]]:
    normalized = deepcopy(data)
    repairs: list[dict[str, Any]] = []
    if not isinstance(normalized, dict):
        return normalized, repairs
    causal = normalized.get("causal_assessment")
    if not isinstance(causal, dict):
        return normalized, repairs
    status = causal.get("status")
    preferred = causal.get("preferred_cause")
    if status in {"COEXIST", "INSUFFICIENT"} and preferred is not None:
        causal["preferred_cause"] = None
        repairs.append(
            {
                "rule": "N1",
                "path": "causal_assessment.preferred_cause",
                "before": preferred,
                "after": None,
                "reason": f"{status} cannot designate a single preferred cause under the frozen output contract",
            }
        )
    return normalized, repairs


def normalize_artifact(raw_path: Path, final_path: Path, audit_path: Path) -> int:
    data = json.loads(raw_path.read_text(encoding="utf-8-sig"))
    normalized, repairs = normalize(data)
    final_path.write_text(
        json.dumps(normalized, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    audit = {
        "normalization_version": NORMALIZATION_VERSION,
        "source": raw_path.name,
        "output": final_path.name,
        "repair_count": len(repairs),
        "repairs": repairs,
    }
    audit_path.write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return len(repairs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()
    count = normalize_artifact(args.raw_json, args.output, args.audit)
    print(
        f"NORMALIZED {args.raw_json} -> {args.output}; "
        f"version={NORMALIZATION_VERSION}; repairs={count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
