# Convergence Guard — Research Roadmap and Pause Criteria

[Русская версия](ROADMAP.ru.md)

**Status: research preview preserved; active feature development paused (2026-10-08).** This is a conditional evidence plan, **not** a promise of future experiments, a release schedule, or a claim of validated performance. The repository remains available for inspection. There is no planned public promotional campaign.

## The question that must be answered first

**Does Convergence Guard provide a meaningful, repeatable advantage over a well-designed, cheaper analysis workflow on tasks where its extra structure should matter?**

Producing longer analyses, more candidate explanations, a more elaborate audit trail, or better-looking normalized outputs is **not**, by itself, proof of better causal reasoning. If an equally effective simpler approach exists, it should be preferred. Until additional evidence exists, CG should be treated as an **experimental protocol**, not a validated accuracy-improving product.

## Evidence at the pause point

| Observation | Defensible reading | Boundary |
|---|---|---|
| [Main benchmark `main-v0.1.7`](evals/results/main-v0.1.7/INTERPRETATION.md): 8 authored cases × 4 implemented modes × 1 repeat = 32 primary runs and 32 calibrations | On **normalized** answers, implemented Full and shared-context multi-agent each had 0/8 premature winners; Full had stronger mean action scores than shared (1.875 vs 1.625 out of 2) | The tested Full/Reduced workflows did **not** implement all canonical stages; one model, one repeat; not a population-level or canonical-Full result |
| Resource use in that benchmark | Implemented Full averaged 9.125 model calls/case; shared-context averaged 4.375; single-context, 1 | No demonstrated cost-adjusted general superiority of Full |
| [Raw/normalized diagnostic](evals/results/main-v0.1.7/diagnostics/REJUDGE-REPORT.md) on M04–M07 | N1 applied in 15/16 runs; for implemented Full, blind judges agreed on **3/4 raw premature winners** versus **0/4 normalized** within this subset | The published normalized metric cannot substitute for raw-behavior evaluation; do not retroactively modify frozen scores |
| [Isolation ablation `v0.1.4`](evals/results/isolation-ablation-v0.1.4/INTERPRETATION.md): 16 cells | The tested context boundary passed a mechanical integrity check | No incremental answer-quality benefit was demonstrated; shared workers had an explicit `NOT EVIDENCE` anti-anchor warning and both judges scored 0/8 false-anchor adoptions |
| [Conformance matrix](evals/protocol/v0.2/CONFORMANCE-MATRIX.md) | A post-benchmark correction layer identifies missing/partial canonical branches and fail-closed behavior | A corrected implementation target is **not** the same as a newly benchmarked, fully conformant protocol |

The [Applicability Evidence Map](convergence-guard/references/applicability-evidence-map.md) records the broader hypotheses and their evidence levels. The existing historical [automation plan](evals/MAIN-AUTOMATION-PLAN.md) and [pilot-era eval specification](evals/protocol/EVAL-SPEC-v0.1.md) describe past designs; they are **not** this roadmap's future commitments.

## Conditional research gates — only if work is resumed

These gates are ordered. A later gate is **not authorized by success at an earlier gate** and should not begin automatically. No new benchmark results are reported by this document.

### Gate 0 — Define the practical value proposition before implementation

- Identify a narrow, falsifiable failure class where an extra stage is expected to change **a correct causal judgment or justified action**, not simply its presentation.
- Predeclare the task population, ground-truth or admissible uncertainty standard, error costs, and what magnitude of quality gain would justify incremental tokens, time and engineering complexity.
- Record a null outcome as legitimate: "a simpler workflow is sufficient" or "the proposed mechanism has no measurable incremental benefit."
- Exclude demonstrations whose answer is a trivial single-step provenance observation; include cases requiring multi-step causal discrimination, interacting or coexisting causes, or action choice under unequal losses.

**Gate 0 exit:** a reviewable, versioned hypothesis and minimum worthwhile effect/cost threshold **before** seeing new outcomes. Otherwise **stop**.

### Gate 1 — Strong, fair comparisons and trustworthy measurement

