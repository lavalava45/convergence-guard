# Isolation execution incident 003 — v0.1.2 aborted before scoring

`isolation-ablation-v0.1.2` was frozen before execution and aborted on its first participant cell, `M03-shared-false-anchor`, during `search_c`.

No v0.1.2 participant cell completed. No blind judging, anchor-adoption judging, or aggregate scoring was performed.

The first two logical search calls completed. During `search_c`, the SSE connection ended without a terminal `finish_reason`. The adapter correctly rejected the response as incomplete, but this incomplete-stream condition was raised as a generic runtime error rather than entering the already-defined transport retry loop.

Replacement version `isolation-ablation-v0.1.3` preserves the exact cases, 2×2 treatment design, false anchors, run order, paired seeds, model/runtime, temperature, output-token ceilings, tools/retrieval policy, output schema, metrics, judge rubric, and interpretation rules. It changes execution transport plumbing only:

- a stream that ends without a non-empty answer plus terminal `finish_reason` is retryable;
- `ChunkedEncodingError`, connection reset, timeout, transient HTTP server errors, and incomplete stream all share the same same-request retry path;
- the frozen transport-attempt cap is raised from 2 to 3 per logical call to reduce invalidation from transient local-server delivery failures.

Logical participant call count remains exactly four per cell. Every retry reuses the same request payload and paired seed. All 16 participant cells are rerun from scratch under v0.1.3.
