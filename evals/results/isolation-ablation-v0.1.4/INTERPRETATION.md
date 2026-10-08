# Isolation ablation v0.1.4 — interpretation

This is the interpretation layer for the frozen targeted isolation experiment. The machine-readable result is in `summary.json`; the two-judge consensus table is in `REPORT.md`.

> **Presentation erratum:** the frozen report generator contains a heading-only typo and writes `Isolation ablation v0.1.2` at the top of `REPORT.md`. The machine-readable `summary.json`, run plan, freeze manifest, result directory, and all participant/judge artifacts identify the valid study as `isolation-ablation-v0.1.4`. The typo affects no metric or mapping and is deliberately left in the generated report so the report remains byte-reproducible from the frozen aggregator.

## Why this experiment was run

The completed `main-v0.1.7` study compared four workflows, but a post-benchmark conformance audit found that its executable `cg-full` and `cg-reduced` treatments were simplified implementations rather than exact executions of every canonical Convergence Guard rule. That means the main study cannot cleanly answer a narrower mechanistic question: **does context isolation itself add protection against anchoring when the rest of the workflow is held fixed?**

`isolation-ablation-v0.1.4` was designed only for that question.

## Design

Four already-frozen cases (`M02`, `M03`, `M04`, `M06`) were run under a 2×2 design:

- isolated search vs shared-history search;
- neutral prior history vs a confident but keyed-wrong false prior conclusion.

Every cell used the same public evidence, model, three search mandates, four logical model calls, temperature, token ceilings, paired stage seeds, and neutral synthesizer. The final synthesizer never saw the injected history directly.

In isolated cells the three search workers never saw parent history or peer outputs. In shared cells they did. The experiment therefore varies one mechanism much more narrowly than the main workflow benchmark.

After several transparently documented execution-only aborts, the valid replacement `v0.1.4` completed **16/16 cells** on the frozen standalone endpoint `http://127.0.0.1:55991/v1`. All **64/64 saved model responses** report that endpoint. Four transient transport failures required a second same-request attempt; no cell was invalidated.

## Manipulation integrity

The isolated manipulation passed its strongest mechanical check.

For every case, `isolated-neutral` and `isolated-false-anchor` had byte-identical model-visible search prompts, identical paired seeds, and byte-identical search outputs. Because the final synthesizer received those same search outputs, the isolated final outputs were also identical within each case.

This demonstrates that the injected history was in fact absent from the isolated treatment path.

## Result

The experiment **did not demonstrate an isolation benefit** on these four cases.

Two independent blind judges first scored causal structure, premature winner, over-abstention, action quality, and next-test quality without seeing isolation condition, history condition, run IDs, anchors, or resource use. Only after those scores were frozen did two independent anchor judges see the false-anchor packets.

Both anchor judges agreed on all eight false-anchor cells:

> **false-anchor adoption = 0/8**

The shared workers were directly exposed to the false prior conclusion, yet no final answer substantively adopted it as the causal winner or privileged explanation.

The primary quality metrics also do not show degradation caused by the false anchor:

| Condition | Structure correct ↑ | Premature winner ↓ | Action quality ↑ | Next-test quality ↑ | False-anchor adoption ↓ |
|---|---:|---:|---:|---:|---:|
| isolated-neutral | 0.750 (4/4 rated) | 0.250 | 1.750 | 0.750 | N/A |
| isolated-false-anchor | 0.750 (4/4) | 0.250 | 1.750 | 0.750 | 0.000 |
| shared-neutral | 0.667 (3/4; 1 judge disagreement) | 0.250 | 1.750 | 1.000 (3/4 rated) | N/A |
| shared-false-anchor | 1.000 (4/4) | 0.000 | 1.750 | 0.333 (3/4 rated) | 0.000 |

Three field-level blind-judge disagreements are left visible rather than silently adjudicated post hoc.

The apparently better shared-false-anchor structure/premature-winner numbers must **not** be interpreted as evidence that a false anchor helps. With four authored cases, one run per cell, and a few judge disagreements, that pattern is descriptive noise/idiosyncrasy unless replicated.

## What this means

This result changes the evidential status of one Convergence Guard design claim.

We now have direct evidence that the implemented isolation boundary can prevent hidden parent history from entering the search workers: the paired isolated artifacts prove that mechanically.

But we **do not yet have evidence that this isolation improves answer quality** under the tested contamination. The shared workflow resisted the false anchors on its own.

The correct claim is therefore:

> **Isolation is an implemented information-boundary control with a plausible threat model, but its incremental quality benefit was not demonstrated by this four-case false-anchor ablation.**

That is narrower than saying isolation is useless. This experiment can only rule on the tested manipulation.

## Important limitation of the anchor manipulation

The shared-history prompt explicitly labeled the inherited conclusion as **“NOT EVIDENCE”** and instructed the worker to re-check it against supplied evidence and not count peer agreement as corroboration. That is good analysis hygiene, but it also acts as an anti-anchoring warning.

Therefore this experiment tested whether isolation adds value **on top of an explicit anti-anchor instruction**. The zero-adoption result may mean the instruction was already sufficient for these cases/model, leaving little room for isolation to improve the measured outcomes.

A stronger future test, if warranted, should preserve ethical/evaluation clarity while making contamination more realistic: for example, inherited intermediate reasoning that is plausible and unlabeled, repeated peer consensus with common ancestry, or a longer multi-step chain where early framing can shape which evidence is ever considered. Such a follow-up should be frozen before execution and should not be inferred from this result.

## Relation to the main benchmark

The main benchmark remains useful as a descriptive comparison of the four **implemented workflows**, but the post-benchmark audit requires narrower wording:

- it did not validate every conditional branch of canonical Full Mode;
- the v0.1.7 Reduced packet was not fully self-contained with respect to every rule it referenced;
- normalization materially altered winner-like causal content in many M04–M07 raw outputs;
- shared-context multi-agent already performed strongly on premature-winner/abstention metrics;
- this targeted ablation found no added answer-quality protection from isolation under the tested false-anchor manipulation.

The v0.2 correction layer addresses the specification/execution gaps with a conformance matrix, self-contained Reduced packet, separate causal/action/protocol-completion schema, fail-closed triggered stages, and raw-vs-normalized diagnostics. Those changes are infrastructure corrections, not retroactive changes to the frozen `main-v0.1.7` scores.

## Bottom line

The evidence now supports three different statements with different strength:

1. **Structured multi-pass analysis looked useful on some difficult cases in the original workflow benchmark.** This remains descriptive and is not a canonical-Full causal effect estimate.
2. **The isolation boundary works mechanically.** The paired isolated artifacts prove that hidden history did not enter those search contexts.
3. **The incremental quality benefit of isolation is still unproven.** This targeted 16-cell experiment produced no false-anchor adoption even without isolation.

That is the current honest evidence boundary.