- Compare, with the **same model, frozen evidence and outcome contract**, at least: (a) a strong single-context prompt explicitly requiring competing explanations, source checks, uncertainty and decision-changing tests; (b) a simpler structured multi-pass/shared-context workflow; and (c) CG only after a **conformance check** of the exact executed protocol. A compact structured core is an optional candidate, **not** an already tested product.
- Report both **equal-call/token-budget** comparisons and **unrestricted actual-cost** comparisons. Record model, version, settings, seeds, calls, input/output tokens, latency, retries, and failures; do not compare an elaborate workflow only with a weak single-shot question.
- Register new cases and scoring rules before execution. Freeze participant-visible evidence independently of private keys; include resolvable, insufficient, coexisting, interacting, and deliberately misleading *nontrivial* cases. Avoid choosing or rewriting cases after seeing workflow outputs. Replicate across runs and at least two genuinely distinct model/runtime settings before claiming transfer.
- Judge **raw model decisions as the primary scientific endpoint**. Treat schema compliance and any normalization as separate metrics; retain raw and normalized artifacts and score their semantic disagreements explicitly. No deletion of a preferred cause may silently turn an incorrect raw choice into a correct one.
- Keep treatment identities blinded during semantic judging, provide transparent rubrics, use multiple judges where feasible, preserve disagreement without silent tie-breaking, and distinguish causal-structure correctness, justified abstention, action quality and next-test quality. Predeclare primary and secondary outcomes; do not create a post-hoc composite winner.
- Record public reproducibility limits accurately: the existing private keys, blind map and individual judgments are not sufficient for public-only rejudging because they are not in the repository. Independent replication requires a new independently frozen evaluation or an appropriately released judging package.

**Gate 1 exit:** a reproducible, methodologically reviewable comparison showing a decision-relevant incremental effect **against the strongest appropriate simpler baseline**, with uncertainty and resource cost reported. A nominal lead on a few authored examples is **not enough**. If no meaningful repeatable advantage is found, **stop claims of performance superiority** and do not escalate to a bigger architecture.

### Gate 2 — Prove which complexity is necessary

Only after Gate 1 demonstrates a worthwhile signal:

- Remove or toggle **one control at a time** while holding the remaining work, budget, evidence and evaluation constant: parallel search, blind separation, provenance handling, adversarial review, assumption testing, and evidence-sufficiency/action separation. Avoid interpreting a package-level win as proof of each component.
- Run a matched isolation test that does **not** accidentally confound the treatment with unequal anti-anchoring instructions; predeclare the contamination intervention, boundary checks and primary quality metric. Mechanical isolation alone is not a quality win.
- Measure the quality-versus-cost frontier and whether a smaller protocol attains the same result. Keep mandatory checks for genuine audit or security needs distinct from unproven accuracy improvements.

**Gate 2 exit:** retain a component for accuracy claims only when it adds a measured, repeatable, decision-relevant benefit at an acceptable cost; otherwise simplify or remove it from that claim. No automatic Full-Mode preference.

### Gate 3 — Reassess continuation, not promotion by default

Choose one outcome based on evidence, not investment already made:

| Decision | Criteria | Consequence |
|---|---|---|
| **Continue narrowly** | Reliable incremental benefit appears on a defined problem class, relative to strong cheaper baselines, with defensible cost and failure analysis | Develop only the validated scope, cite the exact experiments |
| **Simplify** | A compact/simple workflow matches the quality at meaningfully lower cost | Prefer the simpler implementation; update claims and documentation |
| **Keep as research archive** | Benefits remain unreplicated, inconclusive, or mostly procedural | Preserve the protocol, tests, results, caveats, and negative findings; do not advertise proven accuracy improvements |
| **Stop active development** | No meaningful decision-quality advantage or unacceptable complexity/cost after fair comparisons | No new features or release cadence justified by sunk effort |

## Current disposition

**Active development is paused at the research-preview stage. No further work is scheduled or implied by this document.** The evidence so far is insufficient to justify presenting CG as a proven superior approach to causal reasoning. The existing published artifacts are retained, and past study metrics remain frozen.

This roadmap is **documentation only**. It does not launch any new tests, change the canonical skill or modify study results. Future work would require a separate explicit decision, with its hypothesis, budget, baseline and stopping condition fixed in advance. Public outreach is not a milestone or prerequisite.
