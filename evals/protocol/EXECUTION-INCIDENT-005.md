# Execution incident 005 — main-v0.1.4 calibration transport failure

`main-v0.1.4` completed three M01 runs and completed the full primary analysis for the fourth (`M01-r1-shared-context-multi-agent`). That fourth run then exhausted its two calibration transport attempts with TCP resets, so the v0.1.4 batch stopped. No judging or scoring was performed, and later runs were not started. All v0.1.4 artifacts are excluded from the final main-study result set.

Backend logs show that both supposedly failed calibration attempts actually completed model inference successfully (106 generated tokens each) before the HTTP response was lost to the client. The identical frozen calibration request subsequently succeeded unchanged. This establishes a flaky response-transport failure after primary completion, not a participant reasoning failure, schema-contract failure, or CUDA OOM.

The replacement `main-v0.1.5` therefore separates execution into two phases without changing the benchmark treatment:

1. execute and freeze all 32 primary results first;
2. calibrate those immutable primary results in a separate pass.

Calibration already occurs after a valid immutable primary answer and is forbidden from revising it. Deferring calibration therefore changes execution scheduling only. It prevents a secondary calibration transport failure from discarding a valid primary result. Cases, modes, run order, hidden keys, model, runtime profile, primary prompts, schemas, normalization, scoring, and resource ceilings are unchanged. Calibration failures, if any, remain explicitly recorded and may reduce calibration coverage, but do not retroactively invalidate primary comparative outcomes.
