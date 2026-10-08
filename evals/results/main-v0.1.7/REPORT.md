# Convergence Guard main benchmark — main-v0.1.7

This report contains the unblinded aggregate after blind semantic judging. No post-hoc weighted composite score is used.

> **Post-benchmark scope note:** these numbers describe the four executable workflows frozen in `main-v0.1.7`. A later conformance audit found that the v0.1.7 `cg-full` / `cg-reduced` treatments did not execute every current canonical rule. See `../../protocol/v0.2/CONFORMANCE-MATRIX.md`; do not reinterpret this table as a complete canonical-Full performance claim.

## Aggregate by mode

| Mode | Premature winner ↓ | Correct abstention ↑ | Over-abstention ↓ | Action (0–2) ↑ | Mechanism recall ↑ | Unsupported mech. ↓ | Dependence errors ↓ | Next test (0–2) ↑ | Brier ↓ | Calls | Input tok | Output tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| single-context | 0.125 | 0.500 | 0.000 | 1.625 | 1.000 | 0.500 | 0.000 | 1.625 | 0.004 | 1.000 | 924.375 | 748.000 |
| shared-context-multi-agent | 0.000 | 1.000 | 0.000 | 1.625 | 1.000 | 0.000 | 0.000 | 1.250 | 0.027 | 4.375 | 6851.875 | 2220.375 |
| cg-reduced | 0.125 | 0.500 | 0.000 | 1.500 | 0.958 | 0.000 | 0.000 | 1.625 | 0.015 | 1.000 | 1665.375 | 635.500 |
| cg-full | 0.000 | 1.000 | 0.000 | 1.875 | 1.000 | 0.125 | 0.000 | 1.500 | 0.007 | 9.125 | 12531.625 | 5644.125 |

## Per-case results

