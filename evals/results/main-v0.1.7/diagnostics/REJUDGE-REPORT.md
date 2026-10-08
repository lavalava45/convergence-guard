# Blind raw-vs-normalized re-judging — main-v0.1.7

This is a post-benchmark diagnostic layer. It does **not** replace or modify the frozen main-v0.1.7 scores.

Two independent judges scored all 16 M04–M07 neutral packets while blind to treatment mode. Each judge saw the public case, the frozen hidden key, and the raw/normalized participant answers side-by-side. The mode mapping below was joined only after both score sets were saved.

## Inter-rater agreement

| Field | Agreement |
|---|---:|
| `raw.causal_structure_correct` | 15/16 (93.8%) |
| `raw.premature_winner` | 16/16 (100.0%) |
| `raw.winner_like_signal` | 16/16 (100.0%) |
| `normalized.causal_structure_correct` | 15/16 (93.8%) |
| `normalized.premature_winner` | 15/16 (93.8%) |
| `normalized.winner_like_signal` | 14/16 (87.5%) |
| `normalization.materially_changes_semantic_judgment` | 15/16 (93.8%) |
| `normalization.direction` | 15/16 (93.8%) |

Total field-level disagreements: **7**. No tie-breaking adjudication is silently substituted; a consensus value is reported only where both judges agree.

## Unanimous diagnostics after unblinding

Counts below use only judge-agreed cells; `rated` can therefore be < n when judges disagree.

| Mode | n | Raw structure correct | Norm structure correct | Raw premature winner | Norm premature winner | Raw winner-like signal | Norm winner-like signal | Material N1 effect |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| cg-full | 4 | 3/3 (+1 disagree) | 3/3 (+1 disagree) | 3/4 | 0/4 | 3/4 | 2/3 (+1 disagree) | 3/4 |
| cg-reduced | 4 | 4/4 | 4/4 | 3/4 | 0/3 (+1 disagree) | 3/4 | 2/4 | 2/3 (+1 disagree) |
| shared-context-multi-agent | 4 | 4/4 | 4/4 | 2/4 | 0/4 | 2/4 | 2/4 | 2/4 |
| single-context | 4 | 4/4 | 4/4 | 2/4 | 1/4 | 3/4 | 2/3 (+1 disagree) | 1/4 |

## Interpretation rule

The deterministic N1 audit answers *whether a non-null preferred cause was deleted*. This re-judge answers the different semantic question: *did that deletion change the causal interpretation a blind evaluator would assign?* Because this is a diagnostic re-analysis of an existing small dataset, it is descriptive and should not be presented as a new performance benchmark.

## Disagreements

- `R0004` `raw.causal_structure_correct`: judge A=1, judge B=0
- `R0004` `normalized.causal_structure_correct`: judge A=1, judge B=0
- `R0009` `normalized.premature_winner`: judge A=0, judge B=1
- `R0009` `normalization.materially_changes_semantic_judgment`: judge A=1, judge B=0
- `R0009` `normalization.direction`: judge A='IMPROVES', judge B='NEUTRAL'
- `R0021` `normalized.winner_like_signal`: judge A=1, judge B=0
- `R0022` `normalized.winner_like_signal`: judge A=1, judge B=0
