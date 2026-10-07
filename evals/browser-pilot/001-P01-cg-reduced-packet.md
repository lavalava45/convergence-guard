# Browser Pilot Packet 001

RUN_ID: P01-r1-cg-reduced
CASE_ID: P01
MODE: cg-reduced
CG_COMMIT: fda4395b37c782de3e6d79ab41d59b208d39e88f

## Participant wrapper

This is a controlled evaluation run.

Use only the material in this packet. Do not browse the web, use Connected Apps, retrieve other chats, or add facts from outside the packet.

Treatment: **Convergence Guard — Reduced Mode (no independent worker isolation)**.

Execute the Reduced Mode protocol in this single conversation. The embedded Convergence Guard files are the operational instructions for this treatment. Where the full skill discusses Full Mode isolation, do not claim those guarantees; follow the Reduced Mode fallback rules.

Do not ask the user questions. Do not request more files. Do not reveal or discuss the evaluation design.

At the end, return **exactly one JSON object and nothing else**. Do not wrap it in Markdown fences. The JSON must conform to the embedded OUTPUT-SCHEMA and use `case_id` = `P01`.

---

# PARTICIPANT-VISIBLE CASE

# P01 — Checkout service failure after deployment

You are on call for a checkout service. At 10:02 a deployment completed. Within two minutes, most checkout requests began returning HTTP 503.

Your task is to determine what causal conclusion is justified by the available evidence and what action should be taken now.

Constraints:

- restore checkout quickly;
- avoid data-destructive actions;
- a deployment rollback or configuration correction is reversible;
- do not use the open web;
- do not assume facts that are not in the supplied evidence.

Return the required normalized final-answer object.

## Evidence E01

2026-10-06T10:03:11Z checkout-7d9f startup INFO  configuration loaded
2026-10-06T10:03:12Z checkout-7d9f db      ERROR getaddrinfo ENOTFOUND db-proxy-old.internal
2026-10-06T10:03:12Z checkout-7d9f health  WARN  dependency database unavailable
2026-10-06T10:03:13Z checkout-7d9f http    WARN  GET /health -> 503
2026-10-06T10:03:18Z checkout-7d9f db      ERROR getaddrinfo ENOTFOUND db-proxy-old.internal
2026-10-06T10:03:19Z checkout-7d9f http    WARN  POST /checkout -> 503 dependency unavailable

## Evidence E02

Deployment configuration diff at 10:02:

- DATABASE_HOST=db-proxy.internal
+ DATABASE_HOST=db-proxy-old.internal

No application-code files changed in this deployment.

## Evidence E03

Probe executed from the same runtime network namespace at 10:06:

db-proxy.internal
  DNS: resolves to 10.20.4.17
  TCP 5432: success

db-proxy-old.internal
  DNS: NXDOMAIN

## Evidence E04

10:00-10:10 runtime summary:

CPU utilization: 18-27%
Memory utilization: 43-46%
Pod restarts: 0
Database dependency check: FAIL
Other dependency checks: PASS

---

# CONVERGENCE GUARD SKILL

---
name: convergence-guard
description: "Analyze high-stakes, open-ended decisions, diagnoses, architecture, strategy, research, or design problems where competing explanations or actions remain plausible and premature commitment is costly. Not for simple lookups, known-root-cause bugs, or routine procedures."
license: MIT
compatibility: "Full Mode requires controllable context boundaries for every operation that depends on isolation or blindness. A separate worker, chat, thread, or session is not sufficient if decision-relevant material can enter through parent conversation context, chat history, memory, project context, shared state, retrieval, or prior worker history. Hosts that cannot guarantee the required boundary may use the explicitly labeled Reduced Mode only with user consent."
metadata:
  author: "Convergence Guard contributors"
  version: "0.2.2"
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

