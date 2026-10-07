# Comparative eval runbook

## Current gate

The public pilot scaffold is ready to exercise, but the currently tested Chat On Steroids spawned-worker runtime failed the Full Mode isolation preflight.

Do not execute participant runs with a runtime that exposes hidden keys, prior run outputs, parent reasoning, account/project memory, or forbidden sibling conclusions.

## Clean participant-runtime requirements

A usable participant runtime must provide:

1. fresh model contexts whose effective input can be constructed explicitly;
2. no account/project memory or prior-chat injection;
3. no access to private judge/key material;
4. no access to earlier mode/repeat outputs;
5. tool/retrieval allowlists matching the public case contract;
6. identical model/version/settings across all four modes;
7. usage telemetry where available;
8. a way to create multiple genuinely separate contexts for CG Full.

A fresh API request with no tools/retrieval and an explicit message allowlist is a natural implementation, but the harness does not require a specific provider.

## Before pilot

1. Run `validate_cases.py`.
2. Run the runtime isolation preflight.
3. If any required Full boundary is FAIL or materially INCONCLUSIVE, set `cg_full_enabled=false` and do not claim a Full result.
4. Confirm participant roles cannot access hidden keys.
5. Freeze the pilot run plan.
6. Record model/version/settings and the pilot resource cap.

## Pilot order

Use `run-plans/pilot-v0.1.json`.

The plan is blocked-randomized: each case/repeat block contains the four modes once in randomized order.

Do not reorder runs after seeing answers.

## Per-run artifact layout

Runtime artifacts should be written under the ignored `evals/runs/` tree only after doing so cannot expose previous answers to later participant runs.

Suggested layout:

```text
evals/runs/pilot/P01/r1/cg-full/
  manifest.json
  working/
  final.json
  calibration.json
  usage.json
  integrity.json
```

If later participant runs can read this directory, keep outputs outside their tool scope until all participant runs are finished.

## Run sequence

For each planned run:

1. create a manifest skeleton with `new_manifest.py`;
2. instantiate a fresh context according to the mode spec;
3. provide only participant-visible case material;
4. execute within the shared maximum resource budget;
5. persist the primary final answer;
6. validate it with `validate_final.py <final.json> --case <public-case-directory>`; this checks the full normalized structure, case binding, and referenced evidence IDs;
7. only then request the calibration probabilities;
8. record exact telemetry or `unavailable`;
9. never modify the primary answer after calibration.

## Mode execution

### single-context

One fresh context. Use the strong baseline instruction in `protocol/modes/single-context.md`.

### shared-context-multi-agent

Three analyst passes and one synthesizer. Intermediate conclusions deliberately enter a shared journal.

### cg-reduced

Run the repository's Reduced Mode sequentially in one effective context. Record that independent blindness is unavailable.

### cg-full

Run only after preflight PASS. Each isolation-dependent role gets only the current CG protocol's explicit stage allowlist.

## After all participant runs

1. create neutral blind IDs;
2. keep the run-ID mapping private;
3. build judge packets with public case + hidden key + neutralized final answer;
4. record deterministic structural diagnostics separately from semantic judging; winner/abstention outcomes are semantic metrics and are not inferred from the `status` token alone;
5. adjudicate judge disagreements without revealing the mode;
6. unblind only after scoring is frozen.

## After pilot

The pilot exists to find procedural defects.

It is allowed to revise:

- prompts;
- schemas;
- metric anchors;
- telemetry collection;
- mode adapters;
- isolation implementation.

After revisions, create the eight **new** main cases and freeze v1 before the first main run.
