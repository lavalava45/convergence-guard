#!/usr/bin/env python3
"""Create a run manifest skeleton from one run-plan entry."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_tree(case_dir: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in case_dir.rglob("*") if p.is_file()):
        digest.update(path.relative_to(case_dir).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--eval-version", default="0.1-pilot")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8-sig"))
    selected = None
    for block in plan["blocks"]:
        for run in block["runs"]:
            if run["run_id"] == args.run_id:
                selected = run
                break
    if selected is None:
        raise SystemExit(f"run_id not found: {args.run_id}")

    case_dir = args.cases / selected["case_id"]
    manifest = {
        "run_id": selected["run_id"],
        "case_id": selected["case_id"],
        "mode": selected["mode"],
        "repeat": selected["repeat"],
        "eval_version": args.eval_version,
        "model": None,
        "model_settings": None,
        "case_hash": sha256_tree(case_dir),
        "protocol_hash": None,
        "start_time": None,
        "end_time": None,
        "status": "planned",
        "isolation_preflight": (
            "NOT_RUN" if selected["mode"] == "cg-full" else "NOT_APPLICABLE"
        ),
        "usage": {
            "input_tokens": "unavailable",
            "output_tokens": "unavailable",
            "reasoning_tokens": "unavailable",
            "cached_tokens": "unavailable",
            "model_calls": 0,
            "retries": 0,
            "cost": "unavailable",
            "wall_clock_seconds": "unavailable"
        }
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote manifest skeleton to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
