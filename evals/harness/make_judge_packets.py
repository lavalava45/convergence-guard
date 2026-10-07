#!/usr/bin/env python3
"""Build blind semantic-judge packets after participant runs are complete."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def case_material(case_dir: Path) -> dict:
    evidence = []
    for path in sorted((case_dir / "evidence").iterdir()):
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
        "prompt": (case_dir / "prompt.md").read_text(encoding="utf-8-sig"),
        "evidence": evidence,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--blind-map", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--runs", type=Path, required=True)
    parser.add_argument("--private-keys", type=Path, required=True)
    parser.add_argument("--rubric", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8-sig"))
    blind = json.loads(args.blind_map.read_text(encoding="utf-8-sig"))["blind_to_run"]
    planned = {
        run["run_id"]: run
        for block in plan["blocks"]
        for run in block["runs"]
    }
    if set(blind.values()) != set(planned):
        raise SystemExit("blind map and run plan contain different run IDs")

    rubric_text = args.rubric.read_text(encoding="utf-8-sig")
    args.output.mkdir(parents=True, exist_ok=True)
    count = 0
    for neutral_id, run_id in sorted(blind.items()):
        run = planned[run_id]
        case_id = run["case_id"]
        final_path = args.runs / case_id / f"r{run['repeat']}" / run["mode"] / "final.json"
        if not final_path.is_file():
            raise SystemExit(f"missing normalized final for {run_id}: {final_path}")
        key_path = args.private_keys / case_id / "key.json"
        if not key_path.is_file():
            raise SystemExit(f"missing private key for {case_id}: {key_path}")

        packet = {
            "neutral_id": neutral_id,
            "case": case_material(args.cases / case_id),
            "private_key": json.loads(key_path.read_text(encoding="utf-8-sig")),
            "blind_judge_rubric": rubric_text,
            "participant_answer": json.loads(final_path.read_text(encoding="utf-8-sig")),
        }
        (args.output / f"{neutral_id}.json").write_text(
            json.dumps(packet, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        count += 1

    print(f"Created {count} blind judge packets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
