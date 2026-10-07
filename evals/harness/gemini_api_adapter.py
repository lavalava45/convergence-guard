#!/usr/bin/env python3
"""Gemini Developer API adapter for the provider-neutral eval runtime.

Reads one ModelRequest JSON object from stdin and emits one ModelResponse-like
JSON object to stdout. The API key is read from a private file outside the
repository by default, or from CG_GEMINI_KEY_FILE when set.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request


DEFAULT_KEY_FILE = (
    Path(__file__).resolve().parents[3]
    / "_cg-eval-private"
    / "gemini-api-key-2.txt"
)


def key_file() -> Path:
    configured = os.environ.get("CG_GEMINI_KEY_FILE")
    return Path(configured) if configured else DEFAULT_KEY_FILE


def load_key() -> str:
    path = key_file()
    key = path.read_text(encoding="ascii").strip()
    if not key:
        raise RuntimeError(f"empty Gemini API key file: {path}")
    return key


def api_post(model: str, payload: dict) -> dict:
    key = load_key()
    model_id = model.removeprefix("models/")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model_id}:generateContent"
    )
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": key,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini API HTTP {exc.code}: {detail}") from exc


def main() -> int:
    request_data = json.load(sys.stdin)
    model = request_data["model"]
    messages = request_data.get("messages", [])
    settings = request_data.get("settings") or {}
    response_schema = request_data.get("response_schema")

    contents = []
    for message in messages:
        role = message.get("role", "user")
        # Gemini generateContent accepts user/model roles. Treat system-like
        # eval instructions as user content unless a future frozen adapter
        # explicitly uses systemInstruction.
        if role not in {"user", "model"}:
            role = "user"
        contents.append(
            {
                "role": role,
                "parts": [{"text": str(message.get("content", ""))}],
            }
        )

    generation_config = dict(settings)
    if response_schema is not None:
        generation_config["responseMimeType"] = "application/json"
        generation_config["responseSchema"] = response_schema

    payload = {"contents": contents}
    if generation_config:
        payload["generationConfig"] = generation_config

    response = api_post(model, payload)
    parts = (
        response.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [])
    )
    raw_text = "".join(
        part.get("text", "") for part in parts if isinstance(part, dict)
    )
    usage = response.get("usageMetadata") or {}
    out = {
        "raw_text": raw_text,
        "model": response.get("modelVersion") or model,
        "provider_request_id": response.get("responseId"),
        "usage": {
            "input_tokens": usage.get("promptTokenCount", "unavailable"),
            "output_tokens": usage.get("candidatesTokenCount", "unavailable"),
            "reasoning_tokens": usage.get("thoughtsTokenCount", "unavailable"),
            "cached_tokens": usage.get("cachedContentTokenCount", "unavailable"),
            "cost": "unavailable",
        },
        "metadata": {
            "finish_reason": (
                response.get("candidates", [{}])[0].get("finishReason")
            ),
            "total_token_count": usage.get("totalTokenCount", "unavailable"),
            "request_features": {
                "message_count": len(contents),
                "tools_sent": False,
                "retrieval_sent": False,
                "cached_content_sent": False,
                "session_or_previous_interaction_sent": False,
            },
        },
    }
    json.dump(out, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
