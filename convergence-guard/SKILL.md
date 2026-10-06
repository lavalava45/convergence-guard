---
name: convergence-guard
description: "Use this skill for high-stakes, open-ended decisions, diagnoses, architecture, strategy, research, or design problems where several causal explanations or actions remain plausible and premature convergence would be costly. Ground evidence, define the decision, search causally distinct models in isolated contexts, reduce them without anchoring, stress-test the strongest alternatives, separate model belief from action choice, and finish with a decision-changing observation or experiment. Do not use for simple lookups, known-root-cause bugs, syntax fixes, or routine procedures."
license: MIT
compatibility: "Full Mode requires controllable context boundaries for every operation that depends on isolation or blindness. A separate worker, chat, thread, or session is not sufficient if decision-relevant material can enter through parent conversation context, chat history, memory, project context, shared state, retrieval, or prior worker history. Hosts that cannot guarantee the required boundary may use the explicitly labeled Reduced Mode only with user consent."
metadata:
  author: "Convergence Guard contributors"
  version: "0.2.1"
---

# Convergence Guard

Convergence Guard is a decision-analysis protocol for problems where the main failure mode is **premature convergence**: accepting one plausible causal story or action before decision-relevant alternatives have been separated and tested.

It is not a vote among agents. Informationally isolated workers can still share model priors, training biases, evidence, and framing. **Reasoning independence is not evidential independence.** Agreement among workers never counts as independent real-world confirmation by itself.

## Core invariants

1. Separate evidence provenance, inference, assumptions, constraints, and unknowns before generating models.
2. Search for causally distinct models in genuinely isolated contexts when running Full Mode.
3. Keep early quality screening hidden from causal-space mapping.
4. Do not count duplicate or near-duplicate models as corroborating evidence.
5. Distinguish causal plausibility from the best action under uncertainty.
6. Allow models to be mutually exclusive, coexisting, nested, or interacting; do not force every comparison into `A OR B`.
7. Prefer models and actions that create distinguishable, decision-relevant predictions.
8. Converge only when the evidence and decision criteria support a defensible action. Otherwise return an explicit insufficiency result plus the most informative next observation or test.
9. Use the user's language for the final answer unless the user requests another language.

## Activation and modes

Use Convergence Guard when:

- at least two causally distinct explanations or actions remain plausible;
- a wrong early commitment would materially waste resources, hide the real cause, create lock-in, or cause a hard-to-reverse error;
- additional observations, comparisons, or interventions could reduce decision-relevant uncertainty;
- the task is open enough to justify structured analysis.

Do **not** use the full protocol for simple factual lookup, routine procedure, syntax edits, a known-root-cause bug, or a case where factual inspection leaves only one viable action.

### Full Mode

Full Mode requires genuine context isolation for every operation whose value depends on independence or blindness. Never simulate several sequential personas in one context and report that as a Full Mode run.

A separate worker, chat, thread, window, or session is **not by itself evidence of isolation**. Isolation is a property of the worker's effective input boundary, not of the user-interface container.

For each isolation-dependent operation, treat the stage inputs defined by this protocol as an explicit **context allowlist**. In addition to host/system/safety instructions, the worker may receive only the evidence and stage inputs that the protocol authorizes for that role.

The worker must not receive or retrieve decision-relevant material outside that allowlist through:

- parent-conversation transcript or summaries;
- sibling-worker tasks, outputs, or conclusions;
- prior candidate outputs or rankings;
- account memory or referenced chat history;
- project-level cross-chat context;
- shared scratchpads, handoffs, summaries, or retrieval indexes containing prior conclusions;
- persisted history from a reused worker;
- coordinator preferences or selection signals that the stage is meant to be blind to.

Real-world facts are not forbidden merely because they were previously observed. If such information is relevant, include it explicitly in the factual brief with appropriate provenance rather than allowing a worker to inherit an earlier interpretation or conclusion implicitly.

If the runtime can inject or retrieve forbidden decision-relevant context, or if the relevant boundary cannot be established with reasonable confidence, that operation does not satisfy Full Mode. Use Reduced Mode and state the limitation explicitly.

### Reduced Mode

