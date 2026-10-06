# Convergence Guard

[Русская версия](README.ru.md)

Convergence Guard is a decision-analysis protocol for difficult open-ended problems where the main failure mode is **premature convergence**: accepting one plausible causal explanation or action before decision-relevant alternatives have been separated, stress-tested, and compared.

It is packaged as an [Agent Skill](https://agentskills.io/) and is designed for agent clients that can provide genuinely isolated worker contexts.

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
   → 2–3 model finalists + optional information probe

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

v0.2.1 keeps the streamlined v0.2 architecture while tightening runtime-isolation rules and recovery behavior:

- search starts with 3 isolated workers and expands to 5 only when coverage is inadequate;
- screening and blind causal mapping run in parallel fresh contexts;
- boundary review is conditional rather than automatic;
- the finalist slate contains 2–3 viable models and is never padded;
- model relations can be exclusive, coexisting, nested, or interacting;
- causal completeness is separated from causal identification;
- duplicate model families never count as independent corroboration;
- dossier workers no longer compare against rivals they cannot see;
- assumption sensitivity targets high-leverage uncertain assumptions rather than one arbitrary mutation;
- shared blind spots can trigger targeted new evidence/search instead of recycling the same candidate pool;
- pairwise collision compares decision-conflicting implications, not forced winner/loser pairs;
- an explicit decision layer separates belief about causes from action under loss, regret, reversibility, and option value;
- Reduced Mode is formally defined for hosts without isolated worker contexts.

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
│   ├── sars-cov-2-origins-full-mode.md
│   └── sars-cov-2-origins-full-mode.ru.md
└── convergence-guard/
    ├── SKILL.md
    └── references/
        ├── explained-simply.md
        ├── explained-simply.ru.md
        ├── protocol-details.md
        ├── protocol-details.ru.md
        ├── reduced-mode.md
        ├── reduced-mode.ru.md
        ├── runtime-chat-on-steroids.md
        ├── runtime-chat-on-steroids.ru.md
        └── protocol.ru.md
```

`convergence-guard/` is the installable skill directory. Its directory name matches `name: convergence-guard` in `SKILL.md`.

`protocol.ru.md` is preserved as the **historical Russian v0.1.0 protocol**. It is not the canonical v0.2.1 specification.

## Documentation

| English | Russian | Purpose |
|---|---|---|
| [README.md](README.md) | [README.ru.md](README.ru.md) | project overview |
| [CHANGELOG.md](CHANGELOG.md) | [CHANGELOG.ru.md](CHANGELOG.ru.md) | release history |
| [DESIGN.md](DESIGN.md) | [DESIGN.ru.md](DESIGN.ru.md) | threat model and architectural rationale |
| [ATTRIBUTION.md](ATTRIBUTION.md) | [ATTRIBUTION.ru.md](ATTRIBUTION.ru.md) | provenance and influence boundary |
| [explained-simply.md](convergence-guard/references/explained-simply.md) | [explained-simply.ru.md](convergence-guard/references/explained-simply.ru.md) | plain-language explanation |
| [protocol-details.md](convergence-guard/references/protocol-details.md) | [protocol-details.ru.md](convergence-guard/references/protocol-details.ru.md) | detailed protocol rules |
| [reduced-mode.md](convergence-guard/references/reduced-mode.md) | [reduced-mode.ru.md](convergence-guard/references/reduced-mode.ru.md) | single-context fallback |
| [runtime-chat-on-steroids.md](convergence-guard/references/runtime-chat-on-steroids.md) | [runtime-chat-on-steroids.ru.md](convergence-guard/references/runtime-chat-on-steroids.ru.md) | local runtime profile |

## Case studies

Public worked examples:

- [English: Jack the Ripper — Full Mode case study](examples/jack-the-ripper-full-mode.md)
- [Русский: Джек Потрошитель — пример Full Mode](examples/jack-the-ripper-full-mode.ru.md)
- [English: SARS-CoV-2 origins — Full Mode case study](examples/sars-cov-2-origins-full-mode.md)
- [Русский: Происхождение SARS-CoV-2 — пример Full Mode](examples/sars-cov-2-origins-full-mode.ru.md)

The examples record the decision contract, provenance-aware evidence brief, causal-search mandates, coverage gate, blind reduction, finalist dossiers, adjudication, conditional second-opinion review, evidence-sufficiency gate, and the decision-changing observation.

> **Scope of examples:** these case studies demonstrate operation of a decision-analysis protocol over the evidence available to a particular run. They are not substitutes for laboratory research, field investigation, forensic or criminal investigation, intelligence analysis, legal findings, or other domain-specific primary work. Where primary or non-public evidence is inaccessible, the examples preserve that limitation rather than treating an institutional assessment as direct confirmation of the underlying event.

## Full Mode and Reduced Mode

**Full Mode** requires genuine isolated worker/agent contexts for operations that depend on independence or blindness.

**Reduced Mode** is a disclosed single-context fallback. It preserves the reasoning shape but cannot reproduce the anti-anchoring guarantees created by isolated workers. It must not be presented as equivalent to Full Mode.

## Language and localization

The canonical agent-facing protocol is written in English for portable discovery and execution across clients. The skill instructs the agent to answer in the user's language unless another language is requested.

Public human-facing documentation is maintained as paired English/Russian files where practical. The installable `SKILL.md` remains canonical English; current explanatory and operational references have Russian siblings. The historical Russian v0.1.0 protocol remains preserved separately in `convergence-guard/references/protocol.ru.md`.

## Installation

Install or link the `convergence-guard/` directory into the skills directory used by your agent client.

The exact installation mechanism depends on the client. A compatible client should discover `convergence-guard/SKILL.md` and use its `name` and `description` metadata to determine relevance.

## Status

**Pre-release. Latest tagged release: v0.2.1.**

The `main` branch contains unreleased documentation and protocol refinements after v0.2.1; see [CHANGELOG.md](CHANGELOG.md).

The methodology has undergone an initial architecture and failure-mode audit and now includes public Full Mode worked examples spanning historical attribution and a current evidence-asymmetric scientific-origin question. It remains pre-release: broader empirical evaluation is still needed across current questions and against ordinary single-context analysis and lighter multi-agent baselines.

## Attribution

Early versions of this protocol were inspired by Udit Akhouri's ADHD divergent-ideation skill. The current method substantially redesigns the workflow around causal models, information isolation, adversarial comparison, assumption stress-testing, and falsifiable convergence.

See [ATTRIBUTION.md](ATTRIBUTION.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## License

MIT. See [LICENSE](LICENSE).
