# Mode: cg-reduced

## Purpose

Measure the value of Convergence Guard's reasoning structure when genuine isolation is unavailable.

## Definition

Run the repository's current Convergence Guard Reduced Mode in one effective context.

The run preserves the Reduced Mode reasoning shape as documented by the version under test, while explicitly lacking the independence/blindness guarantees of Full Mode.

## Constraints

- one effective context;
- no private key or judge material;
- no conclusions from another repeat or mode;
- same public evidence and allowed tools as other modes;
- all sequential passes, retries, and synthesis work count against the mode budget.

## Manifest requirement

`isolation_preflight` must be `NOT_APPLICABLE`.

## Output

Normalize the final result to the common final-answer schema.
