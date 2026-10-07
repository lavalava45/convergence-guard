# Execution incident 006 — main-v0.1.5 primary response-delivery failure

`main-v0.1.5` completed 13 primary runs and stopped during `M04-r1-cg-full` at the D2 adjudication request. No judging or scoring was performed. The v0.1.5 artifacts are excluded from the final main-study result set.

The D2 request made two permitted transport attempts. Backend logs show that both attempts completed inference successfully (823 and 773 generated tokens respectively) but the non-streaming HTTP connection was reset before the client received the response envelope. This is the same response-delivery failure class previously observed during calibration, now demonstrated during primary analysis.

Control testing sent the identical D2 request through the same already-loaded backend using the OpenAI-compatible streaming endpoint. The server returned HTTP 200 immediately and delivered the complete structured response incrementally (820 output tokens, valid JSON, `finish_reason=stop`).

The replacement execution version is `main-v0.1.6`. It uses SSE streaming for response transport while preserving the same model, prompts, structured-output schema, sampling temperature, per-request token caps, call budgets, cases, run order, hidden keys, normalization, and scoring. Each streamed request is still one model call. The adapter only accepts a streamed response when a complete answer and terminal `finish_reason` are observed; usage telemetry remains required for budget accounting.

Because response transport changed, all 32 main primary runs are rerun cleanly under v0.1.6 rather than mixing streaming and non-streaming participant results.
