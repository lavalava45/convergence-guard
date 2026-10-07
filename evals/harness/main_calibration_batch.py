#!/usr/bin/env python3
"""Calibrate frozen main-v0.1.5 primary results without rerunning them."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import psutil


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PLAN = ROOT / "evals" / "run-plans" / "main-v0.1.json"
RUNNER = HERE / "main_runner.py"


def backend_env() -> tuple[int, dict[str, str]]:
    servers = [
        p for p in psutil.process_iter(["pid", "name", "cmdline"])
        if p.info["name"] and p.info["name"].lower() == "llama-server.exe"
    ]
    if len(servers) != 1:
        raise RuntimeError(f"expected exactly one loaded llama-server; found {len(servers)}")
    p = servers[0]
    cmd = p.info["cmdline"] or []
    env = dict(os.environ)
    env["LMSTUDIO_BASE_URL"] = f"http://127.0.0.1:{cmd[cmd.index('--port') + 1]}/v1"
    env["LMSTUDIO_API_KEY"] = cmd[cmd.index("--api-key") + 1]
    return int(p.info["pid"]), env


def main() -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8-sig"))
    runs = [run for block in plan["blocks"] for run in block["runs"]]
    if len(runs) != 32:
        raise RuntimeError("expected frozen 32-run main plan")
    pid, env = backend_env()
    failures: list[str] = []
    print(f"MAIN v0.1.5 CALIBRATION START pid={pid} runs=32", flush=True)
    for idx, run in enumerate(runs, start=1):
        print(f"[{idx:02d}/32] CAL {run['run_id']}", flush=True)
        proc = subprocess.run(
            [sys.executable, str(RUNNER), "--run-id", run["run_id"], "--calibrate-existing"],
            cwd=ROOT,
            env=env,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            failures.append(run["run_id"])
    print(f"MAIN v0.1.5 CALIBRATION END failures={len(failures)}", flush=True)
    if failures:
        print("FAILED CALIBRATIONS: " + ", ".join(failures), flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
