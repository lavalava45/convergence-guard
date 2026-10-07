#!/usr/bin/env python3
"""Create neutral answer IDs while keeping the identifying map private."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def collect_run_ids(plan: dict) -> list[str]:
    run_ids: list[str] = []
    for block in plan.get("blocks", []):
        for run in block.get("runs", []):
            run_id = run.get("run_id")
            if not isinstance(run_id, str) or not run_id:
                raise ValueError("run plan contains a run without run_id")
            run_ids.append(run_id)
    if len(run_ids) != len(set(run_ids)):
        raise ValueError("run plan contains duplicate run_id values")
    return run_ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--public", type=Path, required=True)
    parser.add_argument("--private-map", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8-sig"))
    run_ids = collect_run_ids(plan)

    pool = run_ids.copy()
    random.Random(args.seed).shuffle(pool)
    mapping = {f"R{i:04d}": run_id for i, run_id in enumerate(pool, start=1)}

    args.public.parent.mkdir(parents=True, exist_ok=True)
    args.private_map.parent.mkdir(parents=True, exist_ok=True)
    args.public.write_text(
        json.dumps(
            {"seed": args.seed, "blind_ids": sorted(mapping)}, indent=2
        ) + "\n",
        encoding="utf-8",
    )
    args.private_map.write_text(
        json.dumps(
            {"seed": args.seed, "blind_to_run": mapping}, indent=2
        ) + "\n",
        encoding="utf-8",
    )
    print(f"Created {len(mapping)} blind IDs")
    print(f"Public list: {args.public}")
    print(f"Private mapping: {args.private_map}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
