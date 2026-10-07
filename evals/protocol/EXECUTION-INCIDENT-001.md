# Execution incident 001 — main-v0.1 aborted before scoring

The first attempted `main-v0.1` run was `M01-r1-cg-reduced`.

Its primary response was returned, persisted, normalized, and structurally validated. The subsequent calibration request failed with a local LM Studio TCP reset (`WinError 10054`) before a response envelope was returned. The run manifest therefore ended as `invalid`.

No semantic judging or scoring was performed and no other `main-v0.1` run was started.

Under the protocol freeze rule, the active study was not silently patched. `main-v0.1` is treated as an aborted execution version and its artifacts are excluded from the main-study result set.

The replacement execution version is `main-v0.1.1`. It keeps the same public cases, private keys, metrics, normalization policy, model, primary resource ceilings, randomization seed/run order, and Convergence Guard code under test. The only execution change is a predeclared transport-failure rule: adapter-internal retries remain disabled, but the runner may make one same-request retry after a recorded transient transport/server failure. Every such attempt consumes a model-call slot. Calibration therefore permits up to two call attempts while retaining the same 1,024 returned-output-token ceiling.

This incident document exists to make the post-freeze operational change auditable rather than invisible.
