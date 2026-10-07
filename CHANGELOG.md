# Changelog

[Русская версия](CHANGELOG.ru.md)

## Unreleased

- added a benchmark-informed selective activation triage to the canonical skill: prefer ordinary analysis for directly resolved, cheap-to-check, reversible cases; reserve Full Mode mainly for remaining causal ambiguity where evidence dependence, framing/open-world risk, hard-to-separate confounding/interaction, or costly irreversible commitment justify the overhead;
- hardened Full Mode stage boundaries after a post-benchmark audit: explicit C3 boundary-critic allowlist, removal of the ambiguous labeled "outside alternative" from D2, explicit routing for premortem/stakeholder findings, and a complete D3 second-opinion input/disposition/reconciliation contract;
- separated causal-structure judgment from action sufficiency explicitly, so a supported `COEXISTING`/`INTERACTING` model judgment is not overwritten by `INSUFFICIENT DATA TO CHOOSE` for the action decision;
- qualified benchmark claims to state that blind semantic scores use the predeclared normalized artifacts; raw M04/M05 Full outputs still contained non-null `preferred_cause` values that frozen rule N1 cleared before judging;
- refreshed the applicability guide from pilot-era hypotheses to the completed `main-v0.1.7` evidence and added historical-status notes to the original 64-run planning documents;
- completed the frozen `main-v0.1.7` comparative benchmark: 8 cases × 4 modes × 1 repeat = 32 primary runs, followed by 32/32 calibration completions and blind semantic judging under neutral answer IDs;
- added machine-readable and human-readable main-study results under `evals/results/main-v0.1.7/`, including paired English/Russian interpretation and explicit resource-cost, calibration, normalization, and metric-limit caveats;
- documented the final dedicated `llama-server 2.52.0` no-prompt-cache runtime used to complete the frozen study after earlier LM Studio-managed transport/cache failures;
- added paired English/Russian applicability guidance with task classes, a quick activation test, and explicit examples of when CG may be excessive versus useful;
- documented the two-case automated local technical pilot, including the P01 over-analysis/over-abstention signal and the P02 underdetermination result;
- added deterministic output normalization v0.1 for mechanically inconsistent non-choice `preferred_cause` fields, with raw-answer preservation and repair auditing;
- tightened the installable skill description and clarified that a complete installation includes the operational `references/` package;
- added API/fresh-request guidance for constructing isolation-dependent workers without inherited session state;
- allowed a single genuine finalist after coverage/missing-evidence checks, while retaining dossier, sensitivity, and shared-bias review and skipping pairwise collision only;
- added explicit `PENDING` validity for materially revised hypotheses so interrupted/budget-limited reruns cannot inherit obsolete validation;
- added an optional information-probe mini-dossier that remains separate from finalist dossiers and adjudication;
- corrected the evidence-sufficiency gate to require worthwhile, decision-changing checks before commitment;
- added the shared evidence brief and decision contract to the blind mapper's input allowlist;
- defined an explicit no-feasible-discriminator outcome, separate from action sufficiency and deferred checks;
- bounded corrective cycles with a shared run budget and a no-progress stopping rule;
- separated negative isolation smoke tests from runtime-backed boundary assurance, including later retrieval/tool access.

- added a 60-second Quick Start and a concise “Why not just ask 5 agents?” explanation to the README;
- made runtime requirements vendor-neutral and removed implementation-specific runtime profile files from the public repository.
- added a third bilingual Full Mode worked example on long-running autonomous-agent reliability, separating policy-complexity, closed-loop state integrity, and persistent-state/coordination mechanisms and deriving a risk-adaptive verification/recovery priority under causal uncertainty.

## v0.2.2 — pre-release

- added DESIGN.md / DESIGN.ru.md with a first-principles threat model and architectural rationale;
- documented threat-to-control traceability, residual risks, rejected design alternatives, and open evaluation questions.
- added a claim-level source-quality policy: source reputation guides verification priority but never substitutes for provenance, inspectability, evidence ancestry, contradiction handling, or replication;
- distinguished confirmation of what a document or institution says from confirmation of the underlying proposition;
- added explicit source roles: EVIDENCE, CORROBORATION, CONTEXT, LEAD ONLY, and UNSUPPORTED.
- added a second public Full Mode worked example on SARS-CoV-2 origins, with paired English/Russian versions, source-dependency analysis, inaccessible-evidence handling, and separate model/evidence-sufficiency judgments;
- added an explicit scope disclaimer for public examples: worked runs demonstrate the protocol and do not substitute for laboratory, forensic, criminal, intelligence, legal, or other domain-specific primary investigations.
- synchronized current public documentation and installable skill metadata to v0.2.2.

## v0.2.1 — pre-release

- tightened Full Mode context-boundary requirements;
- added an explicit runtime isolation preflight and recovery rules;
- clarified that worker agreement is not evidential independence;
- retained the three-worker adaptive search cohort and blind Phase C reduction;
- added paired English/Russian human-facing documentation;
- added the first public Full Mode worked example: the Jack the Ripper identification case;
- synchronized public documentation to v0.2.1.
