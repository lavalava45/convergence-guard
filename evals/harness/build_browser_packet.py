#!/usr/bin/env python3
"""Build the manual browser packet for the first Reduced-Mode pilot run."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()

    case_dir = repo / "evals" / "cases" / "pilot" / "P01"
    evidence = sorted((case_dir / "evidence").iterdir())

    parts = [
        "# Browser Pilot Packet 001\n\n",
        "RUN_ID: P01-r1-cg-reduced\n",
        "CASE_ID: P01\n",
        "MODE: cg-reduced\n",
        f"CG_COMMIT: {commit}\n\n",
        "## Participant wrapper\n\n",
        "This is a controlled evaluation run.\n\n",
        "Use only the material in this packet. Do not browse the web, use Connected Apps, retrieve other chats, or add facts from outside the packet.\n\n",
        "Treatment: **Convergence Guard — Reduced Mode (no independent worker isolation)**.\n\n",
        "Execute the Reduced Mode protocol in this single conversation. The embedded Convergence Guard files are the operational instructions for this treatment. Where the full skill discusses Full Mode isolation, do not claim those guarantees; follow the Reduced Mode fallback rules.\n\n",
        "Do not ask the user questions. Do not request more files. Do not reveal or discuss the evaluation design.\n\n",
        "At the end, return **exactly one JSON object and nothing else**. Do not wrap it in Markdown fences. The JSON must conform to the embedded OUTPUT-SCHEMA and use `case_id` = `P01`.\n\n",
        "---\n\n# PARTICIPANT-VISIBLE CASE\n\n",
        read(case_dir / "prompt.md"),
    ]

    for path in evidence:
        evidence_id = path.name[:3]
        parts.extend([f"\n## Evidence {evidence_id}\n\n", read(path)])

    inclusions = [
        ("CONVERGENCE GUARD SKILL", repo / "convergence-guard" / "SKILL.md"),
        ("REDUCED MODE REFERENCE", repo / "convergence-guard" / "references" / "reduced-mode.md"),
        ("PROTOCOL DETAILS", repo / "convergence-guard" / "references" / "protocol-details.md"),
        ("REQUIRED FINAL OUTPUT SCHEMA", repo / "evals" / "protocol" / "OUTPUT-SCHEMA.json"),
    ]
    for title, path in inclusions:
        parts.extend([f"\n---\n\n# {title}\n\n", read(path)])

    parts.append(
        """
---

# FINAL EXECUTION REMINDER

Perform the P01 analysis now in **Convergence Guard Reduced Mode** using only this packet.

Return exactly one JSON object, no Markdown and no prose outside the JSON.

Structural rules:
- `case_id` must be `P01`.
- `candidate_causes[].id` must be short neutral IDs such as `C1`, `C2`.
- If `status` is `CHOOSE`, `preferred_cause` must equal one candidate ID.
- If `status` is `COEXIST` or `INSUFFICIENT`, `preferred_cause` must be null.
- Cite only evidence IDs E01, E02, E03, E04.
- Do not alter your answer later unless the user explicitly starts a new run; the primary answer will be frozen before calibration.
"""
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {args.output} from CG commit {commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
