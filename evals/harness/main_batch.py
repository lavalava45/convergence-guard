#!/usr/bin/env python3
"""Execute the frozen main-v0.1.7 primary plan against standalone llama-server."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time

import psutil


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PLAN = ROOT / "evals" / "run-plans" / "main-v0.1.json"
RUNNER = HERE / "main_runner.py"


def discover_backend() -> tuple[int, str, str | None, list[str]]:
    servers = [
        p
        for p in psutil.process_iter(["pid", "name", "cmdline"])
        if p.info["name"] and p.info["name"].lower() == "llama-server.exe"
    ]
    if len(servers) != 1:
        raise RuntimeError(f"expected exactly one loaded llama-server; found {len(servers)}")
    proc = servers[0]
    cmd = proc.info["cmdline"] or []
    port = cmd[cmd.index("--port") + 1]
    key = cmd[cmd.index("--api-key") + 1] if "--api-key" in cmd else None
    return int(proc.info["pid"]), port, key, cmd


def validate_load_profile(cmd: list[str]) -> None:
    joined = " ".join(cmd)
    required = (
        "gemma-4-12b-it-Q6_K.gguf",
        "--ctx-size 15000",
        "--n-gpu-layers 999999",
        "--kv-offload",
        "--parallel 1",
        "--no-cache-prompt",
        "--cache-ram 0",
        "--no-cache-idle-slots",
    )
    missing = [item for item in required if item not in joined]
    if missing:
        raise RuntimeError(f"loaded backend does not match frozen profile; missing {missing}")
    if "--no-kv-offload" in joined:
        raise RuntimeError("loaded backend has KV offload disabled")


def main() -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8-sig"))
    runs = [run for block in plan["blocks"] for run in block["runs"]]
    if len(runs) != 32 or any(run["repeat"] != 1 for run in runs):
        raise RuntimeError("main-v0.1.7 requires exactly 32 repeat-1 runs")

    pid, port, key, cmd = discover_backend()
    validate_load_profile(cmd)
    env = dict(os.environ)
    env["LMSTUDIO_BASE_URL"] = f"http://127.0.0.1:{port}/v1"
    if key:
        env["LMSTUDIO_API_KEY"] = key
    else:
        env.pop("LMSTUDIO_API_KEY", None)
    print(f"MAIN v0.1.7 PRIMARY START pid={pid} runs={len(runs)}", flush=True)

    started = time.perf_counter()
    for idx, run in enumerate(runs, start=1):
        before_pid, _, _, before_cmd = discover_backend()
        if before_pid != pid:
            raise RuntimeError(f"backend PID changed before run {idx}: {pid} -> {before_pid}")
        validate_load_profile(before_cmd)
        print(f"[{idx:02d}/32] START {run['run_id']}", flush=True)
        t0 = time.perf_counter()
        proc = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--run-id",
                run["run_id"],
                "--execute",
                "--defer-calibration",
            ],
            cwd=ROOT,
            env=env,
            text=True,
            check=False,
        )
        elapsed = time.perf_counter() - t0
        print(f"[{idx:02d}/32] END rc={proc.returncode} elapsed={elapsed:.1f}s", flush=True)
        if proc.returncode != 0:
            print("BATCH STOPPED ON FIRST NON-COMPLETE RUN", flush=True)
            return proc.returncode

    total = time.perf_counter() - started
    print(f"MAIN v0.1.7 PRIMARY COMPLETE runs=32 elapsed={total:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
