# main-v0.1.7 normalization diagnostics: M04–M07

This is a post-benchmark diagnostic audit. It compares frozen `final.raw.json` with the frozen normalized `final.json`; it does not alter or recompute the published benchmark scores.

`n1_semantic_change_flag=1` means N1 removed a non-null `preferred_cause` value. The flag marks a causal-content deletion for neutral re-judging; it is not itself a judgment that any frozen semantic score was wrong.

Runs audited: **16**. N1 applied: **15**. N1 semantic-change flags: **15**.

| Neutral ID | Case | Mode | Raw status | Raw preferred cause | Normalized preferred cause | N1 | Semantic flag | Only N1 path changed |
|---|---|---|---|---|---|---:|---:|---:|
| R0002 | M04 | shared-context-multi-agent | INSUFFICIENT | producer_retry_or_broker_redelivery_gap | `null` | 1 | 1 | 1 |
| R0004 | M05 | cg-full | INSUFFICIENT | H08 (with caveats on label reliability) | `null` | 1 | 1 | 1 |
| R0006 | M07 | cg-full | INSUFFICIENT | H01 | `null` | 1 | 1 | 1 |
| R0007 | M06 | cg-reduced | COEXIST | Dual independent failures: A refrigerant leak in Cluster A and a mechanical damper bi... | `null` | 1 | 1 | 1 |
| R0009 | M04 | cg-reduced | INSUFFICIENT | C1 (Producer-initiated retries exceeding deduplication TTL) | `null` | 1 | 1 | 1 |
| R0015 | M07 | shared-context-multi-agent | COEXIST | proxy_firmware_7_4 | `null` | 1 | 1 | 1 |
| R0016 | M06 | cg-full | INSUFFICIENT | H01 | `null` | 1 | 1 | 1 |
| R0018 | M07 | single-context | COEXIST | proxy_firmware_7.4_bug_triggered_by_client_5.0_feature_change | `null` | 1 | 1 | 1 |
| R0019 | M05 | cg-reduced | INSUFFICIENT | C2 (High Probability / Structural Interaction) | `null` | 1 | 1 | 1 |
| R0021 | M04 | cg-full | INSUFFICIENT | H01 | `null` | 1 | 1 | 1 |
| R0022 | M04 | single-context | INSUFFICIENT | C1 (High Probability, Low Certainty of Mechanism) | `null` | 1 | 1 | 1 |
| R0023 | M07 | cg-reduced | INSUFFICIENT | C1 (Proxy firmware 7.4 buffer handling error for zstd streams > 8 MiB) | `null` | 1 | 1 | 1 |
| R0025 | M05 | single-context | INSUFFICIENT | `null` | `null` | 0 | 0 | 0 |
| R0027 | M05 | shared-context-multi-agent | INSUFFICIENT | SDK_DATA_DRIFT_INTERACTION_WITH_R91_LABELING_LOGIC_UNCERTAIN_DUE_TO_MISSING_TRACES_AN... | `null` | 1 | 1 | 1 |
| R0030 | M06 | shared-context-multi-agent | COEXIST | CA_01 | `null` | 1 | 1 | 1 |
| R0032 | M06 | single-context | COEXIST | COEXISTENT_FAILURES_IN_DISTINCT_SYSTEMS_OR_COMPONENTS_AFFECTING_TWO_CLUSTERS_SEPARATE... | `null` | 1 | 1 | 1 |

Neutral packet files are under `rejudge-packets/`. They include the public case material and the raw/normalized artifacts, but omit mode, run ID, resource use and frozen judge scores.
