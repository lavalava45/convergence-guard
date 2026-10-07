# Execution incident 003 — main-v0.1.2 aborted before scoring

The first and only attempted `main-v0.1.2` run was `M01-r1-cg-reduced`. No judging or scoring was performed and no other `main-v0.1.2` run was started.

The new direct-backend adapter correctly received a primary model response, but an over-broad local JSON-Schema validation step rejected that raw primary before the benchmark's predeclared normalization stage could run. Specifically, the response used `status=INSUFFICIENT` while retaining a non-null `preferred_cause`, a representation that the existing normalization policy is designed to repair before final validation. The runner therefore consumed its permitted retry and ended the run `invalid` before persisting a primary response artifact.

This was a harness-ordering error introduced in `main-v0.1.2`, not a model, case, or scoring change. The replacement execution version is `main-v0.1.3`. It keeps the same 32-run plan, cases, private keys, metrics, model, runtime profile, budgets, normalization policy, and Convergence Guard treatment. The only change is that local validation inside the adapter is restricted to calibration responses, because only calibration uses the documented weakened server-side grammar compatibility transform. Primary responses again flow through the frozen normalization step before final validation, as designed.
