# Convergence Guard — Applicability Evidence Map

**Status: descriptive research map, 2026-10-08.** [Русская версия](applicability-evidence-map.ru.md).

This document maps **causal problem structures** to possible uses of Convergence Guard (CG). Its breadth is a map of *where to investigate usefulness*, **not** evidence that CG improves performance across all these domains. The [Applicability Guide](applicability.md) explains the operational activation triage.

## How to read evidence levels

| Label | Meaning | What it does **not** mean |
|---|---|---|
| **CHECKED (local)** | A behavior or outcome was observed in the specified frozen, authored cases or audited artifacts. The exact case ID, comparator and limitations must accompany it. | Replicated real-world advantage, statistical significance, or canonical-Full efficacy. |
| **PROMISING (hypothesis)** | The protocol addresses a plausible failure mechanism, but the proposed transfer or incremental performance benefit has **not** been experimentally demonstrated. | A positive benchmark result. |
| **UNCONFIRMED / NEGATIVE (current test)** | The claimed advantage is unsupported, or a targeted experiment did not detect it under the stated manipulation. | Proof that the control is always useless. |
| **OUT OF SCOPE** | Routine/factual tasks, direct low-risk corrections, or work requiring unavailable independent evidence or domain authorization. | A reason to run a larger protocol merely to appear thorough. |

**Unit of evidence:** 8 **authored, closed-evidence operational cases** × 4 **implemented workflows** × 1 repeat = 32 primary runs with one local `gemma-4-12b-it-Q6_K` model and 32 calibrations. The study was *not* a test of full canonical CG v0.2 conformance. Scores are from predeclared normalized outputs; later raw-vs-normalized blind review of M04–M07 showed N1 fired in **15/16** runs and could change causal interpretation. Two-judge isolation ablation used only four older cases. See [main interpretation](../../evals/results/main-v0.1.7/INTERPRETATION.md), [main per-case summary](../../evals/results/main-v0.1.7/summary.json), [normalization re-audit](../../evals/results/main-v0.1.7/diagnostics/REJUDGE-REPORT.md), [isolation interpretation](../../evals/results/isolation-ablation-v0.1.4/INTERPRETATION.md), and [conformance matrix](../../evals/protocol/v0.2/CONFORMANCE-MATRIX.md).

## A. Observed causal regimes — not domain-wide validations

All rows below are **CHECKED (local)** as benchmark observations. This does **not** assign a positive CG advantage to every row. `Action` is the frozen blind-judge action-quality score (0–2) in the order **implemented Full / shared multi-agent / single-context / implemented Reduced**.

| Case, problem structure | Observed action scores | Signal and applicable limit | Implication for use |
|---|---|---|---|
| **M01 — direct resolvable**, packaging-line fault | **2 / 2 / 2 / 2** | No action-quality benefit for Full; direct inspection resolved the task. | Ordinary analysis first. |
| **M02 — strong distractor but resolvable**, export-job incident | **2 / 2 / 2 / 2** | A distracting contemporaneous change did not prevent any workflow from giving a strong action. | Prefer a cheap disconfirming check before escalation. |
| **M03 — several plausible but separable causes**, molding-quality fault | **2 / 2 / 2 / 2** | All modes found a strong action; declared causal statuses did not all match the key. | Compact structured comparison may suffice; causal status still matters. |
| **M04 — genuine underdetermination**, event-pipeline incident | **2 / 1 / 2 / 1** | Full did not beat single on action; uncertainty handling needs explicit causal/action separation. | Do not force attribution; test whether action can proceed under uncertainty. |
| **M05 — deceptive underdetermination and dependent evidence**, fraud-screening incident | **2 / 2 / 1 / 1** | Full and shared each avoided a premature causal winner; single and Reduced each had `premature_winner=1`. The strongest *workflow* separation, not a Full-specific result. | Promising trigger for multi-pass provenance and alternative checking. |
| **M06 — genuinely coexisting causes**, cold-storage incident | **2 / 1 / 1 / 1** | Full had the stronger action, **but its declared causal status did not match the key**; material normalization caveat applies. | Explicitly represent coexisting mechanisms and evaluate action separately. |
| **M07 — interaction/layered causality**, document-gateway incident | **2 / 2 / 2 / 2** | No action advantage for Full; its declared causal status did not match the key. | Use `INTERACTING`/`NESTED` reasoning without assuming Full is needed. |
| **M08 — bounded mini open-world investigation**, optical-resin case | **1 / 1 / 1 / 1** | No action advantage; a designed mini-investigation is not evidence of real open-world research quality. | Treat as a hypothesis for research use, not validation. |

