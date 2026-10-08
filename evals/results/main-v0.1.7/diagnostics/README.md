# main-v0.1.7 post-benchmark normalization diagnostics

This directory is a diagnostic addendum for the already-frozen `main-v0.1.7` benchmark. It does not revise participant artifacts, judge outputs, aggregate scores, or the freeze manifest.

The diagnostic was added because normalization rule N1 changes `causal_assessment.preferred_cause` to `null` whenever the raw answer declares `COEXIST` or `INSUFFICIENT`. The frozen normalization policy described that operation as preserving substantive content. This audit checks the actual raw/normalized pairs directly and identifies runs where N1 removed non-null causal content so those pairs can be reviewed separately from the frozen benchmark score.

## Reproduce

From the repository root:

```powershell
python evals\harness\build_normalization_diagnostics.py
```

The builder reads only:

- `evals/runs/main-v0.1.7/{M04..M07}/.../final.raw.json`
- the corresponding `final.json` and `normalization.json`
- `evals/results/main-v0.1.7/summary.json` for the frozen neutral-ID mapping
- the public case prompt, metadata and evidence under `evals/cases/main/`

It writes only this `diagnostics/` tree.

## Outputs

- `audit.json` contains the complete machine-readable raw/normalized JSON diff, artifact SHA-256 hashes, N1 checks, and raw/normalized causal extracts.
- `audit.md` is a compact human-readable index.
- `rejudge-packets/Rxxxx.json` contains one neutral packet per M04–M07 run. Each packet preserves the frozen raw and normalized answers side-by-side and includes the public case material needed to assess the semantic effect of normalization.

The re-judge packets intentionally omit treatment mode, run ID, resource-use data, original judge scores, and aggregate results. The repository does not contain the hidden case keys, so these packets are for normalization-delta re-judging rather than a reproduction of the original full hidden-key scoring pass.

## Flag semantics

`n1_semantic_change_flag=true` has a narrow deterministic meaning: N1 removed a non-null, non-empty `preferred_cause` from the frozen raw artifact. It marks the pair for semantic re-judging. It does not assert that the raw answer was correct, that the normalized answer was incorrect, or that any frozen metric must change.

For M04–M07, the generated audit finds 16 runs, 15 N1 applications, 15 such flags, and zero mismatches between the observed JSON diff and the recorded N1 normalization path. M05 single-context (`R0025`) is the only run in this scope with no N1 change.
