# Convergence Guard — Applicability Guide

Convergence Guard is not intended to make every analysis longer. Its value should rise when the main risk is **premature convergence**: committing to one plausible causal story before decision-relevant alternatives have been separated.

This guide distinguishes task classes where the protocol is likely to help from classes where its overhead can be counterproductive.

## Evidence status

The boundaries below are partly architectural and partly informed by the current technical pilot. The pilot is **not a performance proof**: it used only two cases, one repeat, and one local model. It is sufficient to identify a concrete failure mode and an applicability hypothesis worth testing in the main benchmark.

In the local pilot:

- **P01 — direct resolvable:** the single-context baseline returned the keyed `CHOOSE` result. Shared-context returned `COEXIST`; Reduced and Full Mode returned `INSUFFICIENT`. All four still recommended the correct corrective action.
- **P02 — intentionally underdetermined:** all four modes returned `INSUFFICIENT` and recommended diagnostic/canary-style next steps instead of forcing a causal winner.

The current interpretation is therefore a **testable hypothesis**, not a universal claim:

> Convergence Guard may be unnecessary or over-cautious on direct-resolvable problems, while becoming more useful as causal ambiguity, confounding, framing risk, evidence dependence, and the cost of premature commitment increase.

The planned main benchmark is designed to test that hypothesis across more task classes.

## Task classes

### 1. Direct resolvable

Typical characteristics:

- short causal chain;
- key mechanism is directly observed or nearly so;
- alternatives are quickly excluded;
- a cheap reversible corrective action exists;
- little value is expected from expanding the causal search space.

Example: a deployment changes one configuration value, logs show the resulting DNS failure, and a direct probe confirms the old target works while the new one does not.

**Recommended treatment:** ordinary single-context analysis or a routine diagnostic workflow. Full Mode is usually unnecessary.

### 2. Bounded ambiguity

Typical characteristics:

- 2–4 plausible mechanisms remain;
- evidence partially separates them;
- one additional observation or canary could materially change the decision;
- premature winner selection is a realistic risk.

**Recommended treatment:** Reduced Mode may be sufficient when isolation is unavailable; Full Mode becomes more attractive as anchoring risk and decision cost increase.

### 3. Resolvable with strong distractors

Typical characteristics:

- one causal model is ultimately better supported;
- another explanation is temporally salient, intuitively attractive, or repeatedly cited;
- several observations are compatible with both;
- the decisive evidence is easy to overlook.

This is a core Convergence Guard target. The method should help prevent the first plausible explanation from monopolizing later reasoning.

**Recommended treatment:** Full Mode is often justified when the wrong commitment is materially costly.

### 4. Interacting or layered causes

Typical characteristics:

- more than one cause may be real;
- one factor creates vulnerability while another triggers the event;
- two individually harmless changes may fail in combination;
- a common cause can make several apparent explanations move together.

These problems are poorly represented as a forced `A OR B`.

**Recommended treatment:** Reduced or Full Mode, with explicit attention to `COEXIST`, interaction, nesting, and causal roles.

### 5. Open-world causal investigation

Typical characteristics:

- the relevant hypothesis space is not known in advance;
- evidence quality and provenance vary sharply;
- sources can share common ancestry;
- framing itself may exclude important causal families;
- decisive experiments may be impossible;
- `INSUFFICIENT DATA TO CHOOSE` may be the correct endpoint.

Historical attribution, contested scientific-origin questions, strategic investigations, and complex socio-technical failures can fall into this class.

**Recommended treatment:** Full Mode when genuine context isolation is available and the stakes justify the cost.

## Quick activation test

Convergence Guard becomes more justified as more of the following are true:

| Signal | Low need for CG | Higher need for CG |
|---|---|---|
| Competing causes | one obvious mechanism | several causally distinct live models |
| Evidence separability | direct discriminating evidence | evidence is compatible with multiple stories |
| Confounding / interaction | negligible | material |
| Framing risk | low | plausible missing causal families |
| Evidence provenance | direct and independent | indirect, conflicting, or common-ancestry |
| Testability | cheap decisive test exists | tests are costly, delayed, or ambiguous |
| Reversibility | wrong action is cheap to undo | commitment creates lock-in or large downside |
| Cost of premature convergence | low | high |

If nearly every signal is in the left column, a heavy Convergence Guard run is probably unnecessary.

## What the pilot currently supports

The current pilot supports only three modest conclusions:

1. Full Mode can be executed end-to-end in an auditable local stateless runtime.
2. Direct-resolvable cases can expose a real **over-abstention / over-analysis** failure mode.
3. Intentionally underdetermined cases can exercise the protocol's legitimate abstention path.

It does **not** establish that CG is generally better than single-context analysis, nor does it establish a universal activation threshold.

## What the main benchmark should establish

The next benchmark should use new frozen cases spanning the task classes above, with the classes defined **before** results are inspected.

The useful empirical question is not simply:

> Does Convergence Guard win more often?

It is:

> Under which causal regimes does Convergence Guard improve decision quality enough to justify its additional cost, and under which regimes does it add unnecessary caution or overhead?

That result can support a practical activation guide for users and, eventually, an automatic triage step before choosing ordinary analysis, Reduced Mode, or Full Mode.
