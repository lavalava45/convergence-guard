# Convergence Guard Comparative Eval — Protocol v0.1

Status: **PILOT DRAFT — NOT FROZEN FOR MAIN STUDY**

## 1. Research question

Compare four complete analysis workflows on fixed cases with participant-visible evidence and a separately stored hidden evaluation key.

The primary question is not which mode produces the longest or most sophisticated-looking analysis. It is whether a mode improves decision-relevant causal reasoning, especially:

- avoidance of unsupported premature convergence;
- correct recognition of insufficient evidence;
- avoidance of unnecessary abstention on resolvable cases;
- evidence-provenance discipline;
- action quality under stated constraints;
- quality of the next discriminating test.

The first study compares complete workflows. It does **not** isolate the causal effect of context isolation alone. A later ablation must hold the CG structure fixed and toggle information boundaries.

## 2. Study stages

### 2.1 Technical pilot

Two cases:

- one resolvable;
- one intentionally underdetermined.

Each case is run once under each of the four modes: 2 × 4 = 8 runs.

Pilot results are used to debug the procedure, not to support a headline performance claim.

### 2.2 Main study

After the pilot is complete and the protocol is frozen:

- 8 new cases;
- 4 modes;
- 2 repeats;
- 64 runs total.

The eight main cases must not be used during pilot debugging.

## 3. Information boundary

Every participant run receives only:

- the case prompt;
- participant-visible evidence files;
- the mode-specific instructions;
- the common output contract;
- the tools explicitly allowed for that case.

Participant runs must not receive:

- hidden causal structure;
- answer keys;
- judge rubric annotations tied to the case;
- hidden provenance-family labels;
- calibration truth labels;
- results from another mode or repeat;
- prior-run summaries;
- private judge mappings.

Hidden case keys must be outside the git repository and unavailable to participant tools, retrieval, project context, memory, and filesystem access.

## 4. Common controls

Within a frozen main-study version, all four modes use:

- the same model family and model version;
- the same model settings supported by the runtime;
- the same participant-visible case material;
- the same allowed external tools;
- the same output schema and length cap;
- the same maximum per-case resource budget;
- no cross-run carryover of conclusions.

If a runtime metric is unavailable, record `unavailable`. Do not substitute word counts for exact token or reasoning-token telemetry.

## 5. Modes

Normative definitions are in `protocol/modes/`.

### 5.1 single-context

One fresh context receives the case and a strong general analytical instruction. Self-checking is allowed. The prompt must not intentionally cripple the baseline and must not teach Convergence Guard terminology.

### 5.2 shared-context-multi-agent

Three analyst passes and one synthesizer operate over a shared journal. Later analysts may see earlier analysts' intermediate conclusions. This comparator receives multi-pass/multi-agent compute but no CG information-boundary guarantees.

### 5.3 cg-reduced

Convergence Guard Reduced Mode is executed sequentially in one effective context. Its lack of independent-worker isolation must be disclosed in the run manifest.

### 5.4 cg-full

Convergence Guard Full Mode is executed only when the runtime isolation preflight passes. Each isolation-dependent role receives an explicit allowlist of effective inputs. A UI-level separate worker/session is not sufficient evidence of isolation.

## 6. Randomization

The main run plan uses blocked randomization.

Each block is one `case_id × repeat` combination and contains the four modes exactly once. Mode order is randomized within each block from a frozen seed.

This prevents the experiment from running all examples of one mode in the same temporal batch.

The pilot uses the same mechanism with one repeat.

## 7. Equal-budget comparison

The primary comparison uses an equal **maximum** budget per case, summed across every worker, coordinator, retry, and synthesis call belonging to a mode.

The exact main-study cap is frozen after pilot telemetry is inspected. The cap may be expressed in the resource dimension the runtime can reliably enforce, such as total billable tokens, total model calls, or a documented composite ceiling.

Actual consumption is not forced to be equal. A cheaper mode is allowed to finish below the cap.

Record where available:

