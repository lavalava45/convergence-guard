#!/usr/bin/env python3
"""Create a deterministic blocked run plan for the comparative eval."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

MODES = [
    "single-context",
    "shared-context-multi-agent",
    "cg-reduced",
    "cg-full",
]


def discover_cases(root: Path) -> list[str]:
    cases: list[str] = []
    for case_file in sorted(root.glob("*/case.json")):
        data = json.loads(case_file.read_text(encoding="utf-8-sig"))
        case_id = data.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{case_file}: missing non-empty case_id")
        cases.append(case_id)
    if not cases:
        raise ValueError(f"No case.json files found under {root}")
    if len(cases) != len(set(cases)):
        raise ValueError("Duplicate case_id values found")
    return cases


def build_plan(case_ids: list[str], repeats: int, seed: int) -> dict:
    rng = random.Random(seed)
    blocks = []
    ordinal = 1

    for repeat in range(1, repeats + 1):
        for case_id in case_ids:
            order = MODES.copy()
            rng.shuffle(order)
            runs = []
            for mode in order:
                runs.append(
                    {
                        "ordinal": ordinal,
                        "run_id": f"{case_id}-r{repeat}-{mode}",
                        "case_id": case_id,
                        "repeat": repeat,
                        "mode": mode,
                        "status": "planned",
                    }
                )
                ordinal += 1
            blocks.append(
                {
                    "block_id": f"{case_id}-r{repeat}",
                    "case_id": case_id,
                    "repeat": repeat,
                    "runs": runs,
                }
            )

    return {
        "design": "blocked-randomization",
        "seed": seed,
        "modes": MODES,
        "repeats": repeats,
        "case_count": len(case_ids),
        "run_count": ordinal - 1,
        "blocks": blocks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--repeats", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.repeats < 1:
        parser.error("--repeats must be >= 1")

    plan = build_plan(discover_cases(args.cases), args.repeats, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {plan['run_count']} runs to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
