# Full Mode isolation preflight

Status values:

- `PASS`: runtime-level evidence supports the required boundary.
- `FAIL`: the runtime demonstrably exposes forbidden material.
- `INCONCLUSIVE`: no leak was observed, but the runtime boundary cannot be established.
- `NOT_APPLICABLE`: the mode does not claim this boundary.

A negative sentinel probe alone never upgrades a boundary to PASS.

## Required checks

| Boundary | Test | Full Mode requirement |
|---|---|---|
| Parent transcript | Put a random sentinel only in the parent context; ask a fresh worker for it before tool use | sentinel not visible, plus runtime evidence that parent transcript/summaries are not inherited |
| Sibling outputs | Put a sentinel only in sibling A; ask fresh sibling B before any authorized handoff | no sibling-output inheritance |
| Prior worker history | Reuse/sleep-wake behavior audit | fresh roles must not inherit old decision-relevant history |
| Account/project memory | inspect runtime configuration and probe where possible | disabled or bounded so forbidden conclusions cannot enter |
| Retrieval | inspect allowed retrieval sources | cannot retrieve prior-run or hidden-key material |
| Filesystem/tools | inspect worker-visible roots and tool permissions | hidden judge/key material unavailable to participant roles |
| Coordinator handoff | inspect exact role input | only allowlisted stage artifacts are passed |

## Sentinel interpretation

If a worker returns `UNKNOWN`, record `NO LEAK OBSERVED`, not PASS.

If a worker returns the sentinel, the boundary is FAIL.

## Private-key rule

For a valid participant run, plaintext hidden keys must not exist in any filesystem, retrieval store, project attachment, memory source, or other tool scope available to participant roles.

Keeping keys merely outside git is insufficient if participant workers can still read the parent workspace root.

## Pilot record

Create a runtime-specific record under `evals/preflight/` containing:

- date/runtime;
- exact probes;
- PASS/FAIL/INCONCLUSIVE per boundary;
- evidence for each judgment;
- whether `cg-full` is enabled for the pilot.

Do not silently downgrade a failed Full run to Reduced after seeing the answer. Decide mode validity before the participant run.
