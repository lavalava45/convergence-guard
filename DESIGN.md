# Convergence Guard — Design Rationale

[Русская версия](DESIGN.ru.md)

> This document explains **why** Convergence Guard is designed the way it is. It is an architectural rationale, not the executable protocol. The canonical operational rules remain in [convergence-guard/SKILL.md](convergence-guard/SKILL.md) and [protocol-details.md](convergence-guard/references/protocol-details.md).

## 1. Problem statement

Convergence Guard is designed for decisions and analyses in which the dominant failure mode is not lack of ideas, but **premature commitment to one plausible explanation or action while decision-relevant alternatives remain unresolved**.

This class of problem appears in diagnosis, architecture, incident analysis, research, strategy, design, historical reconstruction, and other open-ended work where:

- several causal explanations can fit the same observations;
- evidence is incomplete, dependent, selected, or noisy;
- the first coherent story can become an anchor;
- later reasoning can silently inherit that anchor;
- the most plausible explanation may not imply the best action;
- the cost of a confident mistake can exceed the cost of preserving uncertainty.

The protocol therefore optimizes for **calibrated convergence**, not fast consensus.

Its central design question is:

> How can a reasoning system narrow an open causal space without allowing early framing, correlated evidence, hidden context, or decision pressure to manufacture false confidence?

---

## 2. Design goals

Convergence Guard has six primary goals.

### G1. Preserve alternative causal explanations long enough to test them

The system should resist collapsing around the first coherent model before materially different causal mechanisms have been explored.

### G2. Keep evidence strength distinct from reasoning repetition

Several workers repeating the same inference over the same evidence must not be mistaken for several independent real-world confirmations.

### G3. Make causal claims discriminating rather than merely coherent

A useful model must expose what it predicts, what assumptions it needs, and what observation would weaken or distinguish it.

### G4. Prevent evaluation from contaminating representation

The structure of the candidate space should not be determined by early quality scores or coordinator preference.

### G5. Separate belief about causes from choice of action

The most plausible model is not automatically the best basis for action when loss, reversibility, regret, option value, or safety differ across actions.

### G6. Stop honestly when the evidence is insufficient

The protocol must be able to terminate with INSUFFICIENT DATA TO CHOOSE and a decision-changing next observation instead of fabricating precision.

---

## 3. Non-goals

Convergence Guard is not designed to:

- maximize the number of agents or ideas;
- create artificial disagreement;
- produce a vote among workers;
- guarantee truth through multi-agent consensus;
- replace domain evidence with internal debate;
- assign probabilities where the evidence does not support quantitative calibration;
- force every problem into exactly three finalists;
- force mutually compatible causes into winner/loser comparisons;
- run Full Mode when the runtime cannot provide the required information boundaries;
- add process overhead to simple lookups, routine procedures, or known-root-cause problems.

### 3.1 Why Full Mode has an activation gate

Full Mode is justified only when the problem actually contains unresolved causal or action alternatives and premature commitment could cause material loss, lock-in, or missed cause.

The activation gate asks whether:

- at least two causally distinct explanations or actions remain plausible;
- an early mistake would matter;
- additional observations or comparisons could reduce decision-relevant uncertainty;
- the problem is open enough to benefit from structured causal search.

If those conditions are absent, the protocol should not manufacture complexity. This is the first control against T11: rigor begins by deciding whether the expensive reasoning structure is warranted at all.

---

## 4. Threat model

The architecture is derived from a set of failure modes. Each threat below can create false confidence even when every individual reasoning step appears locally plausible.

### T1. Premature convergence

The first plausible explanation becomes an anchor. Later search explores variants of that explanation rather than genuinely different mechanisms.

**Failure signature:** many polished alternatives, but all share the same causal engine.

### T2. Evidence-source dependence and authority substitution

Several claims appear independent because they are repeated by different people, documents, agents, or summaries, while in reality they descend from one upstream observation or source.

The same threat also appears when the prestige, official status, publication venue, or social reputation of a source is substituted for inspection of the claim's actual evidence chain.

**Failure signature:** confidence rises with repetition or authority even though the underlying inspectable evidence has not become stronger.

### T3. Hidden context leakage

A supposedly blind worker receives prior rankings, conclusions, sibling outputs, project memory, parent-chat summaries, or persisted worker history through an ambient context channel.

**Failure signature:** independent stages converge suspiciously early because they are not actually independent in information.

### T4. Causal non-identification

A story explains the observations but competing causal stories predict the same observations. Coherence is silently treated as causality.

