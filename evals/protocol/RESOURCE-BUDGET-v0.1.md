# Main-study resource budget v0.1 — frozen

Status: **FROZEN FOR MAIN STUDY.**

The primary comparison uses the same enforceable ceiling for every `case × mode × repeat` run.

## Primary-analysis ceiling

- maximum model calls: **12**;
- maximum generated/output tokens summed across all primary-analysis calls: **32,768**;
- retries count toward both ceilings;
- the frozen main runner disables adapter-internal transport retries (`maxTransportAttempts=1`) so no model request can occur outside the run-level call counter;
- calibration is excluded from the primary ceiling and is standardized separately;
- no mode receives additional calls or output-token budget because its workflow has more stages;
- a mode may finish below either ceiling;
- if the next request cannot be issued without exceeding the remaining output-token allowance, the run stops as `budget_stop` rather than silently increasing the budget.

The output-token ceiling is enforced by clamping each request's `maxOutputTokens` to the remaining primary allowance. Actual output tokens are accumulated from LM Studio usage telemetry after every call.

The call ceiling is a second hard guard. Provider/transport retries count because they consume model execution. A parse retry or conditional CG second opinion therefore consumes the same finite run budget.

## Calibration add-on

Calibration occurs only after a valid immutable primary answer:

- maximum model calls: **1**;
- maximum generated/output tokens: **1,024**;
- temperature: **0**.

Calibration usage is reported separately and must not be used to rescue or revise the primary answer.

## Frozen local runtime

- runtime: LM Studio OpenAI-compatible local API;
- model: `gemma-4-12b-it`;
- primary temperature: `0.2`;
- per-request output cap: the smaller of the workflow's stage cap and the remaining aggregate primary allowance;
- tools: disabled;
- retrieval: disabled;
- cross-run state: none;
- CG Full requires the recorded isolation preflight to remain PASS.

This budget is a study-design ceiling, not a claim that all modes consume equal resources. Resource efficiency is itself a reported outcome.
