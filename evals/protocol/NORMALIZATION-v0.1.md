# Deterministic Output Normalization v0.1

Status: **FROZEN FOR MAIN STUDY**

## Purpose

Before structural validation, every parseable participant primary answer passes through the same treatment-independent deterministic normalization step.

Normalization is applied only after the participant primary is frozen. It may repair only explicitly enumerated mechanical inconsistencies and must never infer, improve, or rewrite substantive causal reasoning.

## Artifacts

For every run:

- `final.raw.json` preserves the exact parsed participant primary before normalization.
- `normalization.json` records the normalization version and every deterministic repair.
- `final.json` is the normalized artifact used for structural validation, calibration context, blind judging, and scoring.

The raw primary is never overwritten.

## Rule N1 — preferred cause under non-choice status

If `causal_assessment.status` is exactly `COEXIST` or `INSUFFICIENT`, and `causal_assessment.preferred_cause` is not `null`, set `preferred_cause` to `null`.

This preserves the participant's declared status and all substantive content while enforcing the frozen output contract.

## Forbidden repairs

Normalization v0.1 does not change `status`; choose a candidate for `CHOOSE`; invent, delete, merge, or rewrite candidate causes; rewrite actions, evidence, uncertainty, or next tests; repair malformed JSON; repair unknown enum values; infer a missing preferred cause; repair unknown evidence IDs; or add/remove schema fields.

If the answer remains invalid after N1, the run remains structurally invalid.

## Diagnostics

An N1 repair does not invalidate the run. Repair count is retained in the manifest and audit artifact and is reported separately as an output-compliance diagnostic.

## Freeze rule

This policy must be frozen before the first main-study run. Any material change after main execution begins creates a new eval version.
