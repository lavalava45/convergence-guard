# Changelog

[Русская версия](CHANGELOG.ru.md)

## Unreleased

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