If isolation is unavailable, Full Mode is unavailable. With explicit user consent, use [Reduced Mode](references/reduced-mode.md), label it clearly, and do not claim independent-agent confirmation or blind-stage guarantees.

For the Chat On Steroids installation profile, read [references/runtime-chat-on-steroids.md](references/runtime-chat-on-steroids.md) before a Full Mode run.

# Phase A — Establish the decision

## A1. Factual grounding

When the problem depends on external state, build a compact evidence brief. Track provenance explicitly:

- **CONFIRMED** — directly observed in code, data, logs, documentation, measurements, or another inspectable source;
- **REPORTED** — stated by a user, witness, operator, or secondary source but not independently inspected in this run;
- **STRONGLY INFERRED** — supported by a coherent evidence chain but not directly observed;
- **HYPOTHESIS / ASSUMPTION** — plausible but unverified;
- **CONSTRAINT** — a real boundary such as time, budget, policy, compatibility, safety, architecture, or an explicit user decision;
- **OPEN QUESTION** — an unknown that could materially change the decision.

Do not silently upgrade `REPORTED` or `STRONGLY INFERRED` evidence to `CONFIRMED`.

Give all independent search workers the same factual brief. Existing plans, TODOs, previous recommendations, and current architecture are context, not proof that the current framing is correct.

## A2. Decision contract

Define:

1. **Decision question** — what must be chosen, explained, prioritized, or ruled out?
2. **Scope** — what may be reframed and what is fixed?
3. **Success criterion** — what observable outcome makes one action better?
4. **Forbidden substitutions** — what must the analysis not silently turn into?
5. **Loss / cost of error** — what is damaged if the choice is wrong?
6. **Reversibility** — how difficult is it to recover or change course?

## A3. Framing and outside-view check

Ask: **Are we solving the right problem?** Check for upstream causes, proxy objectives, inherited constraints, missing system boundaries, and alternate formulations that would materially change the decision.

When a meaningful reference class exists, record relevant base rates or outside-view evidence before deep candidate refinement. Do not let a generic base rate override strong case-specific evidence; use it as a calibration input.

Use the optional independent reframe review or retrospective causal reconstruction only when their triggers apply. See [protocol details](references/protocol-details.md).

# Phase B — Search the causal space

## B1. Generate search mandates

Start with **three** problem-specific search mandates. A mandate is not a persona. Neighboring mandates should differ materially along at least two useful dimensions such as:

- system boundary;
- intervention point;
- resource or coordination constraint;
- dynamic behavior or feedback structure;
- expected evidence;
- counterfactual boundary.

Each isolated worker's effective decision-relevant context must contain only the shared evidence brief, decision contract, material alternate framing, and its own mandate. This requirement applies both to explicitly supplied inputs and to ambient or automatically retrieved context such as memory, chat history, project context, shared state, or prior worker history.

Each worker returns **2–4 causal models**. Each model must include:

- claim;
- mechanism;
- necessary conditions;
- observable prediction(s);
- action implied if the model is true;
- evidence that would weaken or disconfirm it;
- known causal-identification threats such as confounding, reverse causality, selection effects, or ambiguous temporal order;
- conflicts with confirmed evidence.

A worker may report that its mandate yields no viable model.

## B2. Coverage gate and adaptive expansion

After the initial three workers finish, test coverage rather than automatically paying for two more workers.

Expand to **four or five** isolated search workers only when at least one condition is true:

- mandates or outputs cover substantially the same causal region;
- a major system boundary or intervention class remains unexamined;
- fewer than two decision-relevant causal families survive basic factual sanity checks;
- an outside-view or framing check exposes a plausible missing family.

Expansion workers receive no prior branch outputs. Give them only the shared brief, contract, relevant framing, and a new mandate targeted at the uncovered region.

Assign neutral IDs to all candidate models before Phase C.

# Phase C — Reduce without anchoring

Run **C1 screening and C2 causal mapping in parallel** using separate fresh contexts. Both receive the neutralized candidate set, but neither sees the other's output.

## C1. Independent contract screening

Do not create an aggregate score. For each candidate record:

