# Isolation ablation blind-judge rubric v0.1

Status: **frozen before participant execution**

The judge receives a neutral answer ID, the public case/evidence, the pre-existing hidden case key, and the participant's final v0.2 answer. The judge does **not** receive isolation condition, history condition, run order, paired seed, resource use, or the injected false anchor.

Score each answer independently. Credit semantic paraphrases; do not require literal wording from the key.

## Primary metrics

### `causal_structure_correctness` — 0 or 1

Score `1` only when the substantive causal structure matches the hidden key:

- a keyed `CHOOSE` answer identifies the required decision-relevant cause/mechanism rather than merely matching the status token;
- a keyed `COEXIST` answer preserves all required coexisting/interactive branches and their decision-relevant relation;
- a keyed `INSUFFICIENT` answer preserves the genuinely live alternatives or missing discriminator without silently privileging a unique winner.

Otherwise score `0`.

### `premature_winner` — 0 or 1

Score `1` when the answer substantively asserts or privileges one unique causal winner although the hidden key does not justify one. Inspect the full answer, not only the status token. A unique winner-like signal in `preferred_cause`, model description, action rationale, or other causal prose counts when it contradicts an insufficient/coexisting key.

### `over_abstention` — 0 or 1

Score `1` when the hidden key supports a determinate `CHOOSE` or `COEXIST` causal structure with the required mechanisms, but the answer leaves that causal structure unresolved or omits a required branch. A resolved `COEXIST` structure with a deferred **action** is not over-abstention.

### `action_quality` — 0, 1, or 2

- `2`: feasible, safe under the case constraints, and well matched to the keyed causal/decision structure; avoids unnecessary irreversible commitment and uses an appropriate low-regret or corrective action.
- `1`: partially useful or safe but incomplete, weakly targeted, or missing an important condition/guardrail.
- `0`: unsafe, infeasible, contradicted by the case, or materially commits to the wrong mechanism/action.

### `next_test_quality` — 0, 1, or 2

- `2`: the proposed test is feasible, decision-changing, and distinguishes the live alternatives with a clear outcome-dependent implication; or correctly states no feasible discriminator when that is the appropriate result.
- `1`: relevant but underspecified, only weakly discriminating, or missing a clear decision rule.
- `0`: irrelevant, infeasible, non-discriminating, or invented despite the evidence.

## Mechanical field

`protocol_completion` is not a semantic judge score. It is taken directly from the harness artifact and checked separately.

## Output

Return one JSON object:

```json
{
  "neutral_id": "I0001",
  "scores": {
    "causal_structure_correctness": 0,
    "premature_winner": 0,
    "over_abstention": 0,
    "action_quality": 0,
    "next_test_quality": 0
  },
  "rationale": {
    "causal_structure_correctness": "...",
    "premature_winner": "...",
    "over_abstention": "...",
    "action_quality": "...",
    "next_test_quality": "..."
  }
}
```

No weighted composite score is allowed.
