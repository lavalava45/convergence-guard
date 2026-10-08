# Canonical rule → executable harness conformance

This matrix was added after the review of `main-v0.1.7` found that the published workflow benchmark exercised **simplified implementations**, not every conditional rule in the canonical Convergence Guard specification.

The frozen v0.1.7 result is not rewritten. Its historical code remains recoverable at the frozen commit. The purpose of this matrix is to prevent a future harness from being labeled “Full Mode complete” merely because it contains stages with familiar names.

Machine-readable source: [`CONFORMANCE-MATRIX.json`](CONFORMANCE-MATRIX.json).

## Status meaning

- **FULL** — executable behavior and an auditable artifact exist.
- **PARTIAL** — some behavior exists, but the canonical rule is incomplete or depends on a caller-supplied guarantee.
- **MISSING** — v0.1.7 could omit the rule without marking the run incomplete.
- **FAIL_CLOSED** — v0.2 still lacks full execution of that branch, but a triggered/unresolved condition must make the protocol `PARTIAL_PROTOCOL`/`BUDGET_STOP`; it cannot silently masquerade as complete.

## High-value gaps exposed by the review

| Canonical rule | Frozen v0.1.7 | Post-benchmark v0.2 target | Evidence / consequence |
|---|---|---|---|
| B2 coverage gate | **MISSING** | **FULL** | v0.1.7 jumped from the first three search outputs directly to neutralization. v0.2 emits `B2-coverage.json` and, when triggered, one or two isolated expansion-search artifacts. |
| C3 boundary critic | **MISSING** | **FULL** | v0.1.7 could record `boundary_critic_needed=true` and still go directly to finalist selection. v0.2 requires `C3-boundary.json` whenever C2 triggers it. |
| C4 zero-finalist path | **PARTIAL** | **FULL** | v0.1.7 `choose_finalists()` had a pilot fail-soft that promoted the first non-FAIL candidate if the real filters produced none. v0.2 explicitly allows zero finalists and forbids padding. |
| C4 selection semantics | **PARTIAL** | **FULL** | v0.1.7 hard-coded a hidden support/completeness/discriminability hierarchy. v0.2 uses an explicit C4 artifact with exclusions and checkpoint decision. |
| D1 material revision | **MISSING** | **FULL** | v0.1.7 had no new-ID/PENDING reroute. v0.2 creates a new ID, records the mapping, and reruns affected C/D stages within the finite corrective-cycle budget. |
| D2 missing-family reroute | **PARTIAL** | **FULL** | v0.2 exposes `reroute_needed/reason/mandate`, runs targeted isolated search, then reruns affected C/D2 stages. |
| D3 contract | **PARTIAL** | **FULL for review disposition** | v0.2 has neutral inputs and `CONFIRM / QUALIFY / CHALLENGE`; unresolved decision-changing challenges fail closed instead of being settled by confidence wording. |
| Model vs action outcome | **PARTIAL** | **FULL** | v0.2 schema has separate `causal_structure` and `action_decision`; `COEXIST` is no longer forced to become `INSUFFICIENT` just because action choice is unresolved. |
| Next-test absence | **PARTIAL** | **FULL** | v0.2 can say `NO_FEASIBLE_DISCRIMINATOR` or `DEFERRED_FOR_BUDGET`; it no longer has to invent a populated next test. |
| Execution completeness | **MISSING** | **FULL** | v0.2 `protocol_completion` is a harness fact and records completed, skipped, triggered-but-unexecuted, pending, and omitted stages. |
| Reduced packet dependency closure | **PARTIAL** | **FULL** | v0.1.7 supplied only `reduced-mode.md` even though it referred to detailed external rules. v0.2 uses `REDUCED-SELF-CONTAINED-PACKET.md`; no inaccessible reference is needed to execute the requested discipline. |

## Remaining fail-closed items

The first v0.2 implementation deliberately does **not** claim perfect canonical conformance yet. Optional premortem/stakeholder execution, an optional probe mini-dossier, and full upstream rerouting of a D3 challenge remain implementation targets. Their absence is now visible: if one is materially required, the run may not be reported as protocol-complete.

This is an intentional improvement over v0.1.7: **unsupported behavior becomes an auditable partial execution instead of an invisible approximation.**

## Acceptance checklist before any future “canonical Full Mode” benchmark

1. Every mandatory rule has status `FULL`.
2. Every conditional rule has either an executable triggered path or a testable `FAIL_CLOSED` path that prevents a `COMPLETE` label.
3. Unit tests force B2, C3, zero-finalist, D1 revision, D2 reroute, D3 challenge, no-discriminator, and budget-stop branches.
4. Every isolation-dependent role has an explicit input allowlist and a persisted request artifact proving it.
5. Reduced participant instructions are self-contained under the runtime's actual access boundary.
6. Final output separates causal structure, action decision, next-test status, and protocol completion.
7. Raw and normalized artifacts are both preserved; judging rules state which one is scored and raw winner-like signals are measured separately.
8. A conformance check runs before scoring and can invalidate the “canonical Full” label independently of answer quality.

Until items 1–3 are satisfied for all canonical branches, v0.2 should be described as a **conformance-corrected implementation target**, not as a newly validated Full Mode performance result.