Across all eight cases, implemented Full and shared each had **0/8 normalized premature winners**, versus **1/8** for single and Reduced. Mean action quality was **1.875/2** for Full and **1.625/2** for shared/single, but Full required **9.125** model calls per case versus **4.375** shared and **1** single. Literal declared-status match was **5/8 Full versus 6/8 single**. These small-sample figures are descriptive and should not be compressed into a single winner score.

## B. Wider application contexts — transfer hypotheses, not measured improvements

An **anchor** means an authored case or worked example illustrates a *structurally related question*. It does **not** validate performance in the listed real-world industry.

| Application context | Why causal structure may fit | Available anchor | Current claim level |
|---|---|---|---|
| Reliability engineering, SRE, operational incident response | Competing recent changes, causal chains, canaries, reversible mitigations | M01–M04, M07 | **CHECKED (local analogues); real incidents PROMISING** |
| Industrial process, manufacturing, supply-chain quality | Multiple process variables, upstream/downstream causes and interaction | M01, M03, M06, M08 | **CHECKED (authored analogues); deployment PROMISING** |
| Fraud detection, risk and compliance investigations | Correlated alerts, shared data ancestry, pressure to pick a culprit | M05 | **CHECKED (one authored analogue); transfer PROMISING** |
| Cybersecurity and security-incident attribution | Shared indicators, adversarial misdirection, competing threat paths | M04/M05 as *mechanism analogues only* | **PROMISING; untested in a security benchmark** |
| Long-running autonomous AI agents | Drift, feedback, tool state, retries, coordination, hidden failure coupling | [Worked agent case](../../examples/long-running-autonomous-agents-full-mode.md) | **PROMISING; illustrative protocol walkthrough only** |
| Scientific hypotheses and disputed origins | Competing causal hypotheses, source dependence, inaccessible evidence | [SARS-CoV-2 origins example](../../examples/sars-cov-2-origins-full-mode.md) | **PROMISING; not a scientific adjudication or validation** |
| Historical attribution and archival inquiry | Incomplete provenance, competing reconstructions, selection bias | [Historical worked example](../../examples/jack-the-ripper-full-mode.md) | **PROMISING; not a forensic conclusion** |
| Strategic choices, investment or architecture trade-offs | Model truth differs from reversible, option-preserving actions | Canonical causal/action split; M04/M06 as limited analogues | **PROMISING; no dedicated comparative trials** |
| Safety engineering, complex socio-technical incidents | Nested, interacting, cross-boundary mechanisms | M06/M07 as limited analogues | **PROMISING; no real-world safety validation** |
| Clinical differential diagnosis, public health | Confounding, competing diagnoses, downstream markers, unequal intervention risk | General causal architecture only | **UNCONFIRMED; no clinical accuracy/safety evaluation** |
| Legal investigations, intelligence, public policy | Conflicting testimony, evidence lineage, adversarial framing | Worked historical/science examples as illustrations only | **UNCONFIRMED; no legal/intelligence/policy performance trial** |
| Multimodal/live retrieval and autonomous action pipelines | Evidence may change during the run; context/tool boundaries may leak prior conclusions | Frozen local text-only runs | **UNCONFIRMED; no live-retrieval or multimodal efficacy test** |