- input tokens;
- output tokens;
- reasoning tokens;
- cached tokens;
- model calls;
- retries;
- wall-clock duration;
- cost;
- budget-stop events.

## 8. Participant final answer

Each mode must produce a final object conforming to `OUTPUT-SCHEMA.json`, including the public `case_id`. The case ID binds the artifact to its case without revealing the experimental mode.

Before structural validation and judging, every parseable primary answer passes through the frozen treatment-independent deterministic normalization policy in `NORMALIZATION-v0.1.md`. The exact pre-normalization answer is retained as `final.raw.json`; the repair audit is retained as `normalization.json`; and the normalized `final.json` is the judged/scored artifact.

Normalization may repair only the explicitly enumerated mechanically deterministic inconsistencies in the frozen policy. It must not infer a causal winner, change status, rewrite substantive content, repair malformed JSON, or otherwise improve the participant's reasoning. Normalization repairs are reported separately as a compliance diagnostic.

Working logs are retained separately and are not shown to the blind judge unless a later audit explicitly calls for them.

The final answer must distinguish:

- causal conclusion/status;
- candidate causes;
- preferred cause when justified;
- recommended action;
- evidence IDs used;
- material uncertainty;
- next discriminating test.

The status field is semantic, not a keyword test:

- `CHOOSE`
- `COEXIST`
- `INSUFFICIENT`

## 9. Metrics

Primary metrics are frozen before the main study:

- premature winner;
- correct abstention;
- over-abstention;
- action quality.

Secondary metrics include:

- causal mechanism recall;
- unsupported mechanisms;
- evidence-dependence errors;
- next-test quality;
- usage/cost/latency.

Do not collapse the study into one post-hoc weighted score.

Winner/abstention metrics are judged **semantically** from the blind answer against the hidden key and rubric. The harness must not infer them from the literal `status` token alone. Structural scripts may report the declared status and schema consistency only as diagnostics.

## 10. Calibration add-on

Calibration prompts occur only after the primary answer has been persisted and made immutable for that run.

The same case-specific binary claims are then presented to every mode, which returns probabilities. Brier score may be reported as a proper scoring rule, with the explicit caveat that the small number of correlated claims does not provide a strong standalone estimate of calibration.

## 11. Blind judging

Judging receives:

- public case material;
- the corresponding private key;
- the frozen rubric;
- normalized answers under neutral IDs.

Judging does not receive:

- mode name;
- worker count;
- token/cost telemetry;
- runtime duration;
- original run identifier.

The blind-ID mapping is stored outside the public repository.

## 12. Full-mode isolation preflight

Full Mode is invalid for the study unless the runtime can establish the required effective-input boundaries with reasonable confidence.

A sentinel probe may be used as a diagnostic but a negative sentinel result means only `NO LEAK OBSERVED`; it does not prove isolation.

The preflight should document, at minimum:

- whether parent transcript is inherited;
- whether sibling outputs are inherited;
- whether account/project memory is available;
- whether prior worker history is available on reuse;
- whether retrieval can surface forbidden decision-relevant material;
- what tool/filesystem scope each role receives.
- whether coordinator handoffs contain only the stage-authorized inputs.

If a required boundary is `FAIL` or materially `INCONCLUSIVE`, the run is not labeled CG Full.

## 13. Freeze rule

Before the main 64 runs, freeze and record:

- protocol version;
- metric rubric;
- output schema;
- deterministic normalization policy/version;
- all eight public cases;
- all eight private keys;
- exact mode prompts/specifications;
- model/version/settings;
- allowed tools;
- maximum budget;
- randomization seed and run plan;
- code commit/hash of the eval harness and CG version under test.

After the first main run, a material change creates a new eval version. Do not silently patch the active study.

## 14. Interpretation rule

The planned usefulness criterion is:

> CG is useful if it reduces unsupported winner selection without causing an excessive increase in abstention on resolvable cases, and the quality improvement is commensurate with added resource cost.

If Reduced Mode reaches the same decision quality as Full Mode at lower cost, that is a substantive result rather than an eval failure.
