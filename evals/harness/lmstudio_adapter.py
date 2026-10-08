#!/usr/bin/env python3
"""Streaming OpenAI-compatible LM Studio adapter for the eval harness."""

from __future__ import annotations

import json
import os
import sys
import time
import copy
from typing import Any

import jsonschema
import requests


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
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    if "seed" in settings:
        payload["seed"] = settings["seed"]

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
        try:
            with requests.post(
                f"{BASE_URL}/chat/completions",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    **({"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}),
                },
                stream=True,
                timeout=(10, 180),
            ) as response:
                response.raise_for_status()
                pieces: list[str] = []
                usage: dict[str, Any] = {}
                provider_request_id = None
                result_model = model
                finish_reason = None
                for raw_line in response.iter_lines(decode_unicode=True):
                    if raw_line is None:
                        continue
                    line = raw_line.strip()
                    if not line or not line.startswith("data: "):
                        continue
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    event = json.loads(data)
                    provider_request_id = event.get("id") or provider_request_id
                    result_model = event.get("model") or result_model
                    if event.get("usage"):
                        usage = event["usage"]
                    choices = event.get("choices") or []
                    if choices:
                        choice = choices[0]
                        delta = choice.get("delta") or {}
                        content = delta.get("content")
                        if content:
                            pieces.append(content)
                        if choice.get("finish_reason") is not None:
                            finish_reason = choice.get("finish_reason")
                raw_text = "".join(pieces)
                if not raw_text or finish_reason is None:
                    raise RuntimeError(
                        "LM Studio streaming response ended before a complete answer"
                    )
                result = {
                    "id": provider_request_id,
                    "model": result_model,
                    "choices": [
                        {
                            "message": {"content": raw_text},
                            "finish_reason": finish_reason,
                        }
                    ],
                    "usage": usage,
                }
            break
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else 0
            detail = exc.response.text if exc.response is not None else str(exc)
            last_error = RuntimeError(f"LM Studio HTTP {status}: {detail}")
            transient_400 = (
                status == 400
                and (
                    '"terminated"' in detail
                    or "fetch failed" in detail.lower()
                    or "engine protocol predict request failed" in detail.lower()
                )
            )
            transient_server = status in {500, 502, 503, 504}
            if (transient_400 or transient_server) and attempt < max_transport_attempts:
                time.sleep(2 * attempt)
                continue
            raise last_error from exc
        except (
            requests.ConnectionError,
            requests.exceptions.ChunkedEncodingError,
            requests.Timeout,
            ConnectionResetError,
            TimeoutError,
        ) as exc:
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
            "local_runtime": "standalone llama-server 2.52.0",
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
