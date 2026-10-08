# Isolation ablation v0.1.4 — интерпретация

Это интерпретационный слой для замороженного targeted isolation experiment. Машиночитаемый результат находится в `summary.json`, таблица two-judge consensus — в `REPORT.md`.

> **Presentation erratum:** frozen report generator содержит только ошибку в заголовке и пишет `Isolation ablation v0.1.2` в начале `REPORT.md`. Машиночитаемый `summary.json`, run plan, freeze manifest, result directory и все participant/judge artifacts однозначно относятся к валидному study `isolation-ablation-v0.1.4`. Опечатка не влияет ни на одну metric или mapping и намеренно оставлена в generated report, чтобы он оставался byte-reproducible из frozen aggregator.

## Зачем понадобился этот эксперимент

Завершённый `main-v0.1.7` сравнивал четыре workflow, но post-benchmark conformance audit обнаружил, что executable treatments `cg-full` и `cg-reduced` были упрощёнными реализациями, а не точным исполнением всех правил canonical Convergence Guard. Поэтому main study не способен чисто ответить на более узкий вопрос: **даёт ли сама context isolation дополнительную защиту от anchoring, если остальной workflow оставить одинаковым?**

`isolation-ablation-v0.1.4` был создан именно для этого вопроса.

## Дизайн

Четыре уже замороженных case (`M02`, `M03`, `M04`, `M06`) запускались в 2×2 design:

- isolated search против shared-history search;
- neutral prior history против уверенного, но неправильного по hidden key prior conclusion.

Во всех cells были одинаковыми public evidence, model, три search mandate, четыре logical model calls, temperature, token ceilings, paired stage seeds и neutral synthesizer. Финальный synthesizer никогда не видел injected history напрямую.

В isolated cells три search workers не видели ни parent history, ни outputs соседних workers. В shared cells видели. Поэтому этот эксперимент меняет один механизм значительно чище, чем исходный main workflow benchmark.

После нескольких прозрачно задокументированных abort, связанных только с execution plumbing, валидная replacement-версия `v0.1.4` завершила **16/16 cells** на замороженном standalone endpoint `http://127.0.0.1:55991/v1`. Все **64/64 сохранённых model responses** указывают именно этот endpoint. Четыре transient transport failure потребовали второго same-request attempt; ни одна cell не стала invalid.

## Проверка самой манипуляции

Isolation прошла наиболее сильную механическую проверку.

Для каждого case пары `isolated-neutral` и `isolated-false-anchor` имели byte-identical model-visible search prompts, одинаковые paired seeds и byte-identical search outputs. Поскольку final synthesizer получал те же search outputs, финальные isolated outputs внутри каждого case также совпали.

То есть injected history действительно отсутствовала в isolated treatment path.

## Результат

Эксперимент **не показал преимущества isolation** на этих четырёх cases.

Сначала два независимых blind judge оценили causal structure, premature winner, over-abstention, action quality и next-test quality, не зная isolation condition, history condition, run IDs, anchors или resource use. Только после заморозки этих scores два независимых anchor judge получили false-anchor packets.

Оба anchor judge одинаково оценили все восемь false-anchor cells:

> **false-anchor adoption = 0/8**

Shared workers напрямую видели ложный prior conclusion, но ни один финальный answer не принял его содержательно как причинного winner или привилегированное объяснение.

Primary quality metrics также не показывают ухудшения из-за false anchor:

| Condition | Structure correct ↑ | Premature winner ↓ | Action quality ↑ | Next-test quality ↑ | False-anchor adoption ↓ |
|---|---:|---:|---:|---:|---:|
| isolated-neutral | 0.750 (4/4 rated) | 0.250 | 1.750 | 0.750 | N/A |
| isolated-false-anchor | 0.750 (4/4) | 0.250 | 1.750 | 0.750 | 0.000 |
| shared-neutral | 0.667 (3/4; 1 judge disagreement) | 0.250 | 1.750 | 1.000 (3/4 rated) | N/A |
| shared-false-anchor | 1.000 (4/4) | 0.000 | 1.750 | 0.333 (3/4 rated) | 0.000 |

Три field-level расхождения между blind judges оставлены видимыми; мы не подменяли их post-hoc adjudication.

Визуально лучшие цифры shared-false-anchor по structure/premature-winner **нельзя** интерпретировать как доказательство, что ложный anchor помогает. При четырёх authored cases, одном run на cell и нескольких judge disagreements это описательная idiosyncrasy/noise, пока эффект не replicated.

## Что это означает

Теперь у одного из design claims Convergence Guard более точный evidential status.

У нас есть прямое evidence, что реализованная isolation boundary действительно не пропускает скрытый parent history в search workers: paired isolated artifacts показывают это механически.

Но у нас **пока нет evidence, что такая isolation улучшает качество ответа** при протестированной contamination. Shared workflow самостоятельно устоял против ложных anchors.

Поэтому корректный claim теперь такой:

> **Isolation — реально работающий information-boundary control с правдоподобным threat model, но его incremental quality benefit не был продемонстрирован этим четырёх-case false-anchor ablation.**

Это не означает, что isolation бесполезен. Эксперимент отвечает только за конкретно протестированную manipulation.

## Важное ограничение anchor manipulation

Shared-history prompt явно помечал inherited conclusion как **“NOT EVIDENCE”** и требовал перепроверять его по supplied evidence и не считать peer agreement независимой corroboration. Это хорошая аналитическая дисциплина, но одновременно такой текст сам является anti-anchoring warning.

Поэтому experiment проверял дополнительную пользу isolation **поверх уже явной anti-anchor инструкции**. Нулевая adoption rate может означать, что для этой модели и этих cases одной инструкции уже хватало, и isolation просто не оставалось что улучшать по измеряемым outcomes.

Если понадобится более сильный future test, contamination должна быть реалистичнее, но всё равно заранее заморожена: например, правдоподобное inherited intermediate reasoning без ярлыка «не evidence», повторяющийся peer consensus с общим ancestry или длинная multi-step цепочка, где ранний framing влияет на то, какие evidence вообще будут рассмотрены. Из текущего результата такой эффект выводить нельзя.

## Связь с main benchmark

Main benchmark остаётся полезным как описательное сравнение четырёх **реально реализованных workflows**, но post-benchmark audit требует более узкой формулировки:

- он не валидировал каждую conditional branch canonical Full Mode;
- Reduced packet v0.1.7 не был полностью self-contained относительно всех правил, на которые ссылался;
- normalization материально меняла winner-like causal content во многих raw outputs M04–M07;
- shared-context multi-agent уже показывал сильный результат по premature-winner/abstention metrics;
- targeted ablation не обнаружил дополнительной answer-quality защиты от isolation при протестированном false-anchor manipulation.

Correction layer v0.2 закрывает specification/execution gaps: conformance matrix, self-contained Reduced packet, раздельные causal/action/protocol-completion поля, fail-closed conditional stages и raw-vs-normalized diagnostics. Эти изменения — инфраструктурные исправления, а не заднее переписывание frozen scores `main-v0.1.7`.

## Итог

Сейчас evidence поддерживает три утверждения разной силы:

1. **Structured multi-pass analysis выглядел полезным на части сложных cases исходного workflow benchmark.** Это описательный результат, а не causal effect canonical Full.
2. **Isolation boundary механически работает.** Paired isolated artifacts доказывают, что hidden history не попадала в эти search contexts.
3. **Incremental quality benefit isolation всё ещё не доказан.** В targeted 16-cell experiment false-anchor adoption не возникла даже без isolation.

Это и есть текущая честная граница доказательств.