**Failure signature:** a model sounds complete yet no obtainable fact distinguishes it from its nearest rival.

### T5. Proxy or objective substitution

The analysis quietly solves an easier neighboring problem: most familiar candidate instead of best-supported candidate, highest score instead of best decision, local symptom instead of system cause.

**Failure signature:** the output is internally optimized but no longer answers the original decision question.

### T6. Candidate-selection and survivorship bias

The available candidate pool is itself selected by archives, logging, visibility, institutional attention, current architecture, prior search, or convenience.

**Failure signature:** the analysis treats "best among visible candidates" as "best explanation overall."

### T7. Duplicate-family pseudo-corroboration

Several formulations of one causal mechanism survive screening and create the impression of broad support.

**Failure signature:** family size influences confidence even though the models are near-duplicates.

### T8. Evaluation-induced anchoring

Early scoring, danger flags, ranking, authorship, or coordinator preference changes how later reviewers group or interpret candidates.

**Failure signature:** the map of the causal space reproduces the screener's preferences instead of representing the space independently.

### T9. Model-to-action conflation

The most plausible model is treated as the action recommendation without accounting for asymmetric loss, reversibility, regret, lock-in, option value, or safety.

**Failure signature:** a slightly favored explanation drives a high-cost irreversible commitment even though a more robust action exists.

### T10. Untestable convergence

The process finishes with a confident explanation but cannot state what evidence would change the conclusion.

**Failure signature:** additional evidence can always be assimilated post hoc; no stopping or reversal condition exists.

### T11. Over-processing and ritualized multi-agent cost

Adding more workers, critics, scores, or rounds can create cost and apparent rigor without increasing causal coverage or decision quality.

**Failure signature:** process complexity grows independently of unresolved uncertainty.

### T12. Runtime integrity failure

Worker launch failure, lost binding, stale context, partial completion, or recovery logic can break blindness while leaving the orchestration superficially intact.

**Failure signature:** missing blind work is silently reconstructed in the coordinator context or a contaminated worker is reused.

---

## 5. Core design invariants

The protocol is built around ten invariants.

### I1. Evidence provenance precedes model generation

Facts, reports, inferences, assumptions, constraints, and open questions are separated before causal search.

This controls T2, T4, T5, and T6 by making the evidential substrate inspectable before interpretations multiply.

### I2. Search branches differ by causal mandate, not personality

Workers are separated by system boundary, mechanism, intervention point, dynamics, evidence pattern, or counterfactual boundary.

This controls T1 because different wording or personas are not sufficient if all branches search the same causal region.

### I3. Full Mode blindness is an input-boundary property

A fresh window or worker is not enough. The effective decision-relevant context must match an explicit allowlist.

This directly controls T3.

### I4. Candidate count never increases evidential weight

Duplicate or near-duplicate models may improve representation, but they do not count as independent support.

This controls T2 and T7.

### I5. Representation and evaluation are separated

The causal mapper is blind to screening results; the screener is not allowed to determine the family structure.

This controls T8.

### I6. Causal completeness and causal identification are separate

A model may contain a complete mechanism and still be poorly identified against alternatives.

This controls T4.

### I7. Belief and action are separate outputs

Model judgment and decision judgment are computed separately.

This controls T9.

### I8. Convergence requires a stopping condition

A recommendation is not complete unless residual uncertainty is bounded and the analysis can name the evidence or condition that would change the action.

This controls T10.

### I9. Rigor is adaptive

Additional workers or critics are triggered by uncovered uncertainty, not by a fixed ceremony.

This controls T11 while preserving the ability to escalate when coverage is inadequate.

### I10. Source authority never substitutes for claim-level provenance

Official, peer-reviewed, institutional, expert, fringe, or anonymous status affects search strategy and verification burden, but does not itself determine whether a material claim is true.

Material claims are traced toward inspectable evidence, common evidence ancestry is recorded where decision-relevant, and low-verifiability sources may generate leads without receiving automatic evidential weight.

This controls T2 and also reduces T4 and T6 by preventing reputation or repetition from hiding weak identification or selected evidence.

---

## 6. Why the architecture has five phases

The five-phase structure follows the order in which the threats must be controlled:

    evidence ambiguity
        ↓
    Phase A: establish facts, decision, scope, loss, framing
        ↓
    search-space risk
        ↓
    Phase B: generate causally distinct models under isolation
        ↓
    evaluation / representation contamination risk
        ↓
    Phase C: screen and map separately, then build a slate
        ↓
    fragility / shared-bias risk
        ↓
    Phase D: dossier, stress, collide, audit
        ↓
    decision / overconfidence risk
        ↓
    Phase E: separate belief from action and apply sufficiency gate