- **Contract fit:** PASS / CONDITIONAL / FAIL
- **Evidence support:** STRONG / MIXED / WEAK
- **Causal completeness:** CHAIN PRESENT / PARTIAL / ASSERTION ONLY
- **Causal identification:** SUPPORTED / THREATENED / UNIDENTIFIED, with the main threat named
- **Discriminability:** HIGH / MEDIUM / LOW
- **Decision exposure if wrong:** LOW / MEDIUM / HIGH, including reversibility

Flag attractive-but-dangerous candidates that depend on goal substitution, hidden cost, untestability, factual conflict, or material constraint violations.

Freeze these results.

## C2. Blind causal map

The mapper receives candidate claims, mechanisms, necessary conditions, predictions, implied actions, and disconfirming evidence — but **not** screening results, branch identity, danger flags, or coordinator preference.

Map candidates into causal families without targeting a fixed cluster count. Record relations where relevant:

- **EXCLUSIVE** — both cannot be materially true in the decision context;
- **COEXISTING** — both may be true at the same time;
- **NESTED** — one is a special case or component of another;
- **INTERACTING** — the outcome depends on their interaction.

Near-duplicates may be merged for representation, but preserve source IDs and **never count duplicate formulations as independent support**.

Freeze the map.

## C3. Conditional boundary audit

Use a fresh boundary critic only for disputed merges, uncertain relation types, or neighboring families whose distinction could change the decision. Skip this operation when the map has no decision-relevant ambiguity.

## C4. Build the decision-relevant slate

Now combine the frozen screening and frozen causal map.

Select **2–3 causally distinct model finalists**. Never pad to three.

Prefer non-dominated candidates that differ in mechanism or decision consequence. Record why any strong non-dominated outside model was excluded.

Separately choose at most one **information probe**: a viable model or uncertainty that is especially valuable to test. It is not automatically a finalist and should not be treated as one merely because its test is informative.

If missing evidence or a missing causal family could materially change the slate, pause and perform a targeted evidence/search checkpoint, then rerun only the affected operations.

# Phase D — Stress and adjudicate

## D1. Independent causal dossiers

Create one fresh isolated dossier worker per finalist. Each worker receives the evidence brief, decision contract, and **one finalist only**.

Require:

1. causal mechanism;
2. load-bearing assumptions;
3. observable predictions;
4. concrete disconfirming or decision-invalidating observations;
5. decision consequence if the model is true;
6. causal-identification weaknesses;
7. cost and reversibility of acting on the model and being wrong.

The dossier worker does **not** compare against a rival it cannot see.

If a dossier materially changes the mechanism or adds a new load-bearing premise, create a new hypothesis ID and route that revised model back through the affected screening/mapping/slate steps instead of laundering it into a stronger finalist.

Optional premortem and stakeholder lenses run after the dossier only when triggered. See [protocol details](references/protocol-details.md).

## D2. Fresh slate-level adjudication

Use a fresh adjudicator that did not author the search branches, screening, mapping, or dossiers. Give it the neutral finalist dossiers, evidence brief, contract, and relevant outside alternative. Hide early screening ranks/selection roles and coordinator preference.

The adjudicator performs three operations in order.

### Assumption sensitivity

Select assumptions by **uncertainty × causal leverage × decision sensitivity**. Mutate one assumption at a time. If two assumptions are similarly load-bearing, analyze them separately rather than declaring robustness from one convenient mutation.

For each tested assumption classify the recommendation response as:

- **ROBUST** — recommendation survives the plausible mutation;
- **CONDITIONAL** — recommendation survives only within an explicit boundary;
- **BROKEN** — recommendation fails or reverses.

These labels describe sensitivity under the tested mutation, not probability that the model is true.

### Shared-bias audit

Check for:

- common hidden assumption;
- missing evidence class or missing causal family;
- proxy/objective substitution;
- population or observation-boundary bias;
- common data ancestry masquerading as independent support;
- outside-view/base-rate conflict;
- shared causal-identification weakness.

If this exposes a potentially missing causal family or decisive missing evidence, do not merely replace finalists from the same pool. Route to targeted new search or evidence collection.

### Pairwise decision collision

Compare every existing finalist pair — one pair for two finalists, three pairs for three finalists.

Do not force coexisting or interacting models into a false winner/loser duel. Compare them only where their implications for action conflict.

For each decision-conflicting pair identify:

