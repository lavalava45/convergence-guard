# Convergence Guard v0.2.1 — Detailed Protocol Rules

This file contains operational details that are intentionally kept out of the main `SKILL.md`. Read only the sections relevant to the current run.

## 1. Independence model

Convergence Guard uses several distinct kinds of independence. Do not conflate them.

- **Context isolation**: one worker does not see another worker's output.
- **Preference blindness**: a reviewer does not see earlier rankings, favorites, or authorship.
- **Evidential independence**: two real-world observations come from genuinely separate evidence sources.

Only the first two can be created by worker orchestration. They do **not** create evidential independence. Multiple workers reasoning over the same evidence may reproduce the same bias.

A fresh worker is required when a stage relies on context isolation or preference blindness. Do not deprive a worker of relevant evidence merely to make it appear independent.

## 2. Evidence provenance

Use these labels consistently:

- `CONFIRMED`: inspected directly in the current analysis or available primary evidence.
- `REPORTED`: asserted by a user, operator, witness, secondary source, or prior analysis but not independently inspected here.
- `STRONGLY INFERRED`: supported by a coherent evidence chain but not directly observed.
- `HYPOTHESIS / ASSUMPTION`: plausible but unverified.
- `CONSTRAINT`: a real decision boundary.
- `OPEN QUESTION`: an unknown capable of changing the action.

A user's direct observation can be highly valuable while still being `REPORTED` if the underlying event was not independently inspected. The label tracks provenance, not trustworthiness or importance.

## 3. Optional independent reframe review

Trigger when one or more are true:

- framing error would be expensive;
- the wording embeds a strong causal or solution assumption;
- disagreement concerns the nature of the problem rather than implementation details;
- the analysis is expensive enough that exploring the wrong frame would be materially wasteful.

Use a fresh worker. Give it only the evidence brief, original question, and decision contract. Hide the coordinator's framing conclusion and future candidate models.

Require:

1. strongest hidden assumption in the framing;
2. strongest alternate formulation worth testing;
3. one observation that would distinguish the original and alternate framing.

Do not manufacture a reframe when none is material.

## 4. Optional retrospective causal reconstruction

Use when explaining an event that has already happened and observable traces exist.

Reconstruct backward:

```text
observed outcome
→ immediately preceding state
→ earliest known deviation from expected trajectory
→ competing causal chains
→ missing evidence that would distinguish them
```

Label every link as `CONFIRMED`, `REPORTED`, `STRONGLY INFERRED`, or `HYPOTHESIS` as appropriate. Do not invent missing events merely to make a coherent story.

The reconstruction expands the candidate space; it is not proof of cause.

## 5. Outside-view / reference-class check

Use when a meaningful reference class exists and reasonably relevant base-rate evidence is available.

Record:

- the reference class;
- why it is relevant;
- the baseline frequency or qualitative prior, if supported;
- material differences between the current case and the reference class.

Do not force a reference class where none is defensible. Do not let a generic base rate override stronger case-specific evidence. Its purpose is calibration and missing-family detection.

## 6. Search-mandate quality and adaptive expansion

Start Full Mode with three search mandates.

Before launch, compare mandates pairwise. Reject a pair when both would examine essentially the same system boundary, intervention, mechanism family, and evidence despite different wording.

Useful mandate dimensions include:

- system boundary;
- intervention point;
- resource/information/coordination constraint;
- feedback or temporal dynamics;
- expected evidence;
- counterfactual boundary.

After the first three workers return, run a **coverage gate**. Add one or two workers only if a material causal region remains uncovered, outputs collapse into too few families, or outside-view/framing evidence indicates a missing family.

Expansion workers must not receive previous branch outputs. Their new mandate may target an uncovered region but should not disclose which earlier candidate the coordinator favors or rejects.

The default search budget is therefore **3 workers, adaptively expandable to 5**.

## 7. Candidate traceability

After search, assign neutral IDs. Keep a private trace map containing:

- source worker;
- original wording;
- material premises;
- later transformations.

If refinement changes the causal mechanism, creates a new load-bearing premise, or changes the implied action materially, create a **new hypothesis ID**. Do not silently treat the revised model as the original candidate.

## 8. Causal-identification check

A coherent causal chain is not sufficient evidence of causality.

For each serious candidate, explicitly consider:

- confounding;
- reverse causality;
- selection effects / survivorship;
- temporal ordering;
- measurement or proxy error;
- feedback loops that make direction ambiguous.

