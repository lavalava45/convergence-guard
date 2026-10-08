# Isolation execution incident 001 — v0.1 aborted before scoring

`isolation-ablation-v0.1` was frozen before execution and then aborted on the third participant run, `M02-isolated-false-anchor`.

The first two runs completed, but they are **excluded from all isolation-ablation results**. No blind judging or scoring was performed for v0.1.

The third run failed during `search_c` because the model generated exactly the frozen `maxOutputTokens=1400` tokens and the transport reported `finish_reason=length`. The structured JSON therefore ended inside a string and could not be parsed. This was not a transport reset, causal-analysis outcome, or treatment effect.

The execution design contained two related defects:

1. the participant instruction required 2–4 search models, but the structured `SEARCH_SCHEMA` did not encode `maxItems=4`, so the grammar allowed the model to continue generating additional models;
2. the search token ceiling lived only as a runner constant rather than as an explicit frozen run-plan field.

Replacement version `isolation-ablation-v0.1.1` preserves the exact cases, 2×2 treatment design, false anchors, run order, paired seeds, model/runtime, temperature, tools/retrieval policy, judge rubric, and interpretation rules. It changes execution plumbing only:

- `SEARCH_SCHEMA.models.maxItems = 4`, matching the already-frozen textual 2–4-model instruction;
- search and synthesis output-token ceilings are explicit in the run plan (`2200` each);
- the freeze manifest additionally hashes the imported `cg_v02_workflow.py` dependency.

All 16 participant cells are rerun from scratch under v0.1.1. No v0.1 participant output is mixed into the replacement study.
