#!/usr/bin/env python3
"""Build private neutral blind-judge packets for isolation-ablation-v0.1.4."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "evals" / "cases" / "main"
RUNS = ROOT / "evals" / "runs" / "isolation-ablation-v0.1.4"
RUBRIC = ROOT / "evals" / "protocol" / "v0.2" / "ISOLATION-JUDGE-RUBRIC-v0.1.md"


def case_material(case_id: str) -> str:
    case_dir = CASES / case_id
    parts = [(case_dir / "prompt.md").read_text(encoding="utf-8-sig").strip()]
    for path in sorted((case_dir / "evidence").iterdir()):
        if path.is_file():
            parts.append(f"## {path.name}\n\n" + path.read_text(encoding="utf-8-sig").strip())
    return "\n\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blind-map", type=Path, required=True)
    parser.add_argument("--private-keys", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    blind = json.loads(args.blind_map.read_text(encoding="utf-8-sig"))
    mapping = blind["neutral_to_run"]
    if len(mapping) != 16:
        raise ValueError("expected 16 blind IDs")
    rubric = RUBRIC.read_text(encoding="utf-8-sig")
    args.output.mkdir(parents=True, exist_ok=True)
    for neutral_id, run_id in sorted(mapping.items()):
        run_dir = RUNS / run_id
        manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8-sig"))
        if manifest.get("status") != "complete":
            raise ValueError(f"run not complete: {run_id}")
        case_id = manifest["case_id"]
        final = json.loads((run_dir / "final.json").read_text(encoding="utf-8-sig"))
        key = json.loads((args.private_keys / case_id / "key.json").read_text(encoding="utf-8-sig"))
        packet = {
            "neutral_id": neutral_id,
            "case_id": case_id,
            "public_case": case_material(case_id),
            "hidden_key": key,
            "judge_rubric": rubric,
            "participant_answer": final,
        }
        (args.output / f"{neutral_id}.json").write_text(
            json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    print(f"PACKETS {len(mapping)} -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
