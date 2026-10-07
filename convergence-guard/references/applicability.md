# Convergence Guard — Applicability Guide

Convergence Guard is not intended to make every analysis longer. Its value should rise when the main risk is **premature convergence**: committing to one plausible causal story before decision-relevant alternatives have been separated.

This guide distinguishes task classes where the protocol is likely to help from classes where its overhead can be counterproductive.

## Evidence status

The boundaries below are architectural, but they are now also informed by the frozen `main-v0.1.7` benchmark: 8 cases × 4 modes × 1 repeat = 32 participant runs using one fixed local model, followed by calibration and blind semantic judging. This is **evidence for an applicability map, not a universal performance proof**. One model, eight authored cases, and one repeat per cell do not establish a population-wide ranking.

The main benchmark produced four useful signals:

- **Full Mode had fewer observed premature winners in this 8-case set:** `cg-full` had 0/8 premature winners; single-context and `cg-reduced` each had 1/8. This is descriptive, not a causal or population-level effect estimate.
- **The strongest separation appeared on deceptive underdetermination:** on M05, where apparently abundant evidence largely descended from one evidence branch, Full Mode and shared-context preserved the live alternatives while single-context and Reduced each received `premature_winner=1` and `correct_abstention=0` from the blind judge.
- **Simple/resolvable cases did not justify Full Mode's cost:** on direct and strongly resolvable cases, Full Mode did not produce a decision-quality advantage commensurate with roughly 9.1 model calls per case versus 1 for single-context.
- **Full Mode is not a universal winner:** shared-context multi-agent also achieved 0/8 premature winners at lower cost, and Full Mode sometimes expressed overly cautious literal statuses on keyed `COEXIST` cases.

All blind semantic scores above use the frozen normalized participant artifact. In raw Full Mode outputs for the two keyed-insufficient cases M04 and M05, `preferred_cause` was still populated despite `status=INSUFFICIENT`; the predeclared treatment-independent normalization rule cleared that field before judging. This makes the published abstention scores valid under the frozen protocol, but it is a material output/interpretation caveat rather than evidence of perfectly clean raw abstention behavior.

The current interpretation is therefore:

> Convergence Guard is most justified when causal ambiguity, framing risk, evidence dependence, or the cost of premature commitment is high. Interaction/`COEXIST` structure requires explicit checking, but it is **not by itself** a reason to escalate to Full Mode; escalation is justified when the interaction is hard to separate and additional evidence-dependence, framing/open-world, or commitment-risk factors make the isolation overhead worthwhile. It is usually unnecessary for directly resolved problems, and Full Mode should not be treated as the default when a cheaper workflow already separates the live causes adequately.

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

This is a core Convergence Guard target. The benchmark supports the value of structured multi-stage analysis here, but does not show that Full Mode is always better than a cheaper multi-pass comparator.

**Recommended treatment:** use Full Mode when the wrong commitment is materially costly **and** the extra isolation/anti-anchoring guarantees justify its cost. If Full Mode is unnecessary despite being available, prefer ordinary or cheaper multi-pass analysis rather than relabeling it Reduced Mode. Use Reduced Mode as the explicit fallback when genuine isolation is unavailable and the user accepts that limitation.

### 4. Interacting or layered causes

Typical characteristics:

- more than one cause may be real;
- one factor creates vulnerability while another triggers the event;
- two individually harmless changes may fail in combination;
- a common cause can make several apparent explanations move together.

These problems are poorly represented as a forced `A OR B`.

**Recommended treatment:** explicitly model `COEXIST`, interaction, nesting, and causal roles in whatever workflow is used. Escalate to Full Mode only when the interaction is hard to separate **and** another material risk—such as evidence dependence, framing/open-world search risk, or costly irreversible commitment—makes stronger isolation worth the overhead. If isolation is unavailable and the user accepts the limitation, Reduced Mode is the fallback.

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
| Confounding / interaction | negligible or easy to separate | material **and hard to separate in a decision-relevant way** |
| Framing risk | low | plausible missing causal families |
| Evidence provenance | direct and independent | indirect, conflicting, or common-ancestry |
| Testability | cheap decisive test exists | tests are costly, delayed, or ambiguous |
| Reversibility | wrong action is cheap to undo | commitment creates lock-in or large downside |
| Cost of premature convergence | low | high |

If nearly every signal is in the left column, a heavy Convergence Guard run is probably unnecessary.

## What the current benchmark supports

The completed `main-v0.1.7` study supports four modest conclusions:

1. Full Mode can be executed end-to-end in an auditable isolated local runtime; in this 8-case set it had fewer observed unsupported winner selections on ambiguity-heavy cases than single-context and Reduced Mode.
2. The strongest observed benefit appeared where evidence dependence and framing created false confidence, not on directly resolvable cases.
3. Full Mode's quality gains come with substantial resource overhead, so selective activation matters.
4. Some benefit appears to come from multi-pass analysis generally: shared-context multi-agent performed strongly on several primary metrics, so the current study does not isolate a pure effect of CG-specific information boundaries.

It still does **not** establish that CG is generally superior to ordinary analysis, nor does it establish a universal numeric activation threshold. The benchmark also exposed a metric gap around complete semantic causal-structure correctness for `CHOOSE / COEXIST / INSUFFICIENT` outcomes.

The useful empirical question remains:

> Under which causal regimes does Convergence Guard improve decision quality enough to justify its additional cost, and under which regimes does it add unnecessary caution or overhead?

The current result is enough to support a practical activation guide. The next evidence-building step should be replication on another model/runtime and/or targeted retesting of the cases where modes diverged most, not merely making every run larger.
