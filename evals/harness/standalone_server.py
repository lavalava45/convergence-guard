#!/usr/bin/env python3
"""Manage the fixed local llama-server runtime used by main-v0.1.7."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import psutil
import requests


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUNS = ROOT / "evals" / "runs"
STATE = RUNS / "standalone-server.json"
LOG = RUNS / "standalone-server.log"
HOST = "127.0.0.1"
PORT = 55991
BASE_URL = f"http://{HOST}:{PORT}/v1"
BINARY = Path(
    r"C:\Users\dslava\.cache\lm-studio\extensions\backends\llama.cpp-win-x86_64-nvidia-cuda12-avx2-2.52.0\llama-server.exe"
)
MODEL = Path(r"D:\models\unsloth\gemma-4-12b-it-GGUF\gemma-4-12b-it-Q6_K.gguf")
MMPROJ = Path(r"D:\models\unsloth\gemma-4-12b-it-GGUF\mmproj-F32.gguf")
CHAT_TEMPLATE = ROOT / "evals" / "runtime-gemma4-chat-template.jinja"


def command() -> list[str]:
    return [
        str(BINARY),
        "--model", str(MODEL),
        "--host", HOST,
        "--port", str(PORT),
        "--verbosity", "2",
        "--no-webui",
        "--jinja",
        "--chat-template-file", str(CHAT_TEMPLATE),
        "--ctx-size", "15000",
        "--n-gpu-layers", "999999",
        "--n-cpu-moe", "0",
        "--main-gpu", "0",
        "--tensor-split", "0",
        "--split-mode", "layer",
        "--ctx-checkpoints", "0",
        "--batch-size", "2048",
        "--ubatch-size", "512",
        "--threads", "4",
        "--parallel", "1",
        "--cache-type-k", "f16",
        "--cache-type-v", "f16",
        "--mmproj", str(MMPROJ),
        "--flash-attn", "auto",
        "--kv-offload",
        "--kv-unified",
        "--load-mode", "mmap+mlock",
        "--no-cache-prompt",
        "--cache-ram", "0",
        "--no-cache-idle-slots",
    ]


def running_servers() -> list[psutil.Process]:
    return [
        p for p in psutil.process_iter(["pid", "name", "cmdline"])
        if p.info["name"] and p.info["name"].lower() == "llama-server.exe"
    ]


def wait_health(timeout: float = 45.0) -> None:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            r = requests.get(f"http://{HOST}:{PORT}/health", timeout=2)
            if r.ok:
                return
        except requests.RequestException as exc:
            last_error = exc
        time.sleep(0.5)
    raise RuntimeError(f"standalone llama-server did not become healthy: {last_error}")


def start() -> int:
    existing = running_servers()
    if existing:
        raise RuntimeError(
            "refusing to start with existing llama-server process(es): "
            + ", ".join(str(p.info["pid"]) for p in existing)
        )
    for path in (BINARY, MODEL, MMPROJ, CHAT_TEMPLATE):
        if not path.is_file():
            raise RuntimeError(f"missing runtime file: {path}")
    RUNS.mkdir(parents=True, exist_ok=True)
    log_handle = LOG.open("ab")
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(
        subprocess, "CREATE_NEW_PROCESS_GROUP", 0
    )
    proc = subprocess.Popen(
        command(),
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        creationflags=creationflags,
    )
    log_handle.close()
    STATE.write_text(
        json.dumps(
            {"pid": proc.pid, "base_url": BASE_URL, "port": PORT, "command": command()},
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )
    wait_health()
    print(f"STANDALONE READY pid={proc.pid} base={BASE_URL}")
    return 0


def status() -> int:
    servers = running_servers()
    print(json.dumps(
        [{"pid": p.info["pid"], "cmdline": p.info["cmdline"]} for p in servers],
        indent=2,
        ensure_ascii=False,
    ))
    try:
        r = requests.get(f"http://{HOST}:{PORT}/health", timeout=2)
        print(f"health={r.status_code} {r.text}")
    except requests.RequestException as exc:
        print(f"health=ERROR {exc}")
        return 1
    return 0


def stop() -> int:
    if not STATE.is_file():
        print("No standalone server state file.")
        return 0
    data = json.loads(STATE.read_text(encoding="utf-8"))
    pid = int(data["pid"])
    try:
        p = psutil.Process(pid)
    except psutil.NoSuchProcess:
        print(f"Standalone pid {pid} already exited.")
        return 0
    p.terminate()
    try:
        p.wait(10)
    except psutil.TimeoutExpired:
        p.kill()
        p.wait(5)
    print(f"STANDALONE STOPPED pid={pid}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "status", "stop"])
    args = parser.parse_args()
    if args.action == "start":
        return start()
    if args.action == "status":
        return status()
    return stop()


if __name__ == "__main__":
    raise SystemExit(main())
