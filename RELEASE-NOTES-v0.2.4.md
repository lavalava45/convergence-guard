# Convergence Guard v0.2.4 — Evidence-Graded Applicability Research Preview

**Research prerelease · 8 October 2026 · English / Русский**

This release adds a structured map of where Convergence Guard (CG) might help, **with each claim labeled by its evidence level**. The aim is not to broaden performance claims beyond what the experiments actually measured.

## What is new since v0.2.3

- **[Applicability Evidence Map — English](convergence-guard/references/applicability-evidence-map.md) / [русская карта](convergence-guard/references/applicability-evidence-map.ru.md):** 8 locally observed causal-case regimes, 12 cross-domain application contexts, clearly labeled transfer hypotheses, unconfirmed claims, and an escalation ladder.
- README and the [Applicability Guide](convergence-guard/references/applicability.md) / [руководство](convergence-guard/references/applicability.ru.md) now link to the evidence map.
- Reproducibility limits of the public archive are explicit in [evals/README.md](evals/README.md#reproducibility-boundary).
- Skill metadata and current reference headings are synchronized to `v0.2.4`. **No change to the causal algorithm, no new participant-model experiments, and no retrospective alteration of frozen study results.**

## Existing evidence carried forward unchanged

| Study | Result | What not to infer |
|---|---|---|
| [Main implemented-workflow benchmark `main-v0.1.7`](evals/results/main-v0.1.7/INTERPRETATION.md) | 8 authored cases × 4 modes = 32 primary completions, 32 calibrations. `cg-full` and shared-context multi-agent each had 0/8 **normalized** premature winners; single-context and implemented Reduced each had 1/8. Full action quality averaged 1.875/2 versus 1.625/2 for single/shared, at 9.125 model calls per case versus 1/4.375. | Not evidence that canonical Full CG wins. The tested Full/Reduced workflows did not implement every canonical conditional branch, and shared multi-agent performed strongly at lower cost. |
| [Raw/normalized re-audit](evals/results/main-v0.1.7/diagnostics/REJUDGE-REPORT.md) | Frozen N1 normalization applied in 15/16 M04–M07 runs; two blind judges often found that normalization materially changed causal preference interpretation. | Not a harmless formatting-only transformation, nor a justification to rewrite frozen scores. |
| [Isolation ablation `v0.1.4`](evals/results/isolation-ablation-v0.1.4/INTERPRETATION.md) | 16/16 cells (4 cases × 2 isolation × 2 history), 64 model responses, paired prompt integrity PASS; **false-anchor adoption 0/8** according to both independent anchor judges. | The information boundary was demonstrated mechanically **but no incremental answer-quality advantage** was demonstrated. The shared treatment explicitly instructed workers that inherited prior conclusions were `NOT EVIDENCE`. |

All measurements are **descriptive**: one local model, authored text-only cases, one repeat per primary cell. Literal causal-status matching was 5/8 for implemented Full versus 6/8 for single; this is not a universal ranking. The [conformance correction layer](evals/protocol/v0.2/CONFORMANCE-MATRIX.md) is infrastructure, not a new canonical-Full performance result. No cross-model, frontier, compact Structured Core, real-world deployment, or population-wide superiority claim is made.

## Reproducibility and source boundaries

The published repository contains the canonical skill, three bilingual worked examples, public case packets, harness, frozen run plans, study freeze manifests, aggregate summaries, reports, interpretations and conformance materials. The examples (historical attribution, contested scientific origins, autonomous-agent reliability) **demonstrate protocol use**, not primary forensic/scientific/industrial investigations.

Private hidden keys, truth labels, blind mappings, individual judge scores, and some original runtime artifacts are intentionally outside version control. Therefore this release supports **inspection and partial procedural reproduction**, but not a full independent blind rejudging of published scores using only the public checkout. A third-party replication needs new frozen cases/keys, an identifiable model/runtime, explicit baseline workflows and independent judging. See [evaluation reproducibility limits](evals/README.md#reproducibility-boundary) and the [frozen main manifest](evals/FREEZE-MANIFEST-main-v0.1.7.json) / [isolation manifest](evals/FREEZE-MANIFEST-isolation-ablation-v0.1.4.json).

**Known presentation issue:** the frozen isolation `REPORT.md` header says `v0.1.2` although the valid experiment is `v0.1.4`. The documented, heading-only typo was left untouched to preserve the frozen aggregator hash and byte reproducibility; see its [result index](evals/results/isolation-ablation-v0.1.4/README.md).

## Install and explore

Install the **whole** [`convergence-guard/`](convergence-guard/) directory, including `references/`; `SKILL.md` alone is not a complete operational package. Full Mode requires runtime-demonstrable context separation; when that boundary is unavailable, a user-consented and explicitly labeled Reduced Mode is the fallback.

Recommended entry points: [README](README.md), [Applicability Evidence Map](convergence-guard/references/applicability-evidence-map.md), [Design rationale](DESIGN.md), [Jack the Ripper example](examples/jack-the-ripper-full-mode.md), [autonomous agents example](examples/long-running-autonomous-agents-full-mode.md), [SARS-CoV-2 origins example](examples/sars-cov-2-origins-full-mode.md).

---

## Кратко по-русски

**v0.2.4 — исследовательский предварительный релиз.** Добавлена [доказательная карта применимости](convergence-guard/references/applicability-evidence-map.ru.md): восемь сценариев уже проведённого benchmark и двенадцать контекстов потенциального применения с разделением на **локально проверенные наблюдения**, **перспективные гипотезы** и **неподтверждённые утверждения**. Карта не является доказательством межотраслевого превосходства CG.

Сохранены без изменений результаты `main-v0.1.7` (32 основных ответа, 32 калибровки) и `isolation-ablation-v0.1.4` (16 ячеек, 64 вызова). В главном тесте реализованный Full и shared multi-agent получили по **0/8** преждевременных победителей в нормализованном scoring, но Full был значительно дороже. Отдельный эксперимент показал работающую информационную границу, **не обнаружив прироста качества от изоляции** при данной манипуляции. `main-v0.1.7` **не** проверял полную canonical Full v0.2 реализацию. Последующий аудит выявил существенное влияние нормализации `N1` на причинные интерпретации.

Публичные материалы содержат код, исходные кейсы, freeze manifests и итоговые агрегаты, но **не** приватные ключи и индивидуальные оценки судей. Поэтому полное независимое пересуживание опубликованных результатов только по GitHub-репозиторию невозможно. [Ограничения воспроизводимости](evals/README.md#reproducibility-boundary), [русская интерпретация основного исследования](evals/results/main-v0.1.7/INTERPRETATION.ru.md), [русская интерпретация isolation](evals/results/isolation-ablation-v0.1.4/INTERPRETATION.ru.md).

Это выпуск документации и карты доказательств, **не новый сравнительный benchmark**. Следующий обоснованный шаг — заранее зарегистрированные сложные причинные кейсы на другой модели и сравнение с сильным single-context и компактным Structured Core.
