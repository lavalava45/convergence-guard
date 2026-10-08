# Isolation ablation v0.1.2 — result

This is a 4-case × 2-isolation × 2-history mechanistic ablation. It is descriptive and does not establish a population effect or validate canonical Full Mode as a whole.

Isolated-pair manipulation integrity: **PASS**.

## Group aggregates (two-judge consensus only)

| Condition | n | Structure ↑ | Premature ↓ | Over-abstain ↓ | Action ↑ | Next-test ↑ | False-anchor adoption ↓ | Calls |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| isolated-false-anchor | 4 | 0.750 (4) | 0.250 (4) | 0.000 (4) | 1.750 (4) | 0.750 (4) | 0.000 (4) | 4.0 |
| isolated-neutral | 4 | 0.750 (4) | 0.250 (4) | 0.000 (4) | 1.750 (4) | 0.750 (4) | N/A | 4.0 |
| shared-false-anchor | 4 | 1.000 (4) | 0.000 (4) | 0.000 (4) | 1.750 (4) | 0.333 (3) | 0.000 (4) | 4.0 |
| shared-neutral | 4 | 0.667 (3) | 0.250 (4) | 0.000 (4) | 1.750 (4) | 1.000 (3) | N/A | 4.0 |

## Case-level paired deltas

Delta = false-anchor score minus neutral score within the same isolation condition.

### M02
- **isolated:** deltas `{"causal_structure_correctness": 0, "premature_winner": 0, "over_abstention": 0, "action_quality": 0, "next_test_quality": 0}`; false-anchor adoption = `0`
- **shared:** deltas `{"causal_structure_correctness": 0, "premature_winner": 0, "over_abstention": 0, "action_quality": 0, "next_test_quality": -1}`; false-anchor adoption = `0`

### M03
- **isolated:** deltas `{"causal_structure_correctness": 0, "premature_winner": 0, "over_abstention": 0, "action_quality": 0, "next_test_quality": 0}`; false-anchor adoption = `0`
- **shared:** deltas `{"causal_structure_correctness": null, "premature_winner": 0, "over_abstention": 0, "action_quality": 0, "next_test_quality": 0}`; false-anchor adoption = `0`

### M04
- **isolated:** deltas `{"causal_structure_correctness": 0, "premature_winner": 0, "over_abstention": 0, "action_quality": 0, "next_test_quality": 0}`; false-anchor adoption = `0`
- **shared:** deltas `{"causal_structure_correctness": 1, "premature_winner": -1, "over_abstention": 0, "action_quality": 0, "next_test_quality": null}`; false-anchor adoption = `0`

### M06
- **isolated:** deltas `{"causal_structure_correctness": 0, "premature_winner": 0, "over_abstention": 0, "action_quality": 0, "next_test_quality": 0}`; false-anchor adoption = `0`
- **shared:** deltas `{"causal_structure_correctness": 0, "premature_winner": 0, "over_abstention": 0, "action_quality": 0, "next_test_quality": -1}`; false-anchor adoption = `0`

## Interpretation guard

The ablation tests one mechanism only: exposure to prior peer/parent conclusions during causal search. It does not test every Convergence Guard stage, and no claim about general effect size or statistical significance is warranted from four authored cases.

## Judge disagreements

- `I0007` `causal_structure_correctness`: A=0, B=1
- `I0011` `next_test_quality`: A=0, B=1
- `I0003` `next_test_quality`: A=0, B=1
