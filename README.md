# Convergence Guard

[Русская версия](README.ru.md)

Convergence Guard is a decision-analysis protocol for difficult open-ended problems where the main failure mode is **premature convergence**: accepting one plausible causal explanation or action before decision-relevant alternatives have been separated, stress-tested, and compared.

It is packaged as an [Agent Skill](https://agentskills.io/) and is designed for agent clients that can provide genuinely isolated worker contexts.

![Convergence Guard workflow: shared question, evidence and decision contract flow through isolated search, blind screening and causal mapping, dossiers, pairwise comparison and an evidence-sufficiency gate. Outcomes are justified action, a discriminating check within budget, or explicit uncertainty.](assets/convergence-guard-workflow.png)

## Try it in 60 seconds

If your agent client supports Agent Skills:

1. clone or download this repository;
2. install or link the `convergence-guard/` directory into the skills directory used by your client, so it can discover `convergence-guard/SKILL.md`;
3. start with a prompt like this:

```text
Use Convergence Guard to analyze this question:

Why do autonomous AI agents still struggle with long-running real-world tasks,
and which intervention should be prioritized?

Use Full Mode only if the runtime's isolation preflight passes.
If genuine context isolation is unavailable, say so and use Reduced Mode only
if I accept that limitation. Do not force a winner when the evidence is
insufficient. End with the minimum observation or experiment that could change
the decision.
```

A Full Mode run should not merely produce several opinions. It should establish a decision contract, search causally distinct alternatives in isolated contexts, reduce them without exposing blind stages to one another, stress-test the surviving models, separate model judgment from action judgment, and either recommend an action or return `INSUFFICIENT DATA TO CHOOSE`.

Full Mode is runtime-agnostic, but it is not isolation-agnostic: a client must be able to establish genuine context separation wherever the protocol depends on blindness or independence. Multi-agent support by itself is not enough.

### The idea in one minute

Imagine a cup is broken on the floor. The cat is beside it, and a camera clearly shows the cat pushing it off the table. You do **not** need a panel of investigators, competing causal models, and a long evidence audit. A good ordinary analysis is faster and cheaper. Using Full Convergence Guard here would be like using a forensic laboratory to answer a question already settled by the video.

Now imagine a harder investigation. There are several plausible causes. Five reports appear to support one explanation — but after tracing their provenance, all five turn out to repeat the same original source. The most obvious story is persuasive, yet the evidence still does not justify choosing it over a live alternative. This is the kind of problem Convergence Guard is designed for: it aims to make it harder for the analysis to fall in love with the first convincing story.

That pattern appeared in the frozen `main-v0.1.7` **implemented-workflow benchmark**. On M05, a deliberately deceptive underdetermination case, single-context and the implemented Reduced treatment each received a blind-judge `premature_winner=1`; the implemented Full treatment and shared-context multi-agent preserved the live alternatives. Across all eight cases, the implemented Full treatment had **0/8 premature winners** and the highest mean action quality, but it cost about **9.1 model calls per case instead of 1** for single-context.

So the practical rule is simple:

> **For an easy question, Convergence Guard can be a cannon aimed at a sparrow. For a difficult investigation, it is a useful way to stop the analyst from committing too early to a beautiful but insufficiently supported explanation.**

The benchmark does not show that canonical Full Mode is always best. A post-benchmark conformance audit found that `main-v0.1.7` exercised **simplified Full/Reduced implementations**, not every conditional rule in the current specification. Shared-context multi-agent also had 0/8 premature winners at substantially lower cost, and the implemented Full workflow was sometimes overly cautious about `COEXIST` cases. The evidence supports **selective structured analysis on difficult, ambiguity-heavy decisions**, not automatic use everywhere.

A follow-up 16-cell targeted isolation ablation then held the model, evidence, search mandates, call count, seeds, and synthesis structure fixed while varying only whether search workers could see prior conclusions. The isolation boundary passed its mechanical integrity check, but **no false-anchor adoption occurred even in the shared treatment (0/8 across two independent anchor judges)**. So the current evidence does **not** demonstrate an incremental answer-quality benefit from isolation itself under that tested manipulation. See the [isolation result](evals/results/isolation-ablation-v0.1.4/INTERPRETATION.md).

## Why not just ask 5 agents?

Because five answers are not automatically five independent pieces of evidence.

- **Reasoning independence is not evidential independence.** Agents can reason separately while relying on the same source, dataset, summary, or inherited claim. Agreement can therefore reflect common evidence ancestry rather than independent corroboration.
- **Shared framing creates correlated errors.** If every agent starts from the same candidate set, assumptions, memory, or problem framing, several independent-looking branches can reproduce the same blind spot.
- **Voting measures agreement, not evidential weight.** A 4-to-1 majority can still be four restatements of one weak premise. Convergence Guard compares provenance, causal predictions, assumptions, and decision consequences instead of treating votes as proof.
- **Sometimes there should be no winner.** Convergence Guard includes an evidence-sufficiency gate and can return `INSUFFICIENT DATA TO CHOOSE` rather than manufacturing consensus.

The point is therefore not to use more agents. It is to create **structured independence, controlled information boundaries, provenance-aware comparison, and a legitimate abstention path**.

## What problem does it solve?

Complex analysis often fails in a predictable way:

1. the first plausible explanation becomes an anchor;
2. later alternatives are generated inside that anchor;
3. several agents agree because they share the same evidence, priors, or framing;
4. causal stories are polished without being causally identified;
5. the most plausible model is silently treated as the best action;
6. the final answer sounds confident but does not say what observation would change the decision.

Convergence Guard is designed to make those failures harder.

A central principle of the current architecture is:

> **Reasoning independence is not evidential independence, and the most plausible model is not always the best action under uncertainty.**

For evidence-heavy research, Convergence Guard also evaluates **claims rather than source prestige**. Official, peer-reviewed, institutional, fringe, or anonymous status affects verification strategy but never substitutes for claim-level provenance, inspectability, and evidence ancestry.

## When is Convergence Guard worth using?

Convergence Guard is not meant to make every problem harder. The frozen `main-v0.1.7` workflow benchmark provides a broader applicability signal across eight causal regimes and four implemented modes (32 participant runs total, one repeat per `case × mode` cell), but it should not be read as a complete validation of the canonical Full/Reduced specification.

- `cg-full` produced **0/8 premature winners**, **2/2 correct abstentions** on the keyed-insufficient cases, and the highest mean action quality (**1.875/2**), but at high cost: about **9.1 model calls, 12.5k input tokens, and 5.6k output tokens per case** on average;
- shared-context multi-agent also produced **0/8 premature winners** and **2/2 correct abstentions**, with lower cost but weaker mean action and next-test scores;
- single-context and `cg-reduced` each produced one premature winner on the deliberately deceptive underdetermination case M05;
- Full Mode did **not** dominate every diagnostic: its literal declared status matched the hidden key in 5/8 cases, versus 6/8 for single-context, and the current metric set does not fully collapse every `CHOOSE / COEXIST / INSUFFICIENT` structural error into one scalar correctness score.

One important scoring caveat: blind semantic judging used the **predeclared normalized** `final.json` artifacts. A later blind raw-vs-normalized re-audit of all 16 M04–M07 runs found N1 applied in **15/16** runs, with the two judges often agreeing that the repair materially changed winner-like semantic interpretation. The frozen scores remain unchanged, because the normalizer was predeclared and treatment-independent, but normalization should no longer be treated as merely cosmetic output cleanup. See the [normalization re-audit](evals/results/main-v0.1.7/diagnostics/REJUDGE-REPORT.md).

The result therefore supports a **selective-use** interpretation: heavier structured analysis appears most useful when framing risk, evidence dependence, causal ambiguity, or premature-commitment cost are high, but it is expensive and should not be treated as the default for every resolvable task. A subsequent conformance audit found missing/partial canonical branches in the v0.1.7 executable Full/Reduced treatments; the v0.2 correction layer now records those gaps explicitly and fails closed instead of silently calling an incomplete path “Full Mode complete.”

The targeted isolation ablation adds another important limit: the implemented isolation boundary worked mechanically, but the shared treatment also resisted the injected false anchors, so **the incremental quality benefit of isolation remains unproven** in the current evidence base.

See the bilingual [Applicability Guide](convergence-guard/references/applicability.md) / [Руководство по применимости](convergence-guard/references/applicability.ru.md), the raw [main benchmark metric report](evals/results/main-v0.1.7/REPORT.md), the paired [main interpretation](evals/results/main-v0.1.7/INTERPRETATION.md) / [Russian](evals/results/main-v0.1.7/INTERPRETATION.ru.md), the [v0.2 conformance matrix](evals/protocol/v0.2/CONFORMANCE-MATRIX.md), and the paired [isolation-ablation interpretation](evals/results/isolation-ablation-v0.1.4/INTERPRETATION.md) / [русская версия](evals/results/isolation-ablation-v0.1.4/INTERPRETATION.ru.md). The earlier two-case technical pilot remains documented in [evals/PILOT-REPORT-v0.1.md](evals/PILOT-REPORT-v0.1.md).

## Current workflow

The public protocol is organized into five phases:

```text
A. ESTABLISH THE DECISION
   evidence provenance → decision contract → framing / outside view

B. SEARCH THE CAUSAL SPACE
   3 isolated search mandates → coverage gate → expand to 4–5 only if needed

C. REDUCE WITHOUT ANCHORING
   fresh screening ║ blind causal mapping
   → optional boundary audit
   → normally 2–3 model finalists; may collapse to 1 or 0 after coverage/evidence checks + optional information probe

D. STRESS AND ADJUDICATE
   independent causal dossiers
   → assumption sensitivity
   → shared-bias audit
   → pairwise decision collision
   → optional independent second opinion

E. CONVERGE ON ACTION AND LEARNING
   model judgment ≠ action judgment
   → evidence-sufficiency gate
   → best action or INSUFFICIENT DATA TO CHOOSE
   → minimum decision-changing observation / experiment
```

## What changed from v0.1.0?

v0.2.3 retains the streamlined v0.2 architecture, v0.2.1 runtime-isolation rules, and v0.2.2 claim-level provenance discipline, while adding benchmark-informed activation guidance and a conformance-corrected evaluation layer:

- search starts with 3 isolated workers and expands to 5 only when coverage is inadequate;
- screening and blind causal mapping run in parallel fresh contexts;
- boundary review is conditional rather than automatic;
- the finalist slate normally contains 2–3 viable models, may collapse to one genuine survivor or none, and is never padded;
- model relations can be exclusive, coexisting, nested, or interacting;
- causal completeness is separated from causal identification;
- duplicate model families never count as independent corroboration;
- dossier workers no longer compare against rivals they cannot see;
- assumption sensitivity targets high-leverage uncertain assumptions rather than one arbitrary mutation;
- shared blind spots can trigger targeted new evidence/search instead of recycling the same candidate pool;
- pairwise collision compares decision-conflicting implications, not forced winner/loser pairs;
- an explicit decision layer separates belief about causes from action under loss, regret, reversibility, and option value;
- Reduced Mode is formally defined for hosts without isolated worker contexts;
- material claims are evaluated by provenance, inspectability, common evidence ancestry, contradictions, and source role rather than reputation alone;
- material new evidence discovered inside a blind branch must pass a shared evidence checkpoint before it can change downstream decisions.

## Repository layout

```text
Convergence Guard/
├── .gitattributes
├── README.md
├── README.ru.md
├── CHANGELOG.md
├── CHANGELOG.ru.md
├── DESIGN.md
├── DESIGN.ru.md
├── LICENSE
├── ATTRIBUTION.md
├── ATTRIBUTION.ru.md
├── THIRD_PARTY_NOTICES.md
├── examples/
│   ├── jack-the-ripper-full-mode.md
│   ├── jack-the-ripper-full-mode.ru.md
│   ├── long-running-autonomous-agents-full-mode.md
│   ├── long-running-autonomous-agents-full-mode.ru.md
│   ├── sars-cov-2-origins-full-mode.md
│   └── sars-cov-2-origins-full-mode.ru.md
└── convergence-guard/
    ├── SKILL.md
    └── references/
        ├── explained-simply.md
        ├── explained-simply.ru.md
        ├── applicability.md
        ├── applicability.ru.md
        ├── protocol-details.md
        ├── protocol-details.ru.md
        ├── reduced-mode.md
        ├── reduced-mode.ru.md
        └── protocol.ru.md
```

`convergence-guard/` is the installable skill directory. Install the entire directory, including `references/`; `SKILL.md` alone is not a complete Full/Reduced Mode package unless an adapter explicitly bundles the required references. Its directory name matches `name: convergence-guard` in `SKILL.md`.

`protocol.ru.md` is preserved as the **historical Russian v0.1.0 protocol**. It is not the canonical v0.2.3 specification; runtime-specific wording has been neutralized for the public repository.

## Documentation

| English | Russian | Purpose |
|---|---|---|
| [README.md](README.md) | [README.ru.md](README.ru.md) | project overview |
| [CHANGELOG.md](CHANGELOG.md) | [CHANGELOG.ru.md](CHANGELOG.ru.md) | release history |
| [DESIGN.md](DESIGN.md) | [DESIGN.ru.md](DESIGN.ru.md) | threat model and architectural rationale |
| [ATTRIBUTION.md](ATTRIBUTION.md) | [ATTRIBUTION.ru.md](ATTRIBUTION.ru.md) | provenance and influence boundary |
| [explained-simply.md](convergence-guard/references/explained-simply.md) | [explained-simply.ru.md](convergence-guard/references/explained-simply.ru.md) | plain-language explanation |
| [applicability.md](convergence-guard/references/applicability.md) | [applicability.ru.md](convergence-guard/references/applicability.ru.md) | when CG is likely to help, and when it may be excessive |
| [protocol-details.md](convergence-guard/references/protocol-details.md) | [protocol-details.ru.md](convergence-guard/references/protocol-details.ru.md) | detailed protocol rules |
| [reduced-mode.md](convergence-guard/references/reduced-mode.md) | [reduced-mode.ru.md](convergence-guard/references/reduced-mode.ru.md) | single-context fallback |

## Case studies

Public worked examples:

- [English: Jack the Ripper — Full Mode case study](examples/jack-the-ripper-full-mode.md)
- [Русский: Джек Потрошитель — пример Full Mode](examples/jack-the-ripper-full-mode.ru.md)
- [English: Why autonomous AI agents fail on long-running real-world tasks — Full Mode case study](examples/long-running-autonomous-agents-full-mode.md)
- [Русский: Почему автономные AI-агенты ломаются на длительных реальных задачах — Full Mode case study](examples/long-running-autonomous-agents-full-mode.ru.md)
- [English: SARS-CoV-2 origins — Full Mode case study](examples/sars-cov-2-origins-full-mode.md)
- [Русский: Происхождение SARS-CoV-2 — пример Full Mode](examples/sars-cov-2-origins-full-mode.ru.md)

The examples record the decision contract, provenance-aware evidence brief, causal-search mandates, coverage gate, blind reduction, finalist dossiers, adjudication, conditional second-opinion review, evidence-sufficiency gate, and the decision-changing observation.

> **Scope of examples:** these case studies demonstrate operation of a decision-analysis protocol over the evidence available to a particular run. They are not substitutes for laboratory research, field investigation, forensic or criminal investigation, intelligence analysis, legal findings, or other domain-specific primary work. Where primary or non-public evidence is inaccessible, the examples preserve that limitation rather than treating an institutional assessment as direct confirmation of the underlying event.

## Full Mode and Reduced Mode

**Full Mode** requires genuine isolated worker/agent contexts for operations that depend on independence or blindness.

**Reduced Mode** is a disclosed single-context fallback. It preserves the reasoning shape but cannot reproduce the information-boundary and blindness guarantees created by isolated workers. It must not be presented as equivalent to Full Mode.

## Language and localization

The canonical agent-facing protocol is written in English for portable discovery and execution across clients. The skill instructs the agent to answer in the user's language unless another language is requested.

Public human-facing documentation is maintained as paired English/Russian files where practical. The installable `SKILL.md` remains canonical English; current explanatory and operational references have Russian siblings. The historical Russian v0.1.0 protocol remains preserved separately in `convergence-guard/references/protocol.ru.md`.

## Installation

Install or link the `convergence-guard/` directory into the skills directory used by your agent client.

The exact installation mechanism depends on the client. A compatible client should discover `convergence-guard/SKILL.md` and use its `name` and `description` metadata to determine relevance.

## Status

**Research pre-release. Latest tagged release: v0.2.3.**

The current tagged research preview is [v0.2.3](https://github.com/lavalava45/convergence-guard/releases/tag/v0.2.3). It includes the frozen implemented-workflow benchmark, the post-benchmark conformance corrections, the normalization re-audit, and the targeted isolation ablation. It does **not** establish universal performance superiority or a measured canonical Full v0.2 quality gain. Later changes, when present, are tracked in [CHANGELOG.md](CHANGELOG.md).

The methodology has undergone an initial architecture and failure-mode audit and now includes public Full Mode worked examples spanning historical attribution, a current evidence-asymmetric scientific-origin question, and a contemporary AI-agent reliability problem. The two-case technical pilot has been followed by the frozen `main-v0.1.7` comparative benchmark: 8 cases × 4 modes × 1 repeat = 32 participant runs, followed by 32 calibration runs and blind semantic judging under neutral answer IDs. The result is evidence for an applicability map, not a universal superiority claim: in this 8-case set Full Mode had no observed premature winners and produced the strongest mean actions, while imposing much higher resource cost and still showing structural/status mismatches on some coexistence cases.

## Attribution

Early versions of this protocol were inspired by Udit Akhouri's ADHD divergent-ideation skill. The current method substantially redesigns the workflow around causal models, information isolation, adversarial comparison, assumption stress-testing, and falsifiable convergence.

See [ATTRIBUTION.md](ATTRIBUTION.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## License

MIT. See [LICENSE](LICENSE).