Use:

- `SUPPORTED`: identification threats are reasonably addressed by current evidence;
- `THREATENED`: one or more material threats remain;
- `UNIDENTIFIED`: the causal direction is mostly narrative or correlational on current evidence.

Do not convert these labels into numeric probabilities unless the domain supplies defensible quantitative estimates.

## 9. Parallel screening and blind mapping

Phase C deliberately runs the screener and mapper in parallel fresh contexts after candidate neutralization.

### Screener receives

- evidence brief;
- decision contract;
- neutral candidate models.

It evaluates contract fit, evidence support, causal completeness, causal identification, discriminability, and decision exposure if wrong.

### Mapper receives

- claim;
- mechanism;
- necessary conditions;
- predictions;
- implied action;
- disconfirming evidence.

It does **not** receive screening outcomes, danger flags, source branch identity, or coordinator preference.

Neither process should wait for or see the other's result. Freeze both outputs before reconciliation.

## 10. Model relations and duplicate-family control

The mapper may classify relations as:

- `EXCLUSIVE`;
- `COEXISTING`;
- `NESTED`;
- `INTERACTING`.

Two candidates should be merged representationally only when their mechanism and decision-relevant predictions are materially the same.

When several candidates belong to one near-duplicate family, do not let their count increase confidence. Normalize support at the **family level**, then inspect the evidence supporting that family.

## 11. Conditional boundary audit

The mapper should mark uncertain merges or relation classifications.

Run a separate boundary critic only if:

- a merge is disputed;
- two neighboring families may imply different actions;
- `EXCLUSIVE` versus `COEXISTING/INTERACTING` classification is decision-relevant;
- a family boundary could materially alter finalist selection.

Skip the boundary critic otherwise.

The critic asks whether a plausible condition or intervention would produce materially different predictions and different actions. If not, the distinction is not decision-relevant.

## 12. Finalist slate and information probe

Select **2–3 model finalists**, not exactly three.

The finalist set should contain causally distinct, viable, decision-relevant models. Prefer non-dominated candidates rather than a single aggregate score.

For every strong non-dominated candidate left outside the slate, record one explicit exclusion rationale.

Separately identify at most one **information probe**. This is a model, uncertainty, or test target with high decision value. It is not automatically a finalist.

If fewer than two viable causal families remain, do not create a tournament. Either:

- move directly to decision analysis if only one model/action remains viable after factual checks; or
- collect evidence if the apparent collapse may be caused by missing data.

## 13. Evidence checkpoints

Do not let Phases A–D merely reprocess one frozen factual brief indefinitely.

Pause for targeted evidence collection when any of these occurs:

- the causal map exposes a missing evidence class that could change the slate;
- the shared-bias audit exposes a missing causal family;
- assumption sensitivity turns the leading action on an unresolved fact;
- pairwise collision is repeatedly `UNDETERMINED` because one obtainable fact is missing;
- a dossier exposes a direct contradiction with available primary evidence.

After new evidence arrives, rerun only the affected operations.

## 14. Causal dossier integrity

A dossier worker sees one finalist only. It is responsible for making that model explicit, not for defeating rivals it cannot see.

A dossier must include:

- mechanism;
- load-bearing assumptions;
- observable predictions;
- disconfirming or decision-invalidating observations;
- decision consequence;
- causal-identification weaknesses;
- error cost and reversibility.

When a dossier adds a material new premise or repairs a missing causal link by changing the original model, create a new candidate ID and route it back through screening/mapping/slate as needed.

## 15. Optional premortem

Use after the causal dossier when the contemplated action is expensive, hard to reverse, risky, or strategically important.

Ask for the most plausible **sequence** by which the action fails, the earliest signal, the likely misunderstanding, and reversibility.

Do not use premortem automatically for trivial or easily reversible choices.

## 16. Optional stakeholder lens

Use only when distinct stakeholders materially affect outcomes or constraints.

For statements about stakeholders, preserve evidence provenance: observed, reported, inferred, or hypothetical. Do not invent preferences to fill missing evidence.

## 17. Assumption sensitivity

Do not test an arbitrary single assumption and call the model robust.

Rank candidate assumptions qualitatively by the combination of:

- uncertainty;
- causal leverage;
- decision sensitivity.

Test the most load-bearing assumption first. If another assumption is similarly critical, test it separately. Change one assumption at a time unless interaction itself is the hypothesis being tested.

