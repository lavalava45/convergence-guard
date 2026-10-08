# Convergence Guard Reduced v0.2 — self-contained participant packet

This packet is intentionally self-contained. The participant must not be asked to follow rules that are available only through an external file, link, memory, retrieval system, or hidden parent context.

## Boundary

Reduced Mode uses one effective context. It does **not** provide independent search workers, blind screening/mapping, independent dossier authorship, or independent second-opinion reconstruction. Never treat agreement between sequential passes as independent corroboration.

## Evidence and provenance

Use only supplied case material. For every material factual claim distinguish:

- `CONFIRMED` — directly inspected in the supplied evidence;
- `REPORTED` — stated by a supplied source but not directly verified;
- `INFERRED` — derived from supplied evidence;
- `HYPOTHETICAL` — proposed for testing rather than treated as fact.

Track source identity/ancestry. Multiple reports derived from the same underlying observation do not become independent support merely by being repeated. Do not browse or introduce outside facts.

## Finite run discipline

Treat the analysis as one finite run. Do not silently restart the reasoning after an inconvenient result. At most two corrective cycles are allowed. A corrective cycle is a targeted return caused by missing evidence/family, a material mechanism revision, or a shared-bias finding plus the downstream checks that must be repeated. Stop when the budget is exhausted or when a completed corrective cycle produces no new decision-relevant evidence, viable mechanism, resolved uncertainty, or changed decision implication.

## Workflow

1. **Ground the evidence.** Separate observations from reports, inferences, hypotheses, and constraints. Note evidence ancestry and obvious missing discriminators.
2. **Write the decision contract.** Preserve the supplied decision question, scope, constraints, error cost, reversibility, deadline/default action if supplied, and analysis budget. Do not replace an empirical uncertainty with an unstated value judgment.
3. **Framing check.** Ask whether the problem boundary, proxy objective, or inherited framing is hiding an upstream cause or a materially different formulation.
4. **Freeze at least three different search mandates before generating models.** Mandates must differ in causal boundary/intervention point/evidence pattern, not just persona wording.
5. **Run each mandate as a separate labeled pass.** Do not edit earlier candidate text after later passes. Each candidate needs claim, mechanism, necessary conditions, predictions, implied action, disconfirming evidence, identification threats, and conflicts with confirmed evidence.
6. **Coverage gate.** After the first three passes, ask whether they collapse onto the same causal region, leave a major system boundary unexamined, leave fewer than two decision-relevant families after basic sanity checks, or miss a family exposed by framing/outside-view evidence. If yes and budget allows, add one or two targeted mandates; otherwise record the limitation.
7. **Contract screening without an aggregate score.** For each candidate record contract fit (`PASS/CONDITIONAL/FAIL`), evidence support (`STRONG/MIXED/WEAK`), causal completeness (`CHAIN PRESENT/PARTIAL/ASSERTION ONLY`), causal identification (`SUPPORTED/THREATENED/UNIDENTIFIED` plus the threat), discriminability (`HIGH/MEDIUM/LOW`), and decision exposure (`LOW/MEDIUM/HIGH`). These are qualitative labels: support means directness/independence/consistency of supplied evidence; discriminability means whether a feasible observation can separate the candidate from live rivals; exposure means the practical downside/reversibility of acting while wrong.
8. **Causal map.** Map candidates into families and explicit relations: `EXCLUSIVE`, `COEXISTING`, `NESTED`, or `INTERACTING`. Merge only materially equivalent mechanisms/predictions and preserve all source IDs. Duplicate formulations are not corroboration.
9. **Boundary audit when needed.** If a disputed merge/relation could change the action, explicitly test that boundary before selecting finalists.
10. **Decision-relevant slate.** Normally retain 2–3 causally distinct non-dominated finalists, but never pad. One viable model is allowed. Zero supported models is allowed. Do not reject a causal model merely because its implied intervention is inconvenient or expensive; causal truth and action feasibility are separate questions.
11. **Dossiers.** For each real finalist, preserve its mechanism and state load-bearing assumptions, predictions, disconfirming observations, decision consequence, identification weaknesses, and cost/reversibility of acting while wrong. If refinement materially changes the mechanism or adds a new load-bearing premise, create a **new hypothesis ID**, mark it `PENDING`, and rerun affected screening/mapping/stress checks. A pending revision cannot become the adjudicated winner merely because the budget ended.
12. **Sensitivity and shared-bias audit.** Mutate load-bearing assumptions one at a time and note whether the action is robust, conditional, or broken under each tested mutation. Check common hidden assumptions, missing evidence/families, proxy substitution, population/observation-boundary bias, common data ancestry, outside-view conflict, and shared identification weaknesses.
13. **Pairwise collision only where action implications conflict.** Do not force `COEXISTING`/`INTERACTING` models into a false winner/loser duel. Identify the observation that could flip the action preference; return `UNDETERMINED` when current evidence cannot justify one.
14. **Separate model judgment from action judgment.** A causal structure can be resolved as `COEXISTING` while action choice remains insufficient. Conversely, one low-regret action can be justified across unresolved models without proving which model is true.
15. **Evidence-sufficiency gate for action.** Choose one best action only when no hard factual contradiction invalidates it, it is preferable under the decision contract and surviving models, no worthwhile obtainable pre-commitment check could plausibly reverse it, residual uncertainty is bounded, and downside/reversibility are understood for the stakes. Otherwise defer the commitment rather than invent certainty.
16. **Minimum decision-changing test.** When worthwhile, specify the cheapest practical discriminator, rival predictions, outcome-dependent action rule, key confounders/guardrails, and stopping rule. If none is feasible, state `NO_FEASIBLE_DISCRIMINATOR`; if a known worthwhile check is skipped only because the analysis budget ended, state `DEFERRED_FOR_BUDGET` instead.

## Output integrity

Return the supplied v0.2 structured schema. Causal structure, action decision, next-test status, and protocol completion are separate fields. Zero supported models and no feasible discriminator are valid outcomes. Do not hide a skipped triggered stage by calling the protocol complete.
