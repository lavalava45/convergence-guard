# Attribution

[Русская версия](ATTRIBUTION.ru.md)

Early versions of this protocol were inspired by Udit Akhouri's ADHD divergent-ideation skill. The current method substantially redesigns the workflow around causal models, information isolation, adversarial comparison, assumption stress-testing, and falsifiable convergence.

Historical inspiration: https://github.com/UditAkhourii/adhd

The current protocol is independently maintained and has diverged substantially in architecture, candidate selection, causal testing, and convergence behavior. This attribution is intentionally retained for transparency about the project's origin.

## Influence boundary

The historical ADHD skill contributed a high-level design intuition: widen the search before committing, use isolated parallel branches, and keep generation from being immediately strangled by evaluation.

Convergence Guard does **not** retain ADHD's cognitive-frame library, novelty/viability/fit scoring, weighted ranking, fixed five-branch fan-out, JSON idea-generator prompts, wildcard-frame mechanism, or fixed top-three focus loop.

Convergence Guard independently develops a different problem definition and protocol around:

- evidence provenance and explicit unknowns;
- decision contracts and loss/reversibility;
- causally distinct search mandates rather than cognitive personas;
- causal mechanisms, predictions, and identification threats;
- strict context allowlists and runtime isolation preflight;
- parallel blind screening and causal mapping;
- explicit EXCLUSIVE / COEXISTING / NESTED / INTERACTING relations;
- conditional boundary criticism;
- independent finalist dossiers;
- assumption sensitivity and shared-bias audits;
- pairwise decision collision;
- conditional second opinion;
- an evidence-sufficiency gate;
- a minimum decision-changing observation or experiment;
- an explicitly disclosed Reduced Mode and failure-recovery rules.

For reproducibility, the upstream ADHD `SKILL.md` used as the historical comparison point is commit `55ed38514cd996f6096b51c8320331a8a5dced19` (2026-06-04). That file remained unchanged upstream through the start of Convergence Guard development in September 2026.