The ordering matters. Generating models before defining the decision contract increases T5; ranking models before mapping their causal relations increases T8; choosing an action before stress-testing load-bearing assumptions increases T9.

---

## 7. Phase A: why evidence and decision are established before search

### 7.1 Evidence provenance

The evidence brief is a controlled shared substrate. It separates directly inspected facts, reported claims, strong inference, assumptions, constraints, and open questions.

Without this step, workers can inherit different implicit fact sets, and later disagreement becomes impossible to diagnose: did the models differ, or did the evidence differ?

The brief also prevents a prior recommendation, TODO, or architecture from being treated as factual proof of the current framing.

### 7.1.1 Why source quality is evaluated at claim level

Whole-source trust labels are too coarse for adversarial or contested domains. A prestigious source can make a claim based on inaccessible or weak evidence; a low-reputation source can point to a genuine primary document.

Convergence Guard therefore separates:

- who or what made the claim;
- what evidence is actually inspectable;
- whether several sources share one upstream observation;
- whether the source is evidence, corroboration, context, a lead, or unsupported.

The aim is not to make all sources equal. It is to make their **epistemic role explicit**.

This prevents two opposite errors:

1. **authority substitution** — treating official or peer-reviewed status as a truth guarantee;
2. **source dismissal** — rejecting a potentially valid observation merely because it was surfaced by a low-prestige or partisan source.

The nearest available primary evidence is preferred for factual grounding, while secondary or fringe material can remain useful for discovery. When underlying evidence is inaccessible, only the existence and content of the public assessment are directly confirmable.

This does not make "primary" synonymous with "best overall inference." For cumulative scientific questions, a transparent synthesis can be more informative than a single primary study. Nor do conflicts, funding, ideology, or inaccessible data automatically falsify a claim; they identify limitations or bias channels that must be investigated rather than used as verdict shortcuts.

The shared evidence brief also prevents evidence acquisition from becoming a hidden branch advantage. A blind worker may discover a useful lead, but material new evidence is promoted through a shared checkpoint before it changes the decision. Otherwise branch disagreement could reflect different private fact sets rather than different causal explanations.

### 7.2 Decision contract

The decision contract exists because causal analysis can succeed while the decision still fails.

It fixes:

- the actual decision question;
- what may be reframed;
- observable success criteria;
- forbidden substitutions;
- cost of error;
- reversibility.

This makes proxy drift detectable and provides the later adjudicator with a stable basis for comparing actions.

### 7.3 Framing check and outside view

The framing check exists to detect a missing system boundary, inherited proxy, or upstream formulation error before search becomes expensive.

When a meaningful reference class exists, outside-view or base-rate evidence is added as a calibration input. The reference-class component is conditional because forcing one where none is defensible would create another proxy error.

### 7.4 Why the independent reframe review is optional

A separate reframe reviewer is useful when the original wording itself may be the anchor: for example, when the question embeds a causal assumption, solution choice, or expensive system boundary.

This primarily controls T1 and T5. The reviewer receives the evidence brief, original question, and decision contract, but not later candidate models or coordinator conclusions.

It is conditional because reframing every case would create T11: unnecessary process and artificial alternative formulations where the original frame is already adequate.

### 7.5 Why retrospective causal reconstruction is optional

When the outcome has already happened, temporal ordering and hindsight can make a polished explanation look inevitable. Retrospective causal reconstruction works backward from the observed outcome to competing causal chains and the earliest known deviation.

This controls T4 by making missing links and temporal assumptions explicit, and T6 by exposing when the surviving trace is itself selected.

It expands the candidate space; it is never treated as proof of cause. It is optional because prospective decisions or cases without useful observable traces do not benefit from the reconstruction.

---

## 8. Phase B: why search begins with three isolated mandates

### 8.1 Why mandates, not personas

A persona can change tone while leaving the causal mechanism unchanged. A search mandate must differ along decision-relevant dimensions.

The design target is **causal coverage**, not stylistic diversity.

### 8.2 Why three initially

Three is a cost/coverage default, not a claim that every problem has three true explanations.

One branch cannot reveal whether its own framing is narrow.

Two branches can create a false binary.

Three is the protocol's default minimum search cohort. It is intended to make it practical to:

- escape a single anchor;
- detect false dichotomies;
- compare whether search regions are actually distinct;
- run a meaningful coverage gate.

