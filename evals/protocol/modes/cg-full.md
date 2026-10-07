# Mode: cg-full

## Purpose

Evaluate the current Convergence Guard Full Mode with the information boundaries that are part of the method.

## Activation

The run is valid only if the runtime isolation preflight is `PASS` for every boundary on which the active CG protocol relies.

If a required boundary is `FAIL` or materially `INCONCLUSIVE`, do not relabel a sequential/shared run as Full Mode. Mark the run invalid for the Full-mode treatment.

## Effective-input rule

Each isolation-dependent role receives only host/system/safety instructions, the exact stage inputs allowed by the current CG protocol, and participant-visible case material needed for that role.

It must not inherit or retrieve forbidden decision-relevant material through parent history, sibling outputs, prior worker history, account/project memory, shared scratchpads, or unrestricted retrieval.

## Eval-specific constraints

- private keys and judge files are unavailable to all participant roles;
- outputs from another mode or repeat are unavailable;
- branch-private new evidence must follow CG evidence-checkpoint rules before becoming shared evidence;
- all workers, coordinator calls, retries, and adjudication calls count against the same mode budget.

## Output

Normalize the final adjudicated result to the common final-answer schema.
