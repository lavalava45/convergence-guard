#!/usr/bin/env python3
"""OpenAI-compatible LM Studio adapter for the eval harness."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
import copy
from typing import Any

import jsonschema


BASE_URL = os.environ.get("LMSTUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
API_KEY = os.environ.get("LMSTUDIO_API_KEY")


def main() -> int:
    request = json.load(sys.stdin)
    model = request["model"]
    settings = request.get("settings") or {}
    messages = request.get("messages") or []
    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": item["role"], "content": item["content"]}
            for item in messages
        ],
        "temperature": settings.get("temperature", 0.2),
        "max_tokens": settings.get("maxOutputTokens", 8192),
    }

    schema = request.get("response_schema")
    if schema:
        grammar_schema = schema
        # llama.cpp 2.52.0 resets the connection on the frozen calibration
        # schema when numeric minimum/maximum are present. Remove only those
        # two grammar constraints server-side; validate the returned object
        # locally against the untouched frozen schema below.
        if "calibration" in str(schema.get("title", "")).lower():
            grammar_schema = copy.deepcopy(schema)
            p_schema = (
                grammar_schema["properties"]["probabilities"]["items"]
                ["properties"]["p"]
            )
            p_schema.pop("minimum", None)
            p_schema.pop("maximum", None)
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "eval_response",
                "strict": True,
                "schema": grammar_schema,
            },
        }

    result = None
    last_error: Exception | None = None
    max_transport_attempts = int(settings.get("maxTransportAttempts", 5))
    if max_transport_attempts < 1:
        raise ValueError("maxTransportAttempts must be >= 1")
    transport_attempts = 0
    for attempt in range(1, max_transport_attempts + 1):
        transport_attempts = attempt
        req = urllib.request.Request(
            f"{BASE_URL}/chat/completions",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                **({"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}),
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=600) as response:
                result = json.loads(response.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"LM Studio HTTP {exc.code}: {detail}")
            transient_400 = (
                exc.code == 400
                and (
                    '"terminated"' in detail
                    or "fetch failed" in detail.lower()
                    or "engine protocol predict request failed" in detail.lower()
                )
            )
            transient_server = exc.code in {500, 502, 503, 504}
            if (transient_400 or transient_server) and attempt < max_transport_attempts:
                time.sleep(2 * attempt)
                continue
            raise last_error from exc
        except (urllib.error.URLError, ConnectionResetError, TimeoutError) as exc:
            last_error = exc
            if attempt < max_transport_attempts:
                time.sleep(2 * attempt)
                continue
            raise RuntimeError(f"LM Studio connection failed: {exc}") from exc
    if result is None:
        raise RuntimeError(f"LM Studio request failed after retries: {last_error}")

    choice = result["choices"][0]
    message = choice.get("message") or {}
    if schema and "calibration" in str(schema.get("title", "")).lower():
        jsonschema.validate(json.loads(message.get("content") or ""), schema)
    usage = result.get("usage") or {}
    details = usage.get("completion_tokens_details") or {}
    envelope = {
        "raw_text": message.get("content") or "",
        "model": result.get("model") or model,
        "provider_request_id": result.get("id"),
        "usage": {
            "input_tokens": usage.get("prompt_tokens", "unavailable"),
            "output_tokens": usage.get("completion_tokens", "unavailable"),
            "reasoning_tokens": details.get("reasoning_tokens", 0),
            "cached_tokens": "unavailable",
            "cost": 0.0,
        },
        "metadata": {
            "finish_reason": choice.get("finish_reason"),
            "local_runtime": "LM Studio",
            "base_url": BASE_URL,
            "request_features": {
                "message_count": len(messages),
                "tools_sent": False,
                "retrieval_sent": False,
                "cached_content_sent": False,
                "session_or_previous_interaction_sent": False,
            },
            "transport_attempts": transport_attempts,
        },
    }
    # Keep the subprocess transport ASCII-only on Windows. The parent runner
    # decodes stdout as UTF-8; escaping non-ASCII here avoids dependence on the
    # active Windows console code page without changing the parsed JSON value.
    print(json.dumps(envelope, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
