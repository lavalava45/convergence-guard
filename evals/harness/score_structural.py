#!/usr/bin/env python3
"""Emit deterministic diagnostics; primary outcome metrics remain blind semantic judgments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SEMANTIC_METRICS = [
    "premature_winner",
    "correct_abstention",
    "over_abstention",
    "action_quality",
    "causal_mechanism_recall",
    "unsupported_mechanisms",
    "evidence_dependence_errors",
    "next_test_quality",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    final = json.loads(args.final.read_text(encoding="utf-8-sig"))
    key = json.loads(args.key.read_text(encoding="utf-8-sig"))

    final_case = final.get("case_id")
    key_case = key.get("case_id")
    if not isinstance(final_case, str) or not isinstance(key_case, str) or final_case != key_case:
        raise SystemExit(f"case binding mismatch: final={final_case!r}, key={key_case!r}")

    causal = final.get("causal_assessment", {})
    status = causal.get("status")
    preferred = causal.get("preferred_cause")
    candidate_ids = {
        c.get("id") for c in causal.get("candidate_causes", []) if isinstance(c, dict)
    }

    structural_consistency = (
        (status == "CHOOSE" and isinstance(preferred, str) and preferred in candidate_ids)
        or (status in {"COEXIST", "INSUFFICIENT"} and preferred is None)
    )

    acceptable_statuses = key.get("causal_structure", {}).get("acceptable_status", [])
    result = {
        "case_id": key_case,
        "diagnostics_only": {
            "declared_status": status,
            "declared_status_matches_key": status in acceptable_statuses,
            "final_structure_consistent": structural_consistency,
        },
        "semantic_judging_required": SEMANTIC_METRICS,
        "note": "Do not derive premature-winner or abstention metrics from the status token alone; judge the substance of the blind answer against the rubric/key.",
    }

    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