No worked example should be represented as a real-world controlled experiment, and no item in this table establishes suitability for unsupervised high-stakes decisions.

## C. What specifically has and has not been verified

| Claim | Status | Reason |
|---|---|---|
| The implemented multi-stage Full *workflow* can complete auditable runs on one local model | **CHECKED (local)** | Frozen 32-run main benchmark; not every canonical conditional branch was implemented. |
| The isolated search boundary excluded injected prior-history content in tested cells | **CHECKED (mechanical)** | Byte-identical isolated paired search prompts/outputs in v0.1.4; runtime-specific, not universal host isolation. |
| Structured multi-pass workflows can resist deceptive premature attribution | **CHECKED (local signal)** | M05 separated Full/shared from single/Reduced; one authored case, no replication. |
| Full is the best default for routine, directly resolvable tasks | **UNCONFIRMED / contrary cost signal** | M01–M03 gave no Full action advantage; Full averaged ~9.1 calls/case. |
| Isolated workers improve answer quality beyond an otherwise matched shared workflow | **UNCONFIRMED (no effect shown)** | 16-cell v0.1.4: 0/8 false-anchor adoption even without isolation; shared prompt explicitly warned `NOT EVIDENCE`. |
| Corrected canonical Full v0.2 improves accuracy over a strong baseline | **UNCONFIRMED** | v0.2 is a conformance-corrected implementation target; no controlled performance benchmark yet. |
| Full beats compact Structured Core or frontier single-context | **UNCONFIRMED** | Structured Core and cross-model comparisons have not been run. |
| High-stakes-domain outcome improvement, better calibration across populations, statistically general gain | **UNCONFIRMED** | Authored cases, one model/repeat, no external field outcomes or population estimate. |

## D. Practical activation ladder (a recommendation, not a validated policy)

1. **Direct evidence + cheap reversible action:** ordinary single-context analysis or a domain-specific diagnostic test. Avoid protocol overhead.
2. **Several separable causes, bounded stakes:** compare alternatives, provenance and disconfirmers in a compact **structured multi-pass** workflow. This compact core is a *proposal*, not a benchmarked treatment under that name.
3. **Dependent evidence, hard framing, interacting causes, high lock-in:** consider extra adversarial passes and auditable causal/action separation. A shared-context multi-agent comparator already performed strongly; do not assume isolation itself produces a quality gain.
4. **Full Mode:** only when both (a) decision risk and information-boundary/audit needs justify the cost and (b) the runtime establishes effective context isolation for every isolation-dependent stage. Otherwise Full is **unavailable**, not merely inconvenient.
5. **Reduced Mode:** a clearly disclosed fallback when Full was requested but genuine isolation is unavailable, **with user consent**. Reduced is not a synonym for a cheaper ordinary/Core workflow.

At every level, separate **what caused this**, **what action is justified**, and **what new evidence would change that action**. Defer or abstain if the evidence warrants it. No universal numeric activation threshold or cross-domain guarantee has been established.

## E. Next falsifiable tests — NOT performed for this map

- **H01: interacting causes with a credible single-cause distractor.** Freeze new public evidence and a private key in advance; verify whether the system represents interaction *and* recommends the robust action. Compare single, compact Structured Core, and canonical Full on two fixed model endpoints.
- **H04: most probable cause differs from the best reversible action.** Freeze a loss/action contract and an answer key separately from case evidence; test causal correctness and action quality as distinct primary metrics.

These are candidate smoke/benchmark scenarios, **not positive results**. They should not be rushed into a post-hoc claim or treated as cross-model evidence without a controlled run. The local frozen endpoint used in the old ablation was not available at the time this map was prepared; **no new participant smoke run** is reported here.

**Bottom line:** the *structural applicability hypothesis* is broad; the demonstrated comparative advantage is narrow, conditional, and currently shared with a cheaper multi-pass baseline. Expand by preregistered difficult cases and another model, not by relabeling illustrative examples as validation.
