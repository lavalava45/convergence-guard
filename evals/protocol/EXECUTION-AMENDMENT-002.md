# Execution amendment 002 — main-v0.1.2 before first scored run

Status: **PREDECLARED BEFORE ANY `main-v0.1.2` PARTICIPANT RUN.**

`main-v0.1.1` was frozen but no official participant run was executed under that version. Before execution, two operational changes were made and versioned as `main-v0.1.2` rather than silently altering the frozen version.

## A. One repeat instead of two

The main study now uses **8 cases × 4 modes × 1 repeat = 32 runs**. The retained runs are exactly the already-randomized repeat-1 blocks and their original ordinals 1–32. No case, mode, public evidence, private answer key, metric, normalization rule, model setting, or within-block order was changed. The second-repeat blocks were removed before any `main-v0.1.2` outcome was observed.

The purpose is a complete applicability-map comparison across all `case × mode` cells, not an estimate of generation variance. Any later replication is reported as a separate phase rather than being mixed into this main 32-run set.

## B. Direct loaded-backend transport and calibration grammar compatibility

Control testing showed that the LM Studio proxy on port 1234 could reset connections while the already-loaded internal `llama-server` remained healthy. Main execution therefore targets the single already-loaded LM Studio `llama-server` directly through its OpenAI-compatible endpoint. The batch runner records and pins the backend PID for the batch and aborts if that PID changes.

With llama.cpp backend `2.52.0`, the frozen calibration JSON schema reproducibly reset the connection when the numeric `minimum`/`maximum` keywords on probability `p` were passed into server-side grammar generation. The identical calibration prompt succeeded when those two grammar constraints were omitted. Therefore the adapter removes **only** `minimum` and `maximum` from the schema copy sent to the server grammar layer. The returned JSON is then validated locally against the **untouched frozen calibration schema**, including the original `0 <= p <= 1` constraint. The participant-visible prompt and the accepted output contract are unchanged.

These changes affect execution transport/compatibility only. They do not change the causal tasks, answer keys, scoring, model, temperatures, primary budgets, calibration budget, or Convergence Guard treatment logic.