A negative sentinel probe or worker self-report means only `NO LEAK OBSERVED`, not confirmed isolation. Establish each required boundary through runtime-level evidence covering both initial context and later retrieval/tool access; otherwise record `INCONCLUSIVE`. See [boundary assurance](references/protocol-details.md#11-boundary-assurance).

For API-based workers, construct each request from a fresh allowlisted message set: required host/system/safety instructions plus the role's authorized inputs. Do not attach parent conversation/session state; restrict memory, retrieval, and tool access to the same boundary, including on follow-up calls. A fresh API call or a low temperature alone does not prove isolation. Use model-supported generation settings; this protocol does not prescribe `temperature=0.2`.

### Reduced Mode

If isolation is unavailable, Full Mode is unavailable. With explicit user consent, use [Reduced Mode](references/reduced-mode.md), label it clearly, and do not claim independent-agent confirmation or blind-stage guarantees.

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

`CONFIRMED` applies to what was actually inspected, not automatically to every proposition asserted by an inspected source. For example, if an official report states that event X occurred, it may be `CONFIRMED` that the report makes that statement while event X itself remains `REPORTED` unless the underlying evidence is directly inspectable.

### A1.1 Claim-level source policy

For every material claim, evaluate the claim and its evidence chain rather than assigning truth by source reputation.

Prefer the nearest inspectable primary evidence when practical, but do not treat `primary`, `official`, `peer reviewed`, `institutional`, or `expert` as automatic truth labels.

Use primary material for factual traceability. For population-level or cumulative scientific claims, a transparent systematic review, meta-analysis, or other high-quality synthesis may be more decision-relevant than any single primary study when its methods and constituent evidence are traceable.

For decision-relevant claims, record where practical:

- nearest available primary source;
- source type;
- inspectability of the underlying evidence;
- method or data availability;
- temporal proximity to the event;
- independence / common evidence ancestry;
- known contradictions, material incentives, or conflicts;
- epistemic role in the current run.

Use these source roles:

- **EVIDENCE** — directly bears on the claim and is inspectable enough to support it;
- **CORROBORATION** — independently supports evidence already in the brief;
- **CONTEXT** — useful background that does not materially establish the claim;
- **LEAD ONLY** — points to a potentially relevant claim or source that must be traced before it can carry evidential weight;
- **UNSUPPORTED** — currently lacks enough inspectable support to influence the decision.

Source reputation may guide search priority, but **must not substitute for claim-level provenance**.

Secondary sources are useful for orientation and discovery, but trace material claims to the nearest available primary evidence when feasible.

Advocacy, partisan, fringe, anonymous, or otherwise low-verifiability sources are not automatically excluded. They may generate leads. If they expose directly inspectable underlying evidence, evaluate that material under the same claim-level rules as any other source; if the underlying support cannot be established, keep the claim `LEAD ONLY`, `REPORTED`, or `UNSUPPORTED` as appropriate.

When an institution or intelligence body publishes an assessment whose underlying evidence is classified or unavailable, it may be `CONFIRMED` that the assessment exists and has a stated confidence level; the hidden supporting evidence itself is not `CONFIRMED`.

Do not multiply support by media repetition or citation count. If several reports descend from one upstream observation, dataset, leak, paper, briefing, or document, treat them as one evidential branch unless genuine independence is established.

Preserve contradictory primary evidence explicitly instead of averaging it away or resolving it by source prestige alone.

Treat incentives, affiliation, funding, ideology, or conflicts of interest as possible bias channels to investigate, **not** as automatic evidence that a claim is false. Likewise, unavailable raw data reduce inspectability but do not by themselves prove that a claim is false.

During isolation-dependent stages, a worker may surface a new source or evidence lead, but it must not silently promote branch-private retrieval into shared factual grounding. Route any material new evidence through an evidence checkpoint, classify its provenance/source role, update the shared brief, and rerun only affected operations. This keeps causal branches comparable on the evidence that actually carries decision weight.

Give all independent search workers the same factual brief. Existing plans, TODOs, previous recommendations, and current architecture are context, not proof that the current framing is correct.

## A2. Decision contract

Define:

1. **Decision question** — what must be chosen, explained, prioritized, or ruled out?
2. **Scope** — what may be reframed and what is fixed?
3. **Success criterion** — what observable outcome makes one action better?
4. **Forbidden substitutions** — what must the analysis not silently turn into?
5. **Loss / cost of error** — what is damaged if the choice is wrong?
6. **Reversibility** — how difficult is it to recover or change course?
7. **Analysis budget** — finite limits on time or calls and corrective cycles, chosen within the user's constraints before search. By default allow at most two corrective cycles across the entire run. One cycle is a targeted evidence/search/model-revision return plus its affected downstream reruns, not each worker call. All phases share the budget; recovery retries consume the time/call limit, and changing phases never resets it. Stop at any limit or after a cycle without new decision-relevant evidence, a viable mechanism, resolved uncertainty, or changed decision implications. See [checkpoint and stopping rules](references/protocol-details.md#131-run-budget-and-stopping).

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

The mapper receives the same shared evidence brief and decision contract as the screener, including system boundaries and constraints, plus candidate claims, mechanisms, necessary conditions, predictions, implied actions, and disconfirming evidence — but **not** screening results, branch identity, danger flags, or coordinator preference.

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

Normally select **2–3 causally distinct model finalists**. Never pad the slate. If exactly one viable model remains after C1/C2, check whether missing evidence or search coverage explains the collapse; if not, retain one finalist, run D1 and D2's sensitivity/shared-bias checks, and skip pairwise collision (zero pairs). D3 triggers still apply. If none remain, use a budgeted checkpoint where useful; otherwise proceed to E with no supported model and explicit insufficiency for causal attribution. Do not promote a rejected model to fill a slot.

Prefer non-dominated candidates that differ in mechanism or decision consequence. Record why any strong non-dominated outside model was excluded.

Separately choose at most one **information probe**: a viable model or uncertainty that is especially valuable to test. It is not automatically a finalist and should not be treated as one merely because its test is informative.

If missing evidence or a missing causal family could materially change the slate, perform a targeted evidence/search checkpoint within the run budget, then rerun only the affected operations. All corrective returns, including revised dossiers and shared-bias findings, share that budget. Stop on budget exhaustion or a completed corrective cycle without material progress; proceed to E with explicit limitations, without declaring incomplete stages complete.

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

Mark such revisions `PENDING` until all affected C and D checks, including D2 and any triggered D3 review, are complete against the current evidence and contract. If the budget ends mid-return, preserve the pending revision and its invalidating observations without promoting it. Reuse earlier completed results only where still valid under current evidence; never restore an obsolete slate automatically. If a pending issue could reverse the action, E2 must return insufficiency for that commitment. No prior completed slate means no adjudicated winner.

Optional premortem and stakeholder lenses run after the dossier only when triggered. See [protocol details](references/protocol-details.md).

### Optional probe mini-dossier

If C4's information probe needs elaboration for E3, the coordinator may prepare a separate planning note after C is frozen, within the same budget: target uncertainty and source IDs, contrasting predictions, decision-changing outcomes, feasibility/cost, and confounders. It is not a finalist, independent validation, or an extra mandatory worker. Keep it out of isolated finalist dossier inputs; pass it separately to E3 and recheck it against the final model judgment. New evidence or a materially revised causal model still requires the usual checkpoint; if none is needed, design the test directly in E3.

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

Compare every existing finalist pair — zero pairs for one finalist (skip collision only), one pair for two finalists, three pairs for three finalists. A single finalist still receives assumption sensitivity and the shared-bias audit; absence of rivals does not establish correctness.

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
- no pending check could plausibly reverse the action, is obtainable before commitment, and is worth its cost and delay under the decision contract; perform such a check first, then reassess;
- residual uncertainty is stated and bounded;
- the action's downside and reversibility are understood well enough for the stakes.

Otherwise return `INSUFFICIENT DATA TO CHOOSE` and identify the one observation or test with the highest practical decision value, if one is available. Budget exhaustion does not waive this gate: report an outstanding worthwhile check as deferred, not completed.

## E3. Minimum discriminating observation or experiment

When available and worthwhile, end with the cheapest practical next step that can change the decision, not merely add information.

Specify where relevant:

- measure or observation;
- rival predictions;
- decision threshold or pattern that matters;
- sample size or time window when the domain requires it;
- major confounders and guardrails;
- stopping rule;
- action to take under each material outcome.

If experimentation is impossible or unethical, consider a discriminating observation, audit, comparison, or natural experiment if feasible.

If no ethical, obtainable, decision-relevant discriminator is available, state `NO FEASIBLE DISCRIMINATOR IDENTIFIED` and why. Do not invent a test or promise future evidence. Keep unresolved model judgment separate from action: choose a robust low-regret action only if E2 supports it; otherwise retain `INSUFFICIENT DATA TO CHOOSE`. If search stopped at the budget limit, say that no discriminator was identified within that search, not that none exists. An already known but deferred check is not this terminal state.

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
- Never pad the slate when fewer than three finalists are viable.
- Never force mutually compatible models into false exclusivity.
- Never declare `ROBUST` from a single convenient assumption test when another assumption is comparably load-bearing.
- Never force a recommendation merely because the protocol reached the end.
- On coordination failure, recover completed work and rerun only missing operations.
- For analysis-only requests, stop after the decision and discriminating next step unless implementation is separately requested.

## References

Install the entire `convergence-guard/` directory, including `references/`, and resolve links relative to it. A single-file loader must explicitly bundle/inline the required operational references for the selected mode. The entrypoint retains essential isolation, budget, and pending-revision guards, but does not replace missing mode instructions. If a required reference cannot be read, report the affected stage as unavailable; never invent omitted rules or claim a complete run. The historical protocol is archival, not a current runtime dependency.

- [Detailed protocol rules](references/protocol-details.md)
- [Reduced Mode](references/reduced-mode.md)
- [Historical Russian v0.1.0 protocol](references/protocol.ru.md)

Convergence Guard is a decision-analysis protocol, not a source of truth. Facts, safety constraints, explicit user decisions, and project rules take precedence.

---

# REDUCED MODE REFERENCE

# Convergence Guard — Reduced Mode

Reduced Mode is a single-context fallback for hosts that cannot create genuinely isolated worker contexts.

It preserves the **shape** of the reasoning protocol but not its strongest anti-anchoring guarantees. It must never be presented as equivalent to Full Mode.

## When it is allowed

Use Reduced Mode only when:

- Full Mode isolation is unavailable; and
- the user explicitly accepts the limitation; and
- the task is not so consequential that pretending to compensate for missing independence would be irresponsible.

Label the result clearly as:

`Convergence Guard — Reduced Mode (no independent worker isolation)`

## What guarantees are lost

Reduced Mode cannot honestly provide:

- independent causal-search contexts;
- blind screening versus mapping in separate contexts;
- independent dossier authorship;
- independent second-opinion reconstruction.

Sequential sections in one context remain vulnerable to shared anchoring and memory effects.

## Reduced workflow

1. Build the evidence brief and decision contract, including the same finite run budget and corrective-cycle stopping rules as Full Mode (see [protocol details §13.1](protocol-details.md#131-run-budget-and-stopping)).
   Apply the same claim-level source-quality and provenance rules as Full Mode; Reduced Mode relaxes context-isolation guarantees, not evidence standards.
2. Perform the framing/outside-view check.
3. Generate at least three deliberately different search mandates **before** generating candidate models.
4. Complete each mandate in a separate labeled pass without editing earlier candidate outputs.
5. Create a causal map and contract screening, explicitly noting that blindness is not guaranteed.
6. Normally select 2–3 causally distinct finalists without aggregate scoring. If only one viable model remains after checking for missing evidence or search coverage, retain that one rather than padding the slate. If none remain, skip dossier/tournament work and carry the causal insufficiency forward to the action gate.
7. Build compact causal dossiers for the actual finalists.
8. Stress load-bearing assumptions and audit shared blind spots even when only one finalist remains.
9. Compare decision-conflicting finalist pairs when at least two finalists exist; with one finalist, skip pairwise comparison only.
10. If a dossier materially changes a mechanism or adds a new load-bearing premise, create a new hypothesis ID and mark it `PENDING` until the affected screening/mapping/stress checks are rerun. Never transfer the old candidate's validation to the revised one merely because the budget ended.
11. Keep any optional information-probe elaboration separate from finalist dossiers; it may support the final learning step but is not an extra finalist or independent confirmation.
12. Separate model judgment from action judgment.
13. Apply the evidence-sufficiency gate.
14. End with a feasible, worthwhile decision-changing observation or experiment. If none is identified, state `NO FEASIBLE DISCRIMINATOR IDENTIFIED` and the search limits; retain unresolved model judgment and apply the ordinary action-sufficiency gate. A known check deferred for budget reasons is not a no-discriminator result.

## Integrity rules

- Never call sequential passes “independent agents.”
- Never treat repeated agreement inside one context as corroboration.
- Preserve original candidate wording so later refinement cannot silently rewrite weak ideas.
- A pending revised hypothesis cannot become an adjudicated winner until its affected checks are rerun; budget exhaustion does not validate it.
- Be more willing than Full Mode to conclude `INSUFFICIENT DATA TO CHOOSE` when the missing isolation could matter.
- For very high-stakes decisions, recommend an external independent review or additional real-world evidence rather than adding more simulated internal critics.

---

# PROTOCOL DETAILS

# Convergence Guard v0.2.2 — Detailed Protocol Rules

This file contains operational details that are intentionally kept out of the main `SKILL.md`. Read only the sections relevant to the current run.

## 1. Independence model

Convergence Guard uses several distinct kinds of independence. Do not conflate them.

- **Context isolation**: one worker does not see another worker's output.
- **Preference blindness**: a reviewer does not see earlier rankings, favorites, or authorship.
- **Evidential independence**: two real-world observations come from genuinely separate evidence sources.

Only the first two can be created by worker orchestration. They do **not** create evidential independence. Multiple workers reasoning over the same evidence may reproduce the same bias.

A fresh worker is required when a stage relies on context isolation or preference blindness. Do not deprive a worker of relevant evidence merely to make it appear independent.

### 1.1 Boundary assurance

Separate a smoke-test observation from assurance about the runtime boundary. A harmless synthetic sentinel probe may produce `NO LEAK OBSERVED`, `FAIL` (forbidden context was exposed), or `INCONCLUSIVE`. A worker's negative self-report establishes only that the probe did not reveal leakage; it does not prove absence of access. Use no private user data and do not request hidden system prompts or private context.

For every boundary required by an operation, record runtime-level evidence: inspectable controls or trustworthy runtime documentation applicable to the active configuration. Cover initial context assembly and subsequent access through memory, history, project context, retrieval, shared state, and tools for the operation's duration. An explicit launch payload alone does not establish what the host adds or what the worker can retrieve later.

- `PASS` — runtime-level evidence supports the required boundary for the relevant channels and no observed leak contradicts it; record that evidence and its scope.
- `FAIL` — forbidden access or leakage is established.
- `INCONCLUSIVE` — relevant channels cannot be verified or controlled; a negative smoke test alone cannot produce `PASS`.

A required boundary with `FAIL` or material `INCONCLUSIVE` cannot support a Full Mode claim. Reassess when runtime, configuration, or available retrieval/tools change; an earlier `PASS` does not cover newly enabled channels. A persistence positive control that confirms a revived worker retains its history should be recorded as `RETENTION CONFIRMED`: it establishes that the worker is not fresh, not that parent/sibling isolation holds.

### 1.2 API integration and package loading

Build each isolated worker request from a fresh message set containing required host/system/safety instructions and only stage-authorized inputs. Do not attach parent conversation/session state or reuse a worker that has seen forbidden material. Restrict memory, retrieval, shared stores, and tools to the same allowlist throughout follow-up calls. Verify what the active host injects; a new API request is not sufficient evidence of isolation. Generation settings are model-dependent and are not isolation controls; no fixed temperature is required.

Distribute the entire skill directory with its operational references. A single-file adapter must explicitly inline/bundle required references for its selected mode. If a required dependency is missing, report the affected stage as unavailable rather than guessing omitted rules or claiming a complete run. The historical protocol is archival, not a current execution dependency.

## 2. Evidence provenance

Use these labels consistently:

- `CONFIRMED`: inspected directly in the current analysis or available primary evidence.
- `REPORTED`: asserted by a user, operator, witness, secondary source, or prior analysis but not independently inspected here.
- `STRONGLY INFERRED`: supported by a coherent evidence chain but not directly observed.
- `HYPOTHESIS / ASSUMPTION`: plausible but unverified.
- `CONSTRAINT`: a real decision boundary.
- `OPEN QUESTION`: an unknown capable of changing the action.

A user's direct observation can be highly valuable while still being `REPORTED` if the underlying event was not independently inspected. The label tracks provenance, not trustworthiness or importance.

Inspecting a source does not automatically confirm every proposition inside it. Distinguish:

- `CONFIRMED`: "document D states X";
- `REPORTED`: "X occurred", when D's underlying evidence is unavailable or uninspected.

### 2.1 Claim-level source-quality policy

Evaluate **claims**, not whole websites, journals, institutions, agencies, newspapers, or communities as globally true or false.

For each material claim, trace the evidence chain toward the nearest available inspectable source and record, where practical:

1. nearest primary source or raw observation;
2. source type;
3. inspectability;
4. method / raw-data availability;
5. temporal proximity;
6. common evidence ancestry;
7. known contradictory evidence;
8. material incentives or conflicts that could affect reporting or selection;
9. the source's permitted epistemic role in the current run.

Use:

- `EVIDENCE` — directly bears on the claim and is inspectable enough to support it;
- `CORROBORATION` — genuinely independent support for evidence already present;
- `CONTEXT` — background useful for interpretation but not material proof;
- `LEAD ONLY` — useful for discovering a claim, person, document, dataset, or hypothesis that must be traced before receiving evidential weight;
- `UNSUPPORTED` — insufficiently grounded to affect the decision.

#### Authority is not a truth label

`Official`, `government`, `peer reviewed`, `institutional`, `expert`, and `primary` describe provenance or process. None automatically establishes the truth of the claim.

Use an official source as the best source for what that institution officially said or recorded. Treat the underlying substantive proposition separately.

Peer review raises the cost of some classes of error but does not substitute for inspecting methods, data, selection, assumptions, corrections, retractions, expressions of concern, or independent replication where decision-relevant.

Primary evidence is normally preferred for direct factual grounding, but primary sources can still be mistaken, incomplete, deceptive, selected, contaminated, or poorly measured.

For aggregate scientific questions, a transparent systematic review, meta-analysis, or other high-quality synthesis may carry more decision-relevant evidential weight than a single primary study when its inclusion criteria, methods, and constituent evidence are inspectable. "Trace to primary" is a provenance rule, not a ban on synthesis.

#### Secondary and low-verifiability sources

Secondary sources are acceptable for orientation, synthesis, and source discovery. For a material disputed claim, descend to the nearest available primary evidence whenever practical.

Advocacy, partisan, activist, fringe, anonymous, or conspiracy-oriented sources are not automatically banned. Treat them primarily as **lead generators**. If they cite a concrete document, dataset, recording, or experiment, inspect that underlying material directly. If the underlying support cannot be established, the claim remains `LEAD ONLY`, `REPORTED`, or `UNSUPPORTED` as appropriate.

#### Inaccessible or classified support

If a public document states that a non-public evidence base supports conclusion X:

- it can be `CONFIRMED` that the institution made assessment X;
- its stated confidence level can be recorded;
- the inaccessible evidence itself cannot be counted as directly inspected;
- do not convert institutional confidence into model probability.

#### Common evidence ancestry

Do not count downstream repetition as independent corroboration.

Examples:

- five newspapers repeating one wire-service report are one upstream branch unless they add independent reporting;
- several articles using the same underlying dataset do not constitute several independent datasets;
- multiple agencies may still share one intelligence stream;
- multiple workers reading the same evidence do not create new real-world evidence.

When ancestry matters to the decision, record a compact source-dependency chain or graph.

#### Contradictions

Preserve material contradictory primary evidence in the brief. Do not resolve contradictions merely by counting sources or choosing the most prestigious institution.

Record what observation, provenance check, replication, or missing source could resolve the conflict.

#### Conflicts, incentives, and missing transparency

Funding, affiliation, ideology, institutional interest, personal incentive, or other conflicts identify possible bias mechanisms to inspect. They do not automatically discount evidence and are never sufficient by themselves to classify a substantive claim as false.

Similarly, unavailable raw data, classified support, missing records, or non-reproducibility reduce what can be verified. Absence of inspectability is a limitation on evidential weight, not positive evidence for the opposite proposition unless the missingness itself is independently diagnostic.

#### New sources discovered inside a blind branch

An isolation-dependent worker may identify a useful source, document, dataset, or search lead while developing its causal model. Treat that discovery as a proposed evidence update, not as branch-private factual privilege.

If the new material could change screening, mapping, the slate, or the decision:

1. return the source/claim as a lead with provenance;
2. inspect and classify it through the shared evidence process;
3. update the common evidence brief;
4. rerun only the affected downstream operations.

Do not let competing branches accumulate materially different private evidence bases and then interpret their different conclusions as causal independence.

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

- the same shared evidence brief and decision contract as the screener, including system boundaries and constraints;
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

Normally select **2–3 model finalists**, never padding the slate.

The finalist set should contain causally distinct, viable, decision-relevant models. Prefer non-dominated candidates rather than a single aggregate score.

For every strong non-dominated candidate left outside the slate, record one explicit exclusion rationale.

Separately identify at most one **information probe**. This is a model, uncertainty, or test target with high decision value. It is not automatically a finalist.

If fewer than two viable causal families remain after screening and mapping, check for missing evidence or search coverage; use a targeted checkpoint only when useful and within budget. With one genuine survivor, retain it for D1 and D2 sensitivity/shared-bias review; skip collision (zero pairs), retaining applicable D3 triggers. A lone survivor is not automatically confirmed. With none and no useful budgeted checkpoint, proceed to E without dossiers or a tournament: state no supported model and insufficiency for causal attribution. Any separate action must still satisfy E2. The pre-run activation rule for already obvious cases remains unchanged.

## 13. Evidence checkpoints

Do not let Phases A–D merely reprocess one frozen factual brief indefinitely.

Pause for targeted evidence collection when any of these occurs:

- the causal map exposes a missing evidence class that could change the slate;
- the shared-bias audit exposes a missing causal family;
- assumption sensitivity turns the leading action on an unresolved fact;
- pairwise collision is repeatedly `UNDETERMINED` because one obtainable fact is missing;
- a dossier exposes a direct contradiction with available primary evidence.

After new evidence arrives, rerun only the affected operations.

### 13.1 Run budget and stopping

Before Phase B, record finite total time or call limits and a maximum number of corrective cycles, respecting the user's constraints. Unless another limit is justified in the contract, allow at most **two corrective cycles across the whole run**. A cycle is a targeted return to evidence collection, search, or candidate revision plus its affected downstream reruns; it is not each worker call. The initial 3–5-worker coverage expansion remains inside the total time/call budget.

Before each return, identify the unresolved issue, the expected decision-relevant gain, and the affected operations. All returns, including dossier revisions and shared-bias findings, use the same budget; recovery retries also consume the total time/call budget. Do not reset limits by moving to another phase or renaming the issue.

Stop corrective work when any limit is reached, no feasible step can address the issue, or a completed cycle yields no material progress. Progress means new decision-relevant evidence, a substantively different viable mechanism, resolution of a material uncertainty, or a changed slate/action implication; rewording and repeated agreement do not count. Do not extend the budget automatically.

Preserve valid artifacts and proceed to Phase E with the stopping reason and unfinished work stated. Apply the ordinary sufficiency gate; exhaustion never establishes sufficiency or completion of skipped stages. If a worthwhile check remains outstanding, report it as deferred and return insufficiency for the commitment it blocks. Use the no-discriminator outcome only when no feasible check was identified, not merely because a known check exceeded the run budget.

### 13.2 Revision validity at a budget boundary

Associate frozen results with the hypothesis IDs, evidence/contract revision, and completed checks they depend on. A materially revised hypothesis is `PENDING` until affected C and D checks, including D2 and any triggered D3 review, are complete. Passing C1/C2 alone does not make it adjudicated.

If a return is interrupted, preserve the proposed revision and observations that could invalidate earlier work. Mark affected prior results invalid or pending; retain unaffected completed results only after checking applicability to current evidence and contract. Do not automatically restore the previous slate or transfer its validation to a changed mechanism. Budget exhaustion stops further work, not recording a discovered contradiction.

At E, separate still-valid completed judgments from pending candidates and unresolved threats. A pending revision cannot be an adjudicated winner; a decision-changing unresolved issue blocks commitment under E2. If no completed judgment remains valid, report no adjudicated winner and insufficiency for causal attribution. A separate robust action is permissible only on still-valid grounds that independently satisfy E2.

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

Apply §13.2 during that return; affected dossier/adjudication checks must also finish before the revision is treated as adjudicated.

### 14.1 Optional information-probe mini-dossier

If C4's probe needs elaboration for E3, the coordinator may prepare a separate planning note after screening/mapping are frozen: target uncertainty and source IDs, contrasting predictions, decision-changing outcomes, feasibility/cost, and confounders. It is not a finalist, independent validation, or an extra mandatory worker. Keep it out of isolated finalist workers' inputs. Pass it to E3 and check it against the final model judgment; route new evidence or revised mechanisms through the usual checkpoint. If the probe is already concrete, design the test directly in E3 without extra paperwork. The same budget and no-feasible-discriminator rules apply.

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

- One finalist: no pairs; skip collision only, retaining D1, D2 sensitivity/shared-bias review, and applicable D3 triggers.
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
- no pending check could plausibly reverse the action, is obtainable before commitment, and is worth its cost and delay under the decision contract; perform such a check first, then reassess;
- residual uncertainty is explicit and bounded;
- downside and reversibility are understood enough for the stakes.

Otherwise use `INSUFFICIENT DATA TO CHOOSE`.

Assess a check's practical value against its cost, delay, and the cost of committing incorrectly; exact numerical value-of-information estimates are not required. An unavailable or unjustifiably costly check does not automatically block action, but all other gate conditions still apply. Running out of analysis budget does not make an outstanding worthwhile check unnecessary.

## 23. Minimum discriminating observation / experiment

When a feasible, worthwhile learning step exists, it should be **decision-changing**, not merely informative.

Specify when relevant:

- what is measured or observed;
- competing predictions;
- threshold/pattern that changes the action;
- sample or time window when needed;
- confounders and guardrails;
- stopping rule;
- action under each material outcome.

When experimentation is impossible, unethical, or unnecessary, consider an audit, observation, comparison, or natural experiment if feasible.

If no ethical, obtainable, decision-relevant discriminator is available, return `NO FEASIBLE DISCRIMINATOR IDENTIFIED` with the limiting reason. This describes the learning opportunity, not the action judgment. Keep the causal models unresolved where appropriate; select a robust low-regret action only if the sufficiency gate supports it, otherwise also return `INSUFFICIENT DATA TO CHOOSE`. Do not invent a practical test from a merely hypothetical decisive fact. State the search limits, especially after budget exhaustion, rather than claiming that no possible discriminator exists. A known but deferred check is not a no-discriminator result.

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
With one finalist, baseline is 7 contexts; pairwise collision is skipped, but the dossier and slate-level sensitivity/shared-bias adjudication remain.
With zero finalists, dossier/pairwise work is skipped; this is an insufficiency path rather than a smaller "baseline Full Mode" configuration.

Conditional additions:

- +1 or +2 search workers if the coverage gate fails;
- +1 boundary critic only for decision-relevant map ambiguity;
- +1 reframe reviewer when framing risk is material;
- +1 independent second opinion when its trigger fires.

Rigor is defined by preserved information barriers and decision checks, not by maximizing worker count.

---

# REQUIRED FINAL OUTPUT SCHEMA

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Convergence Guard comparative eval final answer",
  "type": "object",
  "additionalProperties": false,
  "required": ["case_id", "causal_assessment", "action", "evidence", "uncertainty", "next_test"],
  "properties": {
    "case_id": {"type": "string", "minLength": 1},
    "causal_assessment": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "candidate_causes", "preferred_cause"],
      "properties": {
        "status": {"enum": ["CHOOSE", "COEXIST", "INSUFFICIENT"]},
        "candidate_causes": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["id", "claim"],
            "properties": {
              "id": {"type": "string", "minLength": 1},
              "claim": {"type": "string", "minLength": 1}
            }
          }
        },
        "preferred_cause": {
          "type": ["string", "null"],
          "description": "Candidate ID when status=CHOOSE; null for COEXIST or INSUFFICIENT."
        }
      },
      "allOf": [
        {
          "if": {"properties": {"status": {"const": "CHOOSE"}}},
          "then": {"properties": {"preferred_cause": {"type": "string", "minLength": 1}}}
        },
        {
          "if": {"properties": {"status": {"enum": ["COEXIST", "INSUFFICIENT"]}}},
          "then": {"properties": {"preferred_cause": {"type": "null"}}}
        }
      ]
    },
    "action": {
      "type": "object",
      "additionalProperties": false,
      "required": ["recommended_action", "reason"],
      "properties": {
        "recommended_action": {"type": "string", "minLength": 1},
        "reason": {"type": "string", "minLength": 1}
      }
    },
    "evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["evidence_ids", "claim"],
        "properties": {
          "evidence_ids": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string", "pattern": "^E[0-9]{2}$"}
          },
          "claim": {"type": "string", "minLength": 1}
        }
      }
    },
    "uncertainty": {
      "type": "array",
      "items": {"type": "string", "minLength": 1}
    },
    "next_test": {
      "type": "object",
      "additionalProperties": false,
      "required": ["test", "outcome_a_implication", "outcome_b_implication"],
      "properties": {
        "test": {"type": "string", "minLength": 1},
        "outcome_a_implication": {"type": "string", "minLength": 1},
        "outcome_b_implication": {"type": "string", "minLength": 1}
      }
    }
  }
}

---

# FINAL EXECUTION REMINDER

Perform the P01 analysis now in **Convergence Guard Reduced Mode** using only this packet.

Return exactly one JSON object, no Markdown and no prose outside the JSON.

Structural rules:
- `case_id` must be `P01`.
- `candidate_causes[].id` must be short neutral IDs such as `C1`, `C2`.
- If `status` is `CHOOSE`, `preferred_cause` must equal one candidate ID.
- If `status` is `COEXIST` or `INSUFFICIENT`, `preferred_cause` must be null.
- Cite only evidence IDs E01, E02, E03, E04.
- Do not alter your answer later unless the user explicitly starts a new run; the primary answer will be frozen before calibration.
