# Convergence Guard comparative eval — technical pilot report v0.1

Date: 2026-10-07

Status: **technical pilot complete; not a performance result**

> **Subsequent status:** the pilot was followed by the completed frozen `main-v0.1.7` benchmark (32 participant runs, 32 calibration completions, blind semantic judging). References below to the then-planned 64-run main study are preserved as historical pilot-era planning, not the final executed design. See `results/main-v0.1.7/`.

## Executive summary

The manual browser pilot completed all eight planned run slots. Five runs produced valid primary answers and completed calibration. Three slots were invalid for procedural reasons:

- both `cg-full` slots were invalidated before participant execution because the Gemini consumer-browser runtime could not establish the Full Mode isolation boundaries at runtime level;
- `P02-r1-shared-context-multi-agent` produced a semantically recoverable answer, but the primary artifact as captured contained a literal trailing backslash on each line and therefore was not valid JSON. Per the frozen procedure, the primary artifact remained immutable and no calibration was requested.

The valid answers did not reveal a substantive decision-quality separation among `single-context`, `shared-context-multi-agent`, and `cg-reduced` on these two pilot cases. All valid P01 answers selected the keyed configuration error; all valid P02 answers correctly declined to choose between the two live mechanisms. This is useful as a procedure check, but it is not evidence that the modes are equivalent.

The pilot therefore succeeded primarily by identifying two main-study blockers: **runtime isolation for Full Mode** and **manual browser transport/format reliability**.

## Run disposition

| Run | Status | Primary result | Calibration |
|---|---|---|---|
| P01-r1-cg-reduced | complete | valid JSON; `CHOOSE` | complete |
| P01-r1-shared-context-multi-agent | complete | valid JSON; `CHOOSE` | complete |
| P01-r1-single-context | complete | valid JSON; `CHOOSE` | complete |
| P01-r1-cg-full | invalid | not executed | not run |
| P02-r1-shared-context-multi-agent | invalid | formatting-invalid primary; diagnostic recovery parses as `INSUFFICIENT` | not run |
| P02-r1-single-context | complete | valid JSON; `INSUFFICIENT` | complete |
| P02-r1-cg-full | invalid | not executed | not run |
| P02-r1-cg-reduced | complete | valid JSON; `INSUFFICIENT` | complete |

## Hidden-key audit after participant phase

This section is a **non-blind pilot audit**, not the frozen blind semantic score.

### P01 — resolvable

Private key:

- required mechanism: deployment changed `DATABASE_HOST` to a nonexistent DNS name;
- acceptable status: `CHOOSE`;
- acceptable action: restore `db-proxy.internal` or roll back the configuration/deployment.

All three valid participant modes matched that decision structure and recommended the keyed corrective action.

Calibration truth was `K1=1`, `K2=0`. All three completed P01 calibrations returned `1.0, 0.0`, giving Brier score 0 on the two pilot claims.

### P02 — intentionally underdetermined

Private key:

- two live mechanisms remain: TLS-client behavior and new outbound-policy-path disruption;
- acceptable status: `INSUFFICIENT`;
- no preferred cause;
- acceptable action: non-disruptive isolation/diagnostics before production rollback.

Both valid participant modes (`single-context`, `cg-reduced`) matched the keyed decision structure and recommended an isolated diagnostic/canary strategy.

The formatting-invalid shared-context primary is not scored as a valid run. A separately stored diagnostic copy, produced only by removing the literal trailing backslash at each line ending, passes the structural validator and declares `INSUFFICIENT`; it must not be substituted for the frozen primary artifact.

Calibration truth was `K1=0`, `K2=0`. Both completed P02 calibrations returned `0.0, 0.0`, giving Brier score 0 on the two pilot claims.

## Local LM Studio follow-up pilot

After the manual browser pilot, the same P01/P02 cases were run locally through LM Studio using one fixed participant model, `gemma-4-12b-it`, across all four modes. The local OpenAI-compatible adapter uses fresh explicit HTTP requests with tools/retrieval/session carryover disabled. The local isolation preflight passed for the Full Mode boundaries and is recorded in `evals/preflight/lmstudio-local-2026-10-07.json`.

Before accepting this follow-up, the pilot exposed a repeated mechanically inconsistent output pattern: the model sometimes declared `COEXIST` or `INSUFFICIENT` while also populating `preferred_cause`. Because the eval was still pre-main-study, the protocol was amended with the treatment-independent `NORMALIZATION-v0.1.md`. The raw primary is preserved as `final.raw.json`; rule N1 only sets `preferred_cause=null` when status is `COEXIST` or `INSUFFICIENT`; every repair is recorded in `normalization.json`. No status, causal claim, evidence, action, uncertainty, or next test is changed.

All eight local runs completed strict final validation and calibration after this normalization layer.

| Case | Mode | Normalized status | N1 repairs | Calls incl. calibration | Input tokens | Output tokens |
|---|---|---|---:|---:|---:|---:|
| P01 | single-context | `CHOOSE` | 0 | 2 | 1,857 | 595 |
| P01 | shared-context-multi-agent | `COEXIST` | 1 | 5 | 6,828 | 1,796 |
| P01 | cg-reduced | `INSUFFICIENT` | 1 | 2 | 2,580 | 561 |
| P01 | cg-full | `INSUFFICIENT` | 1 | 8 | 10,417 | 4,864 |
| P02 | single-context | `INSUFFICIENT` | 0 | 2 | 1,966 | 675 |
| P02 | shared-context-multi-agent | `INSUFFICIENT` | 1 | 5 | 8,389 | 2,682 |
| P02 | cg-reduced | `INSUFFICIENT` | 0 | 2 | 2,751 | 705 |
| P02 | cg-full | `INSUFFICIENT` | 1 | 9 | 11,735 | 5,608 |

