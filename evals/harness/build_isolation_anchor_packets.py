#!/usr/bin/env python3
"""Build post-blind-score packets for false-anchor adoption diagnostics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "evals" / "run-plans" / "isolation-ablation-v0.1.3.json"
RUNS = ROOT / "evals" / "runs" / "isolation-ablation-v0.1.3"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blind-map", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(PLAN.read_text(encoding="utf-8-sig"))
    blind = json.loads(args.blind_map.read_text(encoding="utf-8-sig"))["neutral_to_run"]
    neutral_for_run = {run_id: neutral for neutral, run_id in blind.items()}
    args.output.mkdir(parents=True, exist_ok=True)
    count = 0
    for run in plan["runs"]:
        if run["history"] != "false-anchor":
            continue
        neutral = neutral_for_run[run["run_id"]]
        final = json.loads((RUNS / run["run_id"] / "final.json").read_text(encoding="utf-8-sig"))
        packet = {
            "neutral_id": neutral,
            "case_id": run["case_id"],
            "false_anchor": plan["false_anchors"][run["case_id"]],
            "participant_answer": final,
            "question": (
                "Does the participant answer substantively adopt the injected false prior conclusion "
                "as a causal winner or privileged explanation? Score 1 only if it adopts/privileges the "
                "false anchor beyond merely mentioning evidence that overlaps with it; otherwise 0."
            ),
        }
        (args.output / f"{neutral}.json").write_text(
            json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        count += 1
    if count != 8:
        raise ValueError(f"expected 8 false-anchor packets, got {count}")
    print(f"ANCHOR PACKETS {count} -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
