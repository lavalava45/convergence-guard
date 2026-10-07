# Execution incident 007 — main-v0.1.6 managed-backend stall

`main-v0.1.6` completed two primary runs and then stopped during `M01-r1-cg-full` at search worker 2. No judging or scoring was performed; v0.1.6 artifacts are excluded from the final main-study result set.

Streaming transport prevented the earlier end-of-response loss but exposed a separate runtime problem in the LM Studio-managed internal server. The first search-2 attempt remained idle until its 600-second read timeout even though the GPU was idle; immediately after the timeout the backend finally launched the queued task. The retry then generated but ended in a connection reset. Server logs throughout earlier runs also showed repeated eviction of very large prompt-cache entries (roughly 0.7-1.3 GiB each). The llama-server build defaults to an 8192 MiB prompt cache, which is unnecessary for this cross-run-isolated benchmark and introduces substantial mutable state and memory pressure.

The replacement `main-v0.1.7` runs the same llama-server 2.52.0 binary and the same Gemma 4 12B Q6_K model as a dedicated standalone localhost process rather than an LM Studio-managed internal process. It preserves context size 15000, full GPU offload, KV offload, one parallel slot, the saved LM Studio Gemma chat template, sampling settings, prompts, cases, hidden keys, schemas, budgets, normalization, and scoring. It disables cross-request prompt caching (`--no-cache-prompt --cache-ram 0 --no-cache-idle-slots`) and context checkpoints, and uses SSE streaming through the Python `requests` client.

All 32 primary runs are rerun cleanly under v0.1.7; no v0.1.6 participant output is mixed into the final set.