The local hidden-key audit is descriptive only because P01/P02 are pilot-debugging cases. On P01, only `single-context` declared the keyed `CHOOSE` status. Shared declared `COEXIST`; Reduced and Full declared `INSUFFICIENT`, so those three overcomplicated or over-abstained on a resolvable case even though all four modes recommended the keyed corrective action of restoring `db-proxy.internal`. On P02, all four modes correctly declared `INSUFFICIENT` and recommended non-disruptive diagnostics/canary-style learning rather than committing to one of the two live mechanisms.

The P02 Full Mode path also exercised the zero-finalist insufficiency branch: C1/C2 left no finalist that survived strongly enough to enter the dossier slate, D2 triggered the independent second opinion, D3 completed, and reconciliation retained `INSUFFICIENT`.

Normalization fired in 4 of 8 local runs. This repair rate must remain a separately reported output-compliance diagnostic in any main study rather than being hidden by normalization.

This local follow-up still does **not** support a performance claim. It uses only two pilot cases and one repeat, and both cases were already used while engineering the harness. Its purpose is to demonstrate an end-to-end automated four-mode runtime, validate the normalization policy, exercise Full Mode isolation, and estimate resource cost before freezing the main study.

## What the pilot does *not* show

- The original manual browser phase does not compare `cg-full` against the other modes because the consumer-browser runtime failed the isolation gate. The later LM Studio follow-up does execute all four modes, including valid Full Mode runs.
- It does not support a headline performance claim: there are only two deliberately simple pilot cases and one repeat.
- It does not establish a general ordering among `single-context`, `shared-context-multi-agent`, `cg-reduced`, and `cg-full`; the two pilot cases are insufficient for that purpose.
- The calibration values are perfect on four highly correlated binary claims across two cases; this is far too small to support a calibration claim.

## Procedural defects found

### 1. Full Mode runtime isolation blocker in the manual browser runtime

Consumer Gemini Temporary Chats provide UI separation, but the pilot could not establish runtime-level absence of parent-history, sibling, account/project-memory, or retrieval leakage. Under the frozen protocol, this is `INCONCLUSIVE`, not `PASS`.

The later LM Studio stateless runtime passed the corresponding local isolation preflight, showing that this blocker is runtime-specific rather than inherent to the protocol.

**Required main-study rule:** the exact runtime selected for the main study must itself pass the frozen preflight. A PASS from one runtime or project must not be transferred to another.

### 2. Manual browser transport is not reliable enough

The P02 shared-context synthesizer artifact was captured with a literal trailing `\` on every line. Removing only those characters yields schema-valid JSON, but the frozen primary cannot be repaired.

**Required main-study fix:** remove manual copy/paste from participant transport. Capture the provider's raw response directly and separately persist:

- provider response bytes/text;
- parsed structured object;
- validation result;
- parse error, if any;
- retry event, if the frozen retry policy permits one.

Prefer provider-supported structured output / JSON-schema enforcement where available.

### 3. Validator parse failures should be first-class results

`validate_final.py` previously emitted an uncaught `JSONDecodeError` traceback. It now emits a concise deterministic `ERROR: invalid JSON ...` and exits 1.

### 4. Primary budget and calibration accounting need separation

The pilot manifests count calibration as another model call. For the main comparison, the **primary reasoning budget** should be frozen independently of the standardized post-freeze calibration add-on; otherwise calibration bookkeeping obscures the resource comparison.

Recommended accounting:

- `primary_model_calls`, tokens, cost, latency;
- `calibration_model_calls`, tokens, cost, latency;
- combined totals only as secondary telemetry.

### 5. Blind judging still needs a clean judging runtime

The current coordinating chat knows run modes and therefore cannot serve as the blind semantic judge. Main-study judging must use neutral answer IDs and a judge context that receives only public case material, private key/rubric, and the neutralized answer.

## Go/no-go criteria before main study

Do **not** start the 64-run main study until all of the following are true:

1. an automated participant adapter can run all four modes without manual copying;
2. the chosen runtime passes the Full Mode isolation preflight;
3. raw-response capture and strict structured parsing are deterministic;
4. retry policy for malformed output is frozen before runs begin;
5. resource-budget accounting is frozen and separates primary analysis from calibration;
6. blind judge packet generation and private ID mapping are automated;
7. eight entirely new main cases and private keys are complete;
8. protocol, prompts, schema, model/version/settings, tools, budget, seed, run plan, harness commit, and CG commit are frozen.

## Pilot conclusion

The pilot achieved its intended purpose: it found procedure failures before the main benchmark. The browser-copy workflow has now been supplemented by an auditable local API/runtime adapter, Full Mode isolation has passed for the LM Studio runtime, and deterministic normalization v0.1 has been defined and exercised. The next step is to freeze the actual main-study model/runtime, budgets, normalization version, eight new cases/private keys, blind-judge pipeline, seed/run plan, and harness/CG commits, then execute the 64 main runs automatically.
