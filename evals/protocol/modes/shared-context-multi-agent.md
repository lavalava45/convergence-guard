# Mode: shared-context-multi-agent

## Purpose

Provide a multi-pass comparator with additional analytical compute but without Convergence Guard's protected information boundaries.

## Structure

Use three analyst passes followed by one synthesizer.

1. Analyst A sees the public case.
2. Analyst B sees the public case plus Analyst A's shared-journal output.
3. Analyst C sees the public case plus the shared journal containing A and B.
4. The synthesizer sees the public case and all three analyst outputs.

The defining property is that intermediate conclusions are available through a shared journal and are not protected by CG-style blindness.

## Constraints

- no private key or judge material;
- no conclusions from another repeat or mode;
- same public evidence and allowed tools as other modes;
- all calls count against the shared mode budget.

## Output

Only the synthesizer's normalized final answer is judged.