- the materially different prediction or condition;
- the fact or observation that could flip the action preference;
- which action is favored on current evidence, if defensible;
- `UNDETERMINED` when the evidence does not justify a preference.

A preference cycle may indicate criterion drift, model interaction, or missing evidence. Do not average it into a synthetic score.

## D3. Conditional independent second opinion

Use a new second-opinion reviewer when pairwise results are cyclic or repeatedly `UNDETERMINED`, evidence for the apparent winner remains weak, the decision is unusually hard to reverse, or the adjudicator exposes a serious shared blind spot.

The reviewer should reconstruct the decisive inference from **raw evidence provenance plus neutral candidate claims** and audit unsupported additions made during dossier refinement. Hide the coordinator's favorite and the adjudicator's winner.

# Phase E — Converge on action and learning

## E1. Separate belief from action

First state the **model judgment**: which causal model(s) are best supported, how they relate, and what major uncertainty remains.

Then make a separate **decision judgment** over feasible actions. Evaluate actions across the surviving plausible models using the decision contract, including:

- expected loss or downside when estimable;
- regret if the chosen action is wrong;
- reversibility and lock-in;
- option value of waiting or preserving flexibility;
- information value of an action that also teaches;
- safety or hard constraints.

Do not invent numeric utilities or probabilities when the evidence does not support them. Qualitative dominance and low-regret reasoning are acceptable when explicit.

A less likely model can still justify the best action if that action is safer, more reversible, or performs well across several plausible models.

## E2. Evidence-sufficiency gate

Choose one best action only when all are true:

- no unresolved hard factual contradiction invalidates it;
- it is preferable under the decision contract and plausible surviving models;
- no unresolved alternative would plausibly reverse the action without also requiring evidence that can be obtained before commitment;
- residual uncertainty is stated and bounded;
- the action's downside and reversibility are understood well enough for the stakes.

Otherwise return `INSUFFICIENT DATA TO CHOOSE` and identify the one observation or test with the highest practical decision value.

## E3. Minimum discriminating observation or experiment

End with the cheapest practical next step that can change the decision, not merely add information.

Specify where relevant:

- measure or observation;
- rival predictions;
- decision threshold or pattern that matters;
- sample size or time window when the domain requires it;
- major confounders and guardrails;
- stopping rule;
- action to take under each material outcome.

If experimentation is impossible or unethical, use a discriminating observation, audit, comparison, or natural experiment instead.

## User-facing output

Keep the answer simpler than the internal workflow. Default to:

1. **Best action / main conclusion**
2. **Model judgment** — what appears to be happening and why
3. **Why this action under uncertainty**
4. **Strongest alternative or interaction**
5. **What could change the decision**
6. **Minimum discriminating observation / experiment**
7. **Material risks, shared biases, or dangerous candidates**

Do not dump stage logs unless the user asks for the audit trail. Use the user's language unless another language is requested.

## Integrity rules

- Fresh worker contexts provide information isolation, not independent external evidence.
- A fresh chat or fresh worker is not proof of context isolation; Full Mode depends on the effective decision-relevant input boundary, including ambient memory, history, project context, retrieval, and persisted worker state.
- Never let branch count become a vote count.
- Never count duplicate models as corroboration.
- Never create a hidden aggregate score from categorical screening.
- Never reveal screening results to the blind mapper before its map is frozen.
- Never rewrite a candidate's mechanism during dossier work without creating a new hypothesis ID and rerouting it.
- Never force three finalists when only two are viable.
- Never force mutually compatible models into false exclusivity.
- Never declare `ROBUST` from a single convenient assumption test when another assumption is comparably load-bearing.
- Never force a recommendation merely because the protocol reached the end.
- On coordination failure, recover completed work and rerun only missing operations.
- For analysis-only requests, stop after the decision and discriminating next step unless implementation is separately requested.

## References

- [Detailed protocol rules](references/protocol-details.md)
- [Reduced Mode](references/reduced-mode.md)
- [Chat On Steroids runtime profile](references/runtime-chat-on-steroids.md)
- [Historical Russian v0.1.0 protocol](references/protocol.ru.md)

Convergence Guard is a decision-analysis protocol, not a source of truth. Facts, safety constraints, explicit user decisions, and project rules take precedence.
