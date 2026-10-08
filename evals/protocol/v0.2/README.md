# Eval protocol v0.2 — post-benchmark correction layer

This directory defines the next evaluation layer after the frozen `main-v0.1.7` workflow benchmark. It does **not** rewrite or rescore the frozen v0.1.7 result set.

The v0.2 changes address three observed gaps:

1. **specification/execution conformance** — a mode may not be labeled complete when a triggered canonical stage was skipped;
2. **outcome separation** — causal structure, action sufficiency, next-test availability, and protocol completion are separate machine-verifiable fields;
3. **normalization transparency** — raw winner-like signals remain auditable even when a predeclared normalizer repairs a structurally inconsistent field.

`OUTPUT-SCHEMA-v0.2.json` intentionally supports:

- zero supported causal models;
- a resolved `COEXISTING` causal structure with an unresolved action decision;
- a robust chosen action while causal structure remains unresolved;
- `NO_FEASIBLE_DISCRIMINATOR` without inventing a next test;
- an explicitly partial protocol when a triggered stage could not be executed;
- pending revised hypotheses that must not be silently promoted.

`METRICS-v0.2.yaml` adds direct causal-structure correctness and raw-output diagnostics. No weighted composite score is allowed.

The first v0.2 experiment is the targeted isolation ablation in `ISOLATION-ABLATION-v0.1.md`. Its purpose is narrow: test whether hiding prior peer conclusions during causal search changes susceptibility to a false confident anchor **while holding the rest of the workflow, model, evidence, call count, and seeds fixed**.