The number is therefore operational, not epistemic.

### 8.3 Why expansion is conditional

The initial cohort expands only when the coverage gate detects an uncovered region, excessive overlap, too few surviving causal families, or framing/outside-view evidence exposes a plausible missing family.

This prevents T11: more workers are not treated as more rigor by default.

The cap of five bounds search fan-out so Phase B cannot become an open-ended substitute for evidence or adjudication. Allowing up to two expansion mandates gives the protocol room to target uncovered regions while keeping search cost finite. The exact cap is an operational parameter rather than an epistemic constant and remains an evaluation target.

### 8.4 Why search workers share the same factual brief

Different evidence sets would make outputs difficult to compare and could manufacture disagreement.

Isolation removes prior conclusions, not relevant facts.

### 8.5 Why search workers return predictions and disconfirmers

This forces each candidate to expose how it can be distinguished from nearby alternatives and prevents a merely narrative model from becoming privileged by eloquence.

---

## 9. Context isolation as an architectural control

Full Mode depends on information barriers only where blindness has decision value.

The key distinction is:

    worker separation ≠ context isolation ≠ evidential independence

- **Worker separation** means two conversations are technically distinct.
- **Context isolation** means forbidden prior conclusions cannot enter the role's effective input.
- **Evidential independence** is a property of real-world evidence sources and cannot be created by orchestration.

The protocol can create the first two. It can only audit, not manufacture, the third.

This is why the context allowlist explicitly excludes parent conclusions, sibling outputs, prior rankings, memory, project summaries, persisted worker history, and coordinator preferences when a role is meant to be blind.

### Residual risk

No prompt can guarantee isolation if the host injects hidden decision-relevant context. Therefore Full Mode is unavailable when the runtime boundary cannot be established with reasonable confidence.

That limitation is a design property, not an implementation inconvenience.

---

## 10. Phase C: why reduction is split into screening and blind mapping

Reduction creates a new danger: once candidates are evaluated, evaluation can distort representation.

The protocol therefore splits two questions:

1. **How well does this candidate fit the evidence and decision contract?**
2. **What causal family does this candidate belong to, and how does it relate to others?**

The screener answers the first. The mapper answers the second.

They run in parallel fresh contexts so neither answer can anchor the other.

### 10.1 Why there is no aggregate score

A single score would mix dimensions with different meanings:

- evidence support;
- causal identification;
- discriminability;
- contract fit;
- decision exposure;
- reversibility.

An aggregate number would require weights that are often unsupported and would hide veto-like failures such as a hard factual contradiction.

The design therefore keeps a vector of judgments rather than manufacturing a scalar ranking.

### 10.2 Why causal relations are explicit

Real problems are not always tournaments.

Models may be EXCLUSIVE, COEXISTING, NESTED, or INTERACTING.

This prevents false dichotomies and allows the final model judgment to be a combination when the evidence supports interacting or coexisting causes.

### 10.3 Why neutral IDs exist

Neutralization reduces authorship and branch-origin cues during screening and mapping.

It also improves traceability: later refinements can be checked against the original candidate rather than silently replacing it.

### 10.4 Why the boundary critic is conditional

Family boundaries matter only when a merge or relation can change the decision.

Running a critic for every classification would increase cost without necessarily increasing decision quality.

### 10.5 Why evidence checkpoints can interrupt the pipeline

The protocol is not allowed to keep reprocessing a frozen evidence set when later analysis reveals that one obtainable evidence class could materially change the slate or action.

An evidence checkpoint is triggered when mapping, a dossier, assumption sensitivity, shared-bias audit, or pairwise collision exposes a decisive missing observation, a new causal family, or a direct contradiction with available primary evidence.

This controls T4 by preventing narrative refinement from substituting for causal identification, T6 by exposing missing or selected evidence boundaries, and T10 by preventing convergence when a practical discriminator is still available.

After new evidence arrives, only affected screening, mapping, slate, dossier, or adjudication artifacts are rerun. Unaffected frozen artifacts are preserved because a full restart would add cost, destroy useful traceability, and expose previously blind stages to later conclusions without decision value.