For each mutation, recompute:

```text
mutated assumption
→ mechanism
→ intermediate consequence
→ prediction
→ action implication
```

`ROBUST`, `CONDITIONAL`, and `BROKEN` describe the action/model response under the tested mutation only.

## 18. Shared-bias audit

The slate-level adjudicator checks for:

1. common hidden assumption;
2. missing evidence class;
3. missing causal family;
4. objective/proxy substitution;
5. population/system-boundary bias;
6. common data ancestry;
7. outside-view/base-rate conflict;
8. common causal-identification weakness.

If a missing family or decisive missing evidence is found, do **not** only replace finalists from the same existing pool. Route to targeted search or evidence collection.

## 19. Pairwise collision

Run pairwise collision only among existing finalists and only where their implications for action conflict.

- Two finalists: compare one pair.
- Three finalists: compare three pairs.

Do not force `EXCLUSIVE` framing on coexisting or interacting causes. A pair may both be true while still implying different priorities or intervention order.

Use a fixed comparison rule:

1. What materially different prediction or condition separates the models?
2. What action differs because of that separation?
3. What obtainable fact could change the action preference?
4. Which action is currently preferable under the decision contract?
5. If no defensible preference exists, return `UNDETERMINED`.

A cycle may reflect criterion drift, interaction, or missing evidence. Do not average it into a score.

## 20. Conditional independent second opinion

Trigger when:

- pairwise results form a cycle;
- several comparisons are `UNDETERMINED`;
- evidence for the apparent winner remains weak or causally unidentified;
- the action is unusually hard to reverse;
- a serious shared blind spot was found;
- the adjudicator's result sharply conflicts with earlier conclusions for reasons that are not yet explained.

The second-opinion reviewer receives raw evidence provenance and neutral candidate claims, plus only the dossier material needed to audit added premises. Hide the coordinator's favorite and adjudicator winner.

The reviewer reconstructs the decisive inference rather than merely rereading polished dossiers.

## 21. Belief versus decision

Convergence Guard produces two linked but distinct outputs.

### Model judgment

What causal model or combination is best supported, with what relation type and what unresolved uncertainty?

### Decision judgment

What action is best given the plausible model set and the decision contract?

A less likely model may still change the rational action when its downside is severe or when one action performs well across multiple plausible models.

Consider qualitatively or quantitatively, when defensible:

- expected loss;
- regret;
- reversibility;
- lock-in;
- option value;
- value of information;
- hard safety constraints.

Never invent probabilities, utilities, or precision that the evidence does not support.

## 22. Evidence-sufficiency gate

A best action is defensible only when:

- no unresolved hard factual contradiction invalidates it;
- it is preferable across the plausible surviving model set under the decision contract;
- no unresolved alternative is likely to reverse the action without requiring evidence that can reasonably be obtained first;
- residual uncertainty is explicit and bounded;
- downside and reversibility are understood enough for the stakes.

Otherwise use `INSUFFICIENT DATA TO CHOOSE`.

## 23. Minimum discriminating observation / experiment

The final learning step should be **decision-changing**, not merely informative.

Specify when relevant:

- what is measured or observed;
- competing predictions;
- threshold/pattern that changes the action;
- sample or time window when needed;
- confounders and guardrails;
- stopping rule;
- action under each material outcome.

When experimentation is impossible, unethical, or unnecessary, use an audit, observation, comparison, or natural experiment.

Prefer “disconfirming” or “decision-invalidating” evidence over absolute “falsification” in noisy domains where no single observation can logically falsify a model.

## 24. Reduced Mode boundary

Reduced Mode is defined separately in [reduced-mode.md](reduced-mode.md). It is not a cheaper Full Mode and must never be described as equivalent to genuinely isolated execution.

## 25. Cost model

Typical rigorous Full Mode with three search workers and three finalists:

```text
3 isolated search workers
+ 1 fresh screener
+ 1 fresh blind mapper
+ 3 isolated dossier workers
+ 1 fresh slate adjudicator
= 9 independent worker contexts
```

With two finalists, baseline is 8 contexts.

Conditional additions:

- +1 or +2 search workers if the coverage gate fails;
- +1 boundary critic only for decision-relevant map ambiguity;
- +1 reframe reviewer when framing risk is material;
- +1 independent second opinion when its trigger fires.

Rigor is defined by preserved information barriers and decision checks, not by maximizing worker count.
