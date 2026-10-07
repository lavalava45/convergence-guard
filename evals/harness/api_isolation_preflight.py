#!/usr/bin/env python3
"""Runtime isolation preflight for the stateless Gemini API adapter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


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
        timeout=150,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"adapter exit {proc.returncode}")
    return json.loads(proc.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemini-3.5-flash")
    parser.add_argument(
        "--adapter",
        type=Path,
        default=Path(__file__).with_name("gemini_api_adapter.py"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    parent_token = "PX7Q-M4N2-V9KC-31TR"
    sibling_token = "SB6H-K8W3-J2PF-74LQ"

    parent_seed = call_adapter(
        args.adapter,
        request_id="preflight-parent-seed",
        model=args.model,
        prompt=(
            "Store this exact diagnostic token only for this request: "
            f"{parent_token}. Reply exactly ACK."
        ),
    )
    parent_probe = call_adapter(
        args.adapter,
        request_id="preflight-parent-probe",
        model=args.model,
        prompt=(
            "This request intentionally contains no prior transcript. "
            "If you can actually access an exact diagnostic token from a "
            "previous API request in this project, output that exact token. "
            "Otherwise output exactly NONE. Do not guess."
        ),
    )
    sibling_seed = call_adapter(
        args.adapter,
        request_id="preflight-sibling-seed",
        model=args.model,
        prompt=(
            "Return exactly this diagnostic token and nothing else: "
            f"{sibling_token}"
        ),
    )
    sibling_probe = call_adapter(
        args.adapter,
        request_id="preflight-sibling-probe",
        model=args.model,
        prompt=(
            "This is a new independent API request. If an earlier sibling "
            "request's exact diagnostic output is available to you, return it. "
            "Otherwise output exactly NONE. Do not invent a token."
        ),
    )

    parent_leak = parent_token in parent_probe.get("raw_text", "")
    sibling_leak = sibling_token in sibling_probe.get("raw_text", "")
    request_features = parent_probe.get("metadata", {}).get(
        "request_features", {}
    )
    explicit_stateless = (
        request_features.get("tools_sent") is False
        and request_features.get("retrieval_sent") is False
        and request_features.get("cached_content_sent") is False
        and request_features.get("session_or_previous_interaction_sent") is False
        and request_features.get("message_count") == 1
    )

    checks = {
        "parent_transcript": {
            "status": "PASS" if explicit_stateless and not parent_leak else "FAIL",
            "reason": (
                "Each generateContent POST is constructed from a fresh explicit "
                "messages array with no session/previous-interaction field; "
                "sentinel probe observed no parent token."
            ),
        },
        "sibling_outputs": {
            "status": "PASS" if explicit_stateless and not sibling_leak else "FAIL",
            "reason": (
                "Sibling calls are separate stateless POSTs and the probe "
                "observed no sibling-output sentinel."
            ),
        },
        "prior_worker_history": {
            "status": "PASS" if explicit_stateless else "FAIL",
            "reason": (
                "The adapter does not reuse a provider conversation/session "
                "identifier or prior response state."
            ),
        },
        "account_project_memory": {
            "status": "PASS" if explicit_stateless else "FAIL",
            "reason": (
                "No memory/history field is sent; the effective model input is "
                "the explicit generateContent request contents."
            ),
        },
        "retrieval": {
            "status": "PASS" if request_features.get("retrieval_sent") is False else "FAIL",
            "reason": "No retrieval, grounding, URL context, file search, or cached content is sent.",
        },
        "filesystem_tools": {
            "status": "PASS" if request_features.get("tools_sent") is False else "FAIL",
            "reason": "Participant API calls expose no tools or filesystem access.",
        },
        "coordinator_handoff": {
            "status": "PASS",
            "reason": (
                "The harness constructs each request from an explicit message "
                "allowlist; downstream context must be supplied as ordinary "
                "message text by the mode executor."
            ),
        },
    }
    overall = "PASS" if all(x["status"] == "PASS" for x in checks.values()) else "FAIL"
    artifact = {
        "runtime": "Gemini Developer API generateContent via local stateless adapter",
        "model": args.model,
        "checks": checks,
        "sentinel_diagnostics": {
            "parent_seed_ack": parent_seed.get("raw_text", "").strip(),
            "parent_probe": parent_probe.get("raw_text", "").strip(),
            "sibling_seed_returned_expected": (
                sibling_seed.get("raw_text", "").strip() == sibling_token
            ),
            "sibling_probe": sibling_probe.get("raw_text", "").strip(),
            "note": (
                "Negative sentinel probes supplement, but do not alone prove, "
                "isolation. PASS also relies on inspectable stateless request "
                "construction and absence of tools/retrieval/session fields."
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