These returns share a finite run budget set before search, including a default cap of two corrective cycles unless the contract justifies another limit. A completed cycle without material progress or any exhausted limit ends corrective work; it does not waive the evidence-sufficiency gate. See [operational stopping rules](convergence-guard/references/protocol-details.md#131-run-budget-and-stopping).

---

## 11. Why the finalist slate normally contains two or three models — and may contain one or none

The slate is a decision-working set, not a podium.

It contains only viable, causally distinct, decision-relevant models.

One model is legitimate when screening/mapping leave a single genuine survivor **after** checking whether missing evidence or search coverage caused the collapse. The protocol keeps that survivor rather than inventing a rival, but still subjects it to dossier work, assumption sensitivity, and the shared-bias audit. A lone survivor is not automatically confirmed.

Zero finalists is also a legitimate state when no candidate remains supportable and no useful budgeted checkpoint can repair the gap. The protocol then carries explicit insufficiency for causal attribution into Phase E instead of promoting a rejected model. A separate robust action may still be justified only if it independently passes the action-sufficiency gate.

Two are sufficient when two families capture the live decision conflict.

Three are useful when a third mechanism changes the action or protects against a missing outside alternative.

The slate is never padded because a weak third candidate would add ceremony, not information.

An information probe is kept separate from the slate because **high value to test** is not the same property as **high current plausibility**.

### 11.1 Why the slate has an upper bound of three

The slate is a compression layer between broad search and expensive adjudication. Its purpose is to preserve the few causal models that can still change the decision, not to retain every plausible explanation.

With one finalist there are zero pairwise collisions; with two there is one; with three there are three. Four finalists would already require six pairwise relations and substantially increase dossier/adjudication cost.

The upper bound of three is therefore an operational compression rule: if many strong families remain, the preferred response is better screening, boundary work, or targeted evidence rather than turning adjudication back into broad search. It is not a claim that four-way causal systems cannot exist, and its calibration remains an evaluation target.

### 11.2 Why there is at most one information probe

The information probe is meant to focus the next evidence budget on the single uncertainty with the highest practical decision value.

Keeping at most one prevents the probe mechanism from becoming a second finalist slate or a generic research backlog. When several missing observations appear similarly important, the coordinator should compare their decision value, cost, and ability to collapse multiple uncertainties rather than automatically launching all of them.

When the chosen probe needs more operational detail, a compact probe mini-dossier may specify the target uncertainty, source IDs, contrasting predictions, decision-changing outcomes, feasibility/cost, and confounders. It remains a planning artifact for learning, not a finalist, extra vote, or independent validation, and stays outside isolated finalist dossier inputs.

The one-probe bound is an operational focus rule, not an epistemic claim, and should be tested in evaluation.

---

## 12. Phase D: why finalists get independent dossiers

A candidate that survives reduction is still often underspecified.

The dossier makes one model explicit:

- mechanism;
- load-bearing assumptions;
- predictions;
- disconfirming observations;
- decision consequence;
- identification weaknesses;
- error cost and reversibility.

Each dossier worker sees one finalist only because its task is model clarification, not rhetorical competition.

This reduces the risk that a worker unconsciously repairs its model merely to defeat a visible rival.

### 12.1 Why model repair creates a new hypothesis ID

If a dossier fixes a missing causal link by adding a new load-bearing premise, it has changed the model.

Allowing the repaired version to inherit the original candidate's screening status would launder an untested hypothesis into the final slate.

The new-ID rule preserves traceability.

A materially revised hypothesis remains `PENDING` until every affected reduction and adjudication check is rerun against the current evidence and contract. This prevents budget exhaustion or an interrupted corrective return from laundering the old candidate's validation onto a changed mechanism.

### 12.2 Why premortem is optional

A premortem is valuable when the contemplated action is expensive, risky, strategically important, or hard to reverse. It forces the analysis to describe a plausible failure sequence, early warning signal, and recovery path rather than merely listing generic risks.

This primarily controls T9 by exposing action fragility that may not change the leading causal model but can change the rational decision.

It is conditional because running a premortem for cheap, reversible actions would create T11 without meaningful decision benefit.

### 12.3 Why the stakeholder lens is optional

Some outcomes depend materially on distinct actors with different constraints, incentives, authority, or information. In those cases a stakeholder lens can reveal a missing system boundary, proxy objective, or coordination mechanism.

This primarily controls T5 and T6 and can affect T9 when the feasibility or cost of an action differs by stakeholder.

The lens is used only when stakeholders materially affect the outcome. Statements about them retain evidence provenance so the analysis does not invent preferences or motives merely to fill missing information.

---

## 13. Why adjudication is slate-level and fresh

The adjudicator is fresh because it must evaluate the final decision structure rather than defend work it authored earlier.

It performs three complementary tests.

### 13.1 Assumption sensitivity

Some models appear strong only because one uncertain premise carries most of the causal load.

Testing assumptions by **uncertainty × causal leverage × decision sensitivity** exposes this fragility.

The output is not a probability. ROBUST, CONDITIONAL, and BROKEN describe response to a plausible mutation.

### 13.2 Shared-bias audit

Independent dossiers can still share:

- one hidden premise;
- one missing evidence class;
- one selected population;
- one proxy objective;
- one upstream data source;
- one causal-identification weakness.

The shared-bias audit exists because independence of reasoning does not imply diversity of blind spots.

### 13.3 Pairwise decision collision

The protocol compares finalist pairs only where their implications for action conflict.

This reveals:

- what observation separates the actions;
- which fact could flip the preference;
- whether current evidence actually supports a choice.

If the models can coexist, they are not forced into a false duel.

---

## 14. Why second opinion is conditional

A second opinion has value when the first adjudication is structurally fragile:

- cycles;
- repeated UNDETERMINED results;
- weak evidence for an apparent winner;
- hard-to-reverse action;
- serious shared blind spot;
- unexplained conflict with earlier stages.

Running it automatically would create T11 and risk turning repeated reasoning into pseudo-corroboration.

The second-opinion reviewer therefore reconstructs the decisive inference from raw evidence provenance and neutral claims rather than merely rereading the polished winner.

---

## 15. Phase E: why model judgment and decision judgment are separate

Suppose model A is somewhat better supported than model B.

That does not imply that the action optimized for A is rational if:

- being wrong under B is catastrophic;
- the A-specific action is irreversible;
- a common action works well under both;
- waiting cheaply resolves the uncertainty;
- an action can both help and generate information.

The architecture therefore produces two outputs.

### Model judgment

What causal model or combination is best supported?

### Decision judgment

What action is best across the surviving plausible model set under the decision contract?

This separation is one of the main defenses against confident but brittle decisions.

---

## 16. Why the evidence-sufficiency gate is explicit

Many reasoning systems have an implicit pressure to return one answer.

Convergence Guard treats **refusal to over-select** as a valid terminal state.

A best action is selected only when:

- no hard contradiction invalidates it;
- it remains preferable across plausible surviving models;
- no pending check could plausibly reverse the action, is obtainable before commitment, and is worth its cost and delay under the decision contract; perform such a check first, then reassess;
- uncertainty is explicit and bounded;
- downside and reversibility are understood for the stakes.

Otherwise the correct output is INSUFFICIENT DATA TO CHOOSE.

This is not a failure to reason. It is a positive calibration result.

---

## 17. Why every run ends with a decision-changing next step

"Need more information" is not actionable, but even a run that selects an action benefits from stating what observation could change the next decision.

The protocol therefore asks for the cheapest practical observation, audit, comparison, or experiment that can change the decision when such a step is available and relevant.

A good terminal probe specifies:

- what to observe;
- what rival models predict;
- what threshold or pattern matters;
- confounders and guardrails;
- stopping rule where relevant;
- action under each material outcome.

This converts uncertainty from a static disclaimer into a learning plan.

---

## 18. Reduced Mode and graceful degradation

The strongest guarantees of Convergence Guard depend on context isolation.

When the host cannot provide that boundary, sequential passes may still improve structure but cannot honestly reproduce blind search, blind mapping, independent dossiers, or independent second opinion.

Reduced Mode exists so the method can degrade **explicitly rather than deceptively**.

Its purpose is not to simulate Full Mode cheaply. Its purpose is to preserve useful reasoning structure while clearly marking which anti-anchoring guarantees are unavailable.

---

## 19. Runtime failure and recovery

Long multi-stage runs fail in practice.

A runtime may:

- fail to launch a worker;
- lose binding;
- partially complete a phase;
- preserve some finished workers but not others;
- make a previously fresh worker no longer fresh.

The recovery rule is:

> preserve valid frozen artifacts, identify the smallest missing operation, and rerun only that operation under the original information boundary.

Do not:

- restart the entire protocol automatically;
- replace a failed blind stage with coordinator reasoning;
- reuse a contaminated worker for a role requiring freshness;
- inject completed sibling outputs into a replacement worker.

This controls T12 and also avoids turning failure recovery into a new source of anchoring.

---

## 20. Why Full Mode rigor is not measured by worker count

The number of workers is an implementation cost, not an epistemic score.

More workers can improve search only if they cover a missing causal region or perform a role that requires fresh blindness.

Otherwise they add:

- correlated reasoning;
- repeated evidence;
- latency and cost;
- more opportunities for context leakage;
- a misleading sense of consensus.

The protocol therefore uses conditional expansion, conditional boundary review, and conditional second opinion.

Rigor is measured by preservation of the relevant information barriers and decision checks.

---

## 21. Threat-to-control traceability

| Threat | Primary controls | Residual risk |
|---|---|---|
| T1 Premature convergence | decision contract; three causally distinct mandates; coverage gate | all mandates can still share a hidden framing |
| T2 Evidence-source dependence / authority substitution | provenance labels; claim-level source roles; source-ancestry tracing; shared-bias audit; no worker-vote logic | upstream ancestry, hidden evidence, or selective disclosure may remain unknown |
| T3 Hidden context leakage | explicit allowlists; fresh contexts; boundary verification; runtime-specific preflight where defined; Reduced Mode boundary | host-side hidden injection may be unobservable |
| T4 Causal non-identification | predictions; disconfirmers; identification labels; pairwise collision | some domains remain observationally underdetermined |
| T5 Proxy substitution | decision contract; forbidden substitutions; success criterion | the original objective itself may be poorly specified |
| T6 Selection/survivorship bias | outside alternatives; outside view; population-boundary audit | unseen candidate space cannot be enumerated completely |
| T7 Duplicate pseudo-corroboration | causal mapping; family-level normalization; no duplicate-count support | subtle duplicates may remain unrecognized |
| T8 Evaluation anchoring | parallel blind screening and mapping; neutral IDs | candidate wording can still carry implicit prestige cues |
| T9 Model/action conflation | separate model and decision judgments; loss/reversibility analysis | action utilities may remain qualitative |
| T10 Untestable convergence | sufficiency gate; minimum discriminating observation | decisive evidence may be unobtainable |
| T11 Ritualized cost | adaptive expansion; conditional critics and second opinion | coordinators may still over-trigger optional stages |
| T12 Runtime failure | frozen artifacts; minimal recovery; no sequential substitution | runtime may make boundary status inconclusive |

---

## 22. Why several tempting alternatives are rejected

### Majority vote

Rejected because workers share training, framing, and often evidence. Vote count is not real-world corroboration.

### Source-prestige ranking

Rejected because `official`, `peer reviewed`, `expert`, or `primary` describe provenance or process rather than guaranteeing a proposition. Prestige can prioritize verification effort but cannot replace claim-level inspection.

The opposite rule — automatically discarding fringe, partisan, anonymous, or advocacy sources — is also rejected. Such sources may surface a valid lead, but the underlying material must carry the evidential weight.

### One global score

Rejected because it hides distinct dimensions, requires unsupported weights, and can let strength on one dimension compensate for a hard failure on another.

### Fixed number of search workers

Rejected because search cost should respond to uncovered causal space, not ceremony.

### Fixed top-three tournament

Rejected because two models may be enough, a third may be weak, or multiple models may coexist.

### Automatic devil's advocate

Rejected as a default because forced opposition can create performative disagreement without adding a distinct causal mechanism.

### Automatic second opinion

Rejected because repetition over the same evidence can be mistaken for corroboration and adds cost without a trigger.

### Sequential personas reported as independent agents

Rejected because the same context retains the anchor and therefore cannot supply the required blindness.

### "Always decide"

Rejected because calibrated insufficiency can dominate an unsupported choice, especially when commitment is costly or reversible evidence collection remains available.

---

## 23. Design assumptions

Convergence Guard itself rests on assumptions that evaluation must test.

### A1. Causal diversity is useful

For the target problem class, materially different causal models should improve robustness relative to repeated refinement of one model.

### A2. Information barriers reduce anchoring

Blindness to prior preferences should change some judgments in cases where early anchoring is otherwise influential.

### A3. Structured causal outputs improve discriminability

Requiring mechanisms, predictions, and disconfirmers should make it easier to identify narrative-only explanations.

### A4. Model/action separation improves decisions under asymmetric loss

Explicit reversibility and regret should sometimes change the recommended action even when the leading causal model does not change.

### A5. An explicit insufficiency option improves calibration

Allowing INSUFFICIENT DATA TO CHOOSE should reduce unsupported certainty without producing excessive refusal to decide.

### A6. Adaptive rigor can preserve quality at lower cost

Coverage gates and conditional critics should achieve comparable or better decision quality than fixed maximal orchestration on cases that do not need every stage.

These are empirical claims, not axioms. The planned evaluation suite should test them directly.

---

## 24. Evaluation implications

The architecture should ultimately be judged against observable outcomes, not elegance.

A useful evaluation program should compare Convergence Guard with simpler baselines on:

- recovery of causally distinct alternatives;
- rate of unsupported singular conclusions;
- detection of dependent evidence;
- detection of hidden assumptions;
- robustness under assumption mutation;
- calibration of INSUFFICIENT DATA TO CHOOSE;
- quality of decision-changing experiments or observations;
- action quality under asymmetric loss and reversibility;
- resistance to injected anchors;
- sensitivity to context leakage;
- cost in model calls, latency, and tokens;
- reproducibility of the audit trail.

The protocol should not be considered successful merely because it produces longer reports or more disagreement.

---

## 25. Open design questions

The current architecture is intentionally explicit about which parts are principled controls and which parts remain qualitative operating thresholds.

The following questions should be treated as evaluation targets rather than silently frozen constants:

### Q1. Search-budget calibration

Three initial search mandates and an adaptive cap of five are currently operational defaults. The rationale for three is to escape a false binary at bounded cost, but the evaluation suite should test whether different domains need different budgets and what to do when coverage remains inadequate after five.

### Q2. Positive definition of sufficient coverage

The current coverage gate is better at detecting obvious insufficiency than proving completeness. A stronger future version may need domain-independent indicators for when the causal space is sufficiently covered for the decision at hand.

### Q3. Qualitative screening thresholds

Labels such as STRONG, MIXED, WEAK, HIGH, MEDIUM, LOW, SUPPORTED, THREATENED, and UNIDENTIFIED are intentionally non-numeric. Their calibration and inter-rater stability need empirical measurement.

### Q4. Family-level support normalization

The protocol says duplicate-family count must not increase support. It does not yet define a quantitative family-normalization operation, and it should not accidentally recreate a hidden aggregate score.

### Q5. Assumption-selection stopping rules

The uncertainty × causal leverage × decision sensitivity heuristic identifies load-bearing assumptions, but ties, stopping rules, and interaction effects remain qualitative.

### Q6. Stakes-based escalation

Reversibility and error cost influence screening, premortem, second opinion, and the sufficiency gate, but the protocol does not yet define a universal threshold at which a stage becomes mandatory.

### Q7. No-discriminator terminal state

Some problems may have no ethical, practical, or obtainable observation capable of separating the live models. The operational terminal state is now `NO FEASIBLE DISCRIMINATOR IDENTIFIED`, with the search limits stated. Model judgment may remain unresolved while a robust low-regret action passes the sufficiency gate; otherwise the decision remains `INSUFFICIENT DATA TO CHOOSE`. A known but deferred check is not this state. Evaluation should test whether this exit prevents invented tests without prematurely abandoning useful evidence search.

### Q8. Artifact validity after interruption or new evidence

Recovery preserves frozen artifacts, but a future implementation may benefit from explicit artifact epochs or dependency metadata that state exactly which earlier outputs become invalid when evidence changes.

### Q9. Slate and information-probe bounds

The normal two-to-three finalist range, the one-survivor exception, the zero-finalist insufficiency exit, the upper bound of three, and the one-probe cap are operational compression rules. Evaluation should test whether they preserve decision quality across domains, when a fourth finalist should trigger additional reduction versus explicit retention, and whether multiple coordinated probes ever outperform one focused highest-value probe.

These are not hidden exceptions to the method. They are part of the research agenda for the evaluation suite.

---

## 26. Versioning and authority

This document explains the design rationale for the current v0.2.2 architecture.

Authority is ordered as follows:

1. [convergence-guard/SKILL.md](convergence-guard/SKILL.md) — canonical executable protocol;
2. [protocol-details.md](convergence-guard/references/protocol-details.md) — detailed operational rules;
3. DESIGN.md — architectural rationale and threat model;
4. explanatory guides and runtime profiles — human guidance and environment-specific integration.

If this document and the canonical skill ever disagree on an operational rule, the skill wins and the design document must be updated.

---

## 27. Summary

Convergence Guard is built around one principle:

> **Convergence should be earned by discriminating evidence and decision robustness, not produced by repetition, ranking pressure, or orchestration ceremony.**

The architecture follows from that principle:

    ground the evidence
    → define the decision and cost of error
    → search distinct causal regions under isolation
    → reduce without leaking evaluation into representation
    → stress load-bearing assumptions and shared blind spots
    → separate causal belief from action
    → choose only when evidence is sufficient, otherwise state insufficiency
    → identify the cheapest practical observation that can change the next decision

That is the design contract Convergence Guard is intended to preserve as the implementation evolves.
