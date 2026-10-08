# Main benchmark v0.1.7 — interpretation

This is the interpretation layer for the frozen `main-v0.1.7` result set. The machine-readable aggregate is in `summary.json`; the metric table is in `REPORT.md`.

> **Post-benchmark correction note:** a later conformance audit found that the executable `cg-full` and `cg-reduced` treatments in this study were simplified implementations rather than exact executions of every conditional rule in the current canonical specification. The frozen scores below remain historical results for those implemented workflows; they should not be read as a complete validation of canonical Full/Reduced Mode. See `../../protocol/v0.2/CONFORMANCE-MATRIX.md` and the later `../isolation-ablation-v0.1.4/INTERPRETATION.md`.

## What was run

The final main study used 8 frozen cases × 4 modes × 1 repeat = **32 participant runs**. The reduction from the earlier 64-run design to one repeat was declared before the final study version began; it trades variance estimation for completing one full `case × mode` matrix. The final participant runtime was a dedicated local `llama-server 2.52.0` process using `gemma-4-12b-it-Q6_K.gguf`, context 15,000, full GPU offload, KV offload, one parallel slot, SSE streaming, and cross-request prompt caching disabled.

All **32/32 primary runs** completed and were frozen before calibration. All **32/32 calibration runs** then completed with no calibration failures. Semantic judging used neutral answer IDs and three independent judge contexts that did not receive mode names, run IDs, cost, latency, worker counts, or the private blind mapping. No post-hoc weighted composite score is reported.

## Main result

The implemented `cg-full` treatment had the strongest aggregate action score and the most conservative premature-convergence profile:

- premature winner: **0/8** for `cg-full`, **0/8** for shared-context multi-agent, **1/8** for single-context, **1/8** for `cg-reduced`;
- correct abstention on the two keyed-insufficient cases: **2/2** for `cg-full`, **2/2** for shared-context multi-agent, **1/2** for single-context, **1/2** for `cg-reduced`;
- mean action quality: **1.875/2** for `cg-full`, 1.625 for single-context, 1.625 for shared-context multi-agent, and 1.500 for `cg-reduced`;
- mean decision-relevant mechanism recall: **1.000** for `cg-full`, shared-context, and single-context; 0.958 for `cg-reduced`;
- mean next-test quality was **not** best for Full Mode: 1.500 for `cg-full` versus 1.625 for both single-context and `cg-reduced`.

These semantic scores are scores of the frozen normalized `final.json` artifacts. A later blind raw-vs-normalized re-audit of all 16 M04–M07 runs found N1 applied in **15/16** runs; two independent judges often found that deleting the raw `preferred_cause` materially changed winner-like semantic interpretation. The frozen benchmark scores remain unchanged because N1 was predeclared and treatment-independent, but raw-output behavior was less clean than the aggregate alone suggests. See `diagnostics/REJUDGE-REPORT.md`.

The clearest applicability signal appeared on **M05, deceptive underdetermination**. Both `cg-full` and shared-context preserved the live alternatives under blind semantic judging; single-context and `cg-reduced` each received `premature_winner=1` and `correct_abstention=0`. This is consistent with the hypothesis that additional structure becomes useful when apparently abundant evidence is dependent on one evidence branch and framing pressure is high.

## Cost of the improvement

The quality gains were expensive. Mean primary usage per case was:

| Mode | Model calls | Input tokens | Output tokens |
|---|---:|---:|---:|
| single-context | 1.000 | 924 | 748 |
| cg-reduced | 1.000 | 1,665 | 636 |
| shared-context-multi-agent | 4.375 | 6,852 | 2,220 |
| cg-full | 9.125 | 12,532 | 5,644 |

Relative to single-context, Full Mode used about **9.1× as many model calls, 13.6× as many input tokens, and 7.5× as many output tokens**. The benchmark therefore supports a selective-use interpretation, not an “always use Full Mode” rule.

Shared-context multi-agent is an important comparator: it matched Full Mode on zero premature winners and perfect correct abstention in the two keyed-insufficient cases while using roughly half as many calls. Full Mode nevertheless had higher mean action quality (1.875 vs 1.625), better calibration Brier in this small add-on (0.007 vs 0.027), and higher next-test quality (1.500 vs 1.250). With only eight cases and one repeat, these differences are descriptive rather than statistically established.

## A result that prevents a simplistic “Full Mode wins” claim

The blind semantic metrics and the declared status token do not tell exactly the same story. Declared-status match against the hidden key was:

- single-context: **6/8**;
- `cg-full`: **5/8**;
- shared-context multi-agent: **5/8**;
- `cg-reduced`: **4/8**.

In particular, `cg-full` declared `INSUFFICIENT` on M06 and M07, where the frozen key expected `COEXIST`. Some answers nevertheless represented the required decision-relevant mechanisms and actions well enough to score strongly on the frozen semantic metrics. This exposes a limitation in the current metric set: it has explicit premature-winner and abstention metrics, but no single direct semantic **causal-structure correctness** metric covering every `CHOOSE / COEXIST / INSUFFICIENT` error mode.

The correct conclusion is therefore narrower: **in this 8-case set, Full Mode had no observed unsupported winner selections and produced the strongest actions, but it did not dominate every structural or efficiency diagnostic.** The status-mismatch pattern should be treated as a target for the next benchmark revision rather than hidden by the aggregate.

## Calibration and output compliance

Mean Brier scores were very low for all modes: 0.004 single-context, 0.007 `cg-full`, 0.015 `cg-reduced`, and 0.027 shared-context. The protocol already warns that this is a small set of correlated binary claims, so these values should not support a standalone calibration claim.

Normalization was invoked frequently: 5/8 Full, 5/8 single-context, 7/8 Reduced, and 7/8 shared-context runs required the frozen mechanical repair that clears a non-null `preferred_cause` under `COEXIST` or `INSUFFICIENT`. The later M04–M07 blind re-audit confirmed that this can be semantically material rather than purely cosmetic: N1 was applied in 15/16 inspected runs, and the judges often treated the raw-vs-normalized difference as changing winner-like interpretation. Because N1 was frozen before the main study and applied treatment-independently, using the normalized artifact is procedurally valid; nevertheless raw-versus-normalized disagreement is now an explicit interpretive limitation rather than a future-only concern.

The more complex workflows also incurred transport retries during primary execution: 6 total for `cg-full`, 3 for shared-context, and none for single-context or Reduced. The final standalone no-prompt-cache runtime completed every frozen run, but runtime complexity is part of the practical cost of the multi-call workflows.

## What this benchmark does and does not establish

This result is useful evidence for an **applicability map**, not a universal model ranking. In this 8-case set, the structured multi-stage modes showed fewer observed premature winner selections on the most adversarially ambiguous case than single-context and Reduced Mode, while their extra cost was often unnecessary on simpler cases. Some of that observed benefit may come from multi-pass analysis generally rather than from CG-specific isolation alone, because shared-context multi-agent performed strongly on several primary metrics.

The study does **not** establish general superiority of Convergence Guard. Important limitations are: one local model; eight authored cases; one repeat per cell; one blind semantic judgment per answer rather than replicated inter-rater judging; high normalization rates; and a metric gap around full causal-structure correctness. No significance test or broad population claim is justified from this dataset.

The next evidence-producing step, if pursued, should be a replication on a different model/runtime and/or a small targeted re-test of the cases where the modes diverged most, rather than mechanically expanding this same 32-run matrix.
