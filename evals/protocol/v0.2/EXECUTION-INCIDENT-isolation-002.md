# Isolation execution incident 002 — v0.1.1 aborted before scoring

`isolation-ablation-v0.1.1` was frozen before execution and then aborted when `M03-isolated-false-anchor` failed during `search_a`.

Five participant cells had completed before the failure. They are **excluded from all final isolation-ablation results**. No blind judging, anchor-adoption judging, or aggregate scoring was performed for v0.1.1.

The failure was transport plumbing, not a participant-analysis outcome. The standalone server closed an SSE connection mid-stream. `requests` surfaced this as `ChunkedEncodingError`. The adapter's frozen retry block handled `ConnectionError`, timeout, and direct connection reset, but not `ChunkedEncodingError`; therefore the same-request retry policy was never reached for this equivalent connection-failure class.

Replacement version `isolation-ablation-v0.1.2` preserves the exact cases, 2×2 treatment design, false anchors, run order, paired seeds, model/runtime, temperature, output-token ceilings, tools/retrieval policy, output schema, metrics, judge rubric, and interpretation rules from v0.1.1. It changes execution transport handling only:

- `requests.exceptions.ChunkedEncodingError` is treated as a retryable connection failure under the already-frozen `maxTransportAttempts=2` request policy.

All 16 participant cells are rerun from scratch under v0.1.2. No v0.1.1 participant output is mixed into the replacement study.
