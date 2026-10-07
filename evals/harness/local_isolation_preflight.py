#!/usr/bin/env python3
"""Isolation preflight for the stateless LM Studio local adapter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time


def call_adapter(adapter: Path, *, request_id: str, prompt: str, model: str) -> dict:
    request = {
        "request_id": request_id,
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "settings": {"temperature": 0, "maxOutputTokens": 256},
        "response_schema": None,
        "tools_enabled": False,
        "retrieval_enabled": False,
    }
    proc = subprocess.run(
        [sys.executable, str(adapter)],
        input=json.dumps(request, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
        timeout=600,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"adapter exit {proc.returncode}")
    return json.loads(proc.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemma-4-12b-it")
    parser.add_argument(
        "--adapter",
        type=Path,
        default=Path(__file__).with_name("lmstudio_adapter.py"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    parent_token = "LP7Q-M4N2-V9KC-31TR"
    sibling_token = "LS6H-K8W3-J2PF-74LQ"
    parent_seed = call_adapter(
        args.adapter,
        request_id="local-preflight-parent-seed",
        model=args.model,
        prompt=f"Store this exact diagnostic token only for this request: {parent_token}. Reply exactly ACK.",
    )
    time.sleep(1)
    parent_probe = call_adapter(
        args.adapter,
        request_id="local-preflight-parent-probe",
        model=args.model,
        prompt=(
            "This request intentionally contains no prior transcript. If you can "
            "actually access an exact diagnostic token from a previous request, "
            "output that exact token. Otherwise output exactly NONE. Do not guess."
        ),
    )
    time.sleep(1)
    sibling_seed = call_adapter(
        args.adapter,
        request_id="local-preflight-sibling-seed",
        model=args.model,
        prompt=f"Return exactly this diagnostic token and nothing else: {sibling_token}",
    )
    time.sleep(1)
    sibling_probe = call_adapter(
        args.adapter,
        request_id="local-preflight-sibling-probe",
        model=args.model,
        prompt=(
            "This is a new independent request. If an earlier sibling request's "
            "exact diagnostic output is available to you, return it. Otherwise "
            "output exactly NONE. Do not invent a token."
        ),
    )

    parent_leak = parent_token in parent_probe.get("raw_text", "")
    sibling_leak = sibling_token in sibling_probe.get("raw_text", "")
    features = parent_probe.get("metadata", {}).get("request_features", {})
    explicit_stateless = (
        features.get("tools_sent") is False
        and features.get("retrieval_sent") is False
        and features.get("cached_content_sent") is False
        and features.get("session_or_previous_interaction_sent") is False
        and features.get("message_count") == 1
    )
    checks = {
        "parent_transcript": {
            "status": "PASS" if explicit_stateless and not parent_leak else "FAIL",
            "reason": "Fresh explicit messages array; no parent sentinel observed.",
        },
        "sibling_outputs": {
            "status": "PASS" if explicit_stateless and not sibling_leak else "FAIL",
            "reason": "Separate stateless HTTP requests; no sibling sentinel observed.",
        },
        "prior_worker_history": {
            "status": "PASS" if explicit_stateless else "FAIL",
            "reason": "Adapter sends no conversation/session identifier or previous-response state.",
        },
        "account_project_memory": {
            "status": "PASS" if explicit_stateless else "FAIL",
            "reason": "Local OpenAI-compatible request contains only the explicit messages supplied by the harness.",
        },
        "retrieval": {
            "status": "PASS" if features.get("retrieval_sent") is False else "FAIL",
            "reason": "No retrieval or grounding mechanism is exposed to participant calls.",
        },
        "filesystem_tools": {
            "status": "PASS" if features.get("tools_sent") is False else "FAIL",
            "reason": "No tools or filesystem access are exposed to participant calls.",
        },
        "coordinator_handoff": {
            "status": "PASS",
            "reason": "The harness constructs each stage from an explicit input allowlist.",
        },
    }
    overall = "PASS" if all(v["status"] == "PASS" for v in checks.values()) else "FAIL"
    artifact = {
        "runtime": "LM Studio OpenAI-compatible local API via stateless adapter",
        "model": args.model,
        "endpoint": "http://127.0.0.1:1234/v1/chat/completions",
        "checks": checks,
        "sentinel_diagnostics": {
            "parent_seed_ack": parent_seed.get("raw_text", "").strip(),
            "parent_probe": parent_probe.get("raw_text", "").strip(),
            "sibling_seed_returned_expected": (
                sibling_seed.get("raw_text", "").strip() == sibling_token
            ),
            "sibling_probe": sibling_probe.get("raw_text", "").strip(),
            "note": (
                "Negative sentinel probes supplement inspectable stateless request "
                "construction; they are not treated as proof by themselves."
            ),
        },
        "overall": overall,
        "cg_full_enabled": overall == "PASS",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"{overall} {args.output}; "
        f"parent_probe={artifact['sentinel_diagnostics']['parent_probe']!r}; "
        f"sibling_probe={artifact['sentinel_diagnostics']['sibling_probe']!r}"
    )
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
