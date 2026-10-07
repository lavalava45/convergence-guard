#!/usr/bin/env python3
"""Build a reproducibility manifest without executing participant runs."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def sha256_tree(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        h.update(path.relative_to(root).as_posix().encode())
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def git_output(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=True
    )
    return proc.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--private-main", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-seed", type=int, required=True)
    parser.add_argument("--blind-seed", type=int, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    evals = repo / "evals"
    manifest = {
        "freeze_status": "frozen",
        "benchmark_version": "main-v0.1.3",
        "repository_head": git_output(repo, "rev-parse", "HEAD"),
        "repository_dirty": bool(git_output(repo, "status", "--porcelain")),
        "hashes": {
            "public_main_cases_sha256": sha256_tree(evals / "cases" / "main"),
            "public_main_calibration_sha256": sha256_tree(evals / "calibration" / "main"),
            "protocol_sha256": sha256_tree(evals / "protocol"),
            "harness_sha256": sha256_tree(evals / "harness"),
            "cg_under_test_sha256": sha256_tree(repo / "convergence-guard"),
            "private_main_tree_sha256": sha256_tree(args.private_main),
        },
        "runtime": {
            "name": "LM Studio direct loaded llama-server OpenAI-compatible API",
            "model": "gemma-4-12b-it",
            "model_file": "gemma-4-12b-it-Q6_K.gguf",
            "context_size": 15000,
            "gpu_layers": "all (--n-gpu-layers 999999)",
            "kv_offload": True,
            "parallel_slots": 1,
            "temperature": 0.2,
            "tools_enabled": False,
            "retrieval_enabled": False,
            "isolation_preflight": "evals/preflight/lmstudio-local-2026-10-07.json",
        },
        "resource_budget": {
            "policy": "evals/protocol/RESOURCE-BUDGET-v0.1.md",
            "primary_max_model_calls": 12,
            "primary_max_output_tokens": 32768,
            "calibration_max_model_calls": 2,
            "calibration_max_output_tokens": 1024,
        },
        "normalization_version": "v0.1",
        "randomization": {
            "run_plan_seed": args.run_seed,
            "blind_id_seed": args.blind_seed,
            "run_plan": "evals/run-plans/main-v0.1.json",
        },
        "design": {
            "case_count": 8,
            "modes": [
                "single-context",
                "shared-context-multi-agent",
                "cg-reduced",
                "cg-full",
            ],
            "repeats": 1,
            "run_count": 32,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote frozen benchmark manifest to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