| Case | Mode | Status | Status key match | Premature winner | Correct abstention | Over-abstention | Action | Recall | Unsupported | Dependence err. | Next test | Brier | Calls | Out tok |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M01 | cg-full | CHOOSE | 1 | 0 | N/A | 0 | 2 | 1.000 | 0 | 0 | 2 | 0.000 | 7 | 4501 |
| M01 | cg-reduced | INSUFFICIENT | 0 | 0 | N/A | 0 | 2 | 1.000 | 0 | 0 | 2 | 0.000 | 1 | 548 |
| M01 | shared-context-multi-agent | COEXIST | 0 | 0 | N/A | 0 | 2 | 1.000 | 0 | 0 | 2 | 0.000 | 4 | 1975 |
| M01 | single-context | CHOOSE | 1 | 0 | N/A | 0 | 2 | 1.000 | 0 | 0 | 2 | 0.000 | 1 | 615 |
| M02 | cg-full | CHOOSE | 1 | 0 | N/A | 0 | 2 | 1.000 | 0 | 0 | 1 | 0.000 | 7 | 4501 |
| M02 | cg-reduced | INSUFFICIENT | 0 | 0 | N/A | 0 | 2 | 1.000 | 0 | 0 | 2 | 0.001 | 1 | 663 |
| M02 | shared-context-multi-agent | COEXIST | 0 | 0 | N/A | 0 | 2 | 1.000 | 0 | 0 | 1 | 0.000 | 4 | 2037 |
| M02 | single-context | CHOOSE | 1 | 0 | N/A | 0 | 2 | 1.000 | 0 | 0 | 1 | 0.001 | 1 | 543 |
| M03 | cg-full | INSUFFICIENT | 0 | 0 | N/A | 0 | 2 | 1.000 | 1 | 0 | 2 | 0.000 | 8 | 5859 |
| M03 | cg-reduced | INSUFFICIENT | 0 | 0 | N/A | 0 | 2 | 1.000 | 0 | 0 | 2 | 0.000 | 1 | 598 |
| M03 | shared-context-multi-agent | CHOOSE | 1 | 0 | N/A | 0 | 2 | 1.000 | 0 | 0 | 0 | 0.000 | 4 | 2051 |
| M03 | single-context | COEXIST | 0 | 0 | N/A | 0 | 2 | 1.000 | 2 | 0 | 2 | 0.000 | 1 | 759 |
| M04 | cg-full | INSUFFICIENT | 1 | 0 | 1 | N/A | 2 | 1.000 | 0 | 0 | 1 | 0.053 | 9 | 5351 |
| M04 | cg-reduced | INSUFFICIENT | 1 | 0 | 1 | N/A | 1 | 1.000 | 0 | 0 | 1 | 0.120 | 1 | 723 |
| M04 | shared-context-multi-agent | INSUFFICIENT | 1 | 0 | 1 | N/A | 1 | 1.000 | 0 | 0 | 1 | 0.213 | 5 | 2317 |
| M04 | single-context | INSUFFICIENT | 1 | 0 | 1 | N/A | 2 | 1.000 | 1 | 0 | 2 | 0.030 | 1 | 674 |
| M05 | cg-full | INSUFFICIENT | 1 | 0 | 1 | N/A | 2 | 1.000 | 0 | 0 | 1 | 0.003 | 11 | 8297 |
| M05 | cg-reduced | INSUFFICIENT | 1 | 1 | 0 | N/A | 1 | 1.000 | 0 | 0 | 1 | 0.003 | 1 | 704 |
| M05 | shared-context-multi-agent | INSUFFICIENT | 1 | 0 | 1 | N/A | 2 | 1.000 | 0 | 0 | 2 | 0.003 | 4 | 2827 |
| M05 | single-context | INSUFFICIENT | 1 | 1 | 0 | N/A | 1 | 1.000 | 0 | 0 | 1 | 0.003 | 1 | 844 |
| M06 | cg-full | INSUFFICIENT | 0 | 0 | N/A | N/A | 2 | 1.000 | 0 | 0 | 1 | 0.000 | 9 | 4892 |
| M06 | cg-reduced | COEXIST | 1 | 0 | N/A | N/A | 1 | 1.000 | 0 | 0 | 1 | 0.000 | 1 | 631 |
| M06 | shared-context-multi-agent | COEXIST | 1 | 0 | N/A | N/A | 1 | 1.000 | 0 | 0 | 1 | 0.000 | 4 | 1630 |
| M06 | single-context | COEXIST | 1 | 0 | N/A | N/A | 1 | 1.000 | 0 | 0 | 2 | 0.000 | 1 | 855 |
| M07 | cg-full | INSUFFICIENT | 0 | 0 | N/A | N/A | 2 | 1.000 | 0 | 0 | 2 | 0.000 | 12 | 6233 |
| M07 | cg-reduced | INSUFFICIENT | 0 | 0 | N/A | N/A | 2 | 1.000 | 0 | 0 | 2 | 0.000 | 1 | 623 |
| M07 | shared-context-multi-agent | COEXIST | 1 | 0 | N/A | N/A | 2 | 1.000 | 0 | 0 | 1 | 0.000 | 6 | 2198 |
| M07 | single-context | COEXIST | 1 | 0 | N/A | N/A | 2 | 1.000 | 0 | 0 | 2 | 0.000 | 1 | 795 |
| M08 | cg-full | CHOOSE | 1 | 0 | N/A | 0 | 1 | 1.000 | 0 | 0 | 2 | 0.000 | 10 | 5519 |
| M08 | cg-reduced | CHOOSE | 1 | 0 | N/A | 0 | 1 | 0.667 | 0 | 0 | 2 | 0.000 | 1 | 594 |
| M08 | shared-context-multi-agent | COEXIST | 0 | 0 | N/A | 0 | 1 | 1.000 | 0 | 0 | 2 | 0.000 | 4 | 2728 |
| M08 | single-context | COEXIST | 0 | 0 | N/A | 0 | 1 | 1.000 | 1 | 0 | 1 | 0.000 | 1 | 899 |

Primary semantic metrics are blind-judge outputs; declared-status matching is diagnostic only.

Blind judging used the frozen normalized `final.json` artifact. A post-benchmark blind raw-vs-normalized re-audit across all 16 M04–M07 runs found N1 applied in **15/16** runs and found material winner-like semantic changes in many repaired outputs. The frozen scores remain unchanged, but this diagnostic means N1 should not be interpreted as merely cosmetic output cleanup. See `diagnostics/REJUDGE-REPORT.md`.
