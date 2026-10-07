#!/usr/bin/env python3
"""Provider-neutral runtime adapter contract for automated eval execution.

The harness can bind this contract to any provider/runtime that can construct
fresh requests from an explicit message allowlist and return raw response text
plus defensible telemetry. Provider-specific credentials and SDK code stay
outside this module.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
import shlex
import subprocess
from typing import Any, Protocol


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ModelRequest:
    request_id: str
    model: str
    messages: list[Message]
    settings: dict[str, Any] = field(default_factory=dict)
    response_schema: dict[str, Any] | None = None
    tools_enabled: bool = False
    retrieval_enabled: bool = False

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


@dataclass(frozen=True)
class Usage:
    input_tokens: int | str = "unavailable"
    output_tokens: int | str = "unavailable"
    reasoning_tokens: int | str = "unavailable"
    cached_tokens: int | str = "unavailable"
    cost: float | str = "unavailable"


@dataclass(frozen=True)
class ModelResponse:
    raw_text: str
    model: str
    provider_request_id: str | None = None
    usage: Usage = field(default_factory=Usage)
    metadata: dict[str, Any] = field(default_factory=dict)


class RuntimeAdapter(Protocol):
    def call(self, request: ModelRequest) -> ModelResponse:
        """Execute exactly one model request with no implicit prior state."""


class SubprocessJSONAdapter:
    """Bridge to a provider-specific executable over JSON stdin/stdout.

    The child process receives one ModelRequest JSON object on stdin and must
    return one JSON object with at least:

        {"raw_text": "...", "model": "..."}

    Optional fields:

        provider_request_id
        usage
        metadata

    This keeps provider SDKs and secrets out of the core eval harness.
    """

    def __init__(self, command: str) -> None:
        if not command.strip():
            raise ValueError("adapter command must be non-empty")
        self.command = command

    def call(self, request: ModelRequest) -> ModelResponse:
        proc = subprocess.run(
            shlex.split(self.command),
            input=request.to_json(),
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"adapter exited {proc.returncode}: {proc.stderr.strip()}"
            )
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"adapter returned invalid JSON: line {exc.lineno} "
                f"column {exc.colno}: {exc.msg}"
            ) from exc

        raw_text = payload.get("raw_text")
        model = payload.get("model")
        if not isinstance(raw_text, str):
            raise RuntimeError("adapter response missing string raw_text")
        if not isinstance(model, str) or not model.strip():
            raise RuntimeError("adapter response missing non-empty model")

        usage_data = payload.get("usage") or {}
        usage = Usage(
            input_tokens=usage_data.get("input_tokens", "unavailable"),
            output_tokens=usage_data.get("output_tokens", "unavailable"),
            reasoning_tokens=usage_data.get("reasoning_tokens", "unavailable"),
            cached_tokens=usage_data.get("cached_tokens", "unavailable"),
            cost=usage_data.get("cost", "unavailable"),
        )
        metadata = payload.get("metadata") or {}
        if not isinstance(metadata, dict):
            raise RuntimeError("adapter response metadata must be an object")

        return ModelResponse(
            raw_text=raw_text,
            model=model,
            provider_request_id=payload.get("provider_request_id"),
            usage=usage,
            metadata=metadata,
        )
