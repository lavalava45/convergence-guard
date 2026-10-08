# Convergence Guard — руководство по применимости

Convergence Guard не предназначен для того, чтобы делать любой анализ длиннее. Его ценность должна расти там, где основная опасность — **преждевременная сходимость**: принять одну правдоподобную причинную историю до того, как действительно важные альтернативы были разделены и проверены.

Это руководство разделяет классы задач, где протокол, вероятно, полезен, и задачи, где его накладные расходы могут оказаться контрпродуктивными.

## Статус доказательств

Границы ниже следуют из архитектуры метода, но теперь дополнительно опираются на два descriptive eval layer: замороженный implemented-workflow benchmark `main-v0.1.7` (8 cases × 4 modes × 1 repeat = 32 participant runs) и последующий targeted isolation-ablation на 16 cells. Это **evidence для карты применимости, а не универсальное доказательство превосходства**. Одна модель, authored cases и один repeat на ячейку не дают общего рейтинга для всех задач.

Основной benchmark дал четыре полезных сигнала:

- **В этом 8-case наборе у Full Mode наблюдалось меньше premature winners:** `cg-full` получил 0/8 premature winners; single-context и `cg-reduced` — по 1/8. Это описательный результат, а не causal или population-level effect estimate.
- **Самое сильное различие появилось на deceptive underdetermination:** на M05, где кажущееся изобилие evidence в основном происходило из одной evidence-ветки, Full Mode и shared-context сохранили живые альтернативы, тогда как single-context и Reduced получили от blind judge `premature_winner=1` и `correct_abstention=0`.
- **Простые/разрешимые cases не оправдали цену Full Mode:** на прямых и хорошо разрешимых задачах Full Mode не дал преимущества в качестве решения, соразмерного примерно 9.1 model calls на case против 1 у single-context.
- **Full Mode не является универсальным победителем:** shared-context multi-agent тоже получил 0/8 premature winners при меньшей цене, а Full Mode иногда выдавал чрезмерно осторожный literal status на keyed `COEXIST` cases.
- **Main benchmark не валидировал canonical Full/Reduced execution:** post-benchmark conformance audit нашёл missing/partial conditional branches в executable treatments v0.1.7. Поэтому эти результаты нужно читать как comparison реализованных workflows, а не causal effect полного canonical skill.
- **Incremental quality benefit isolation не был продемонстрирован:** в последующем 4-case × 2-isolation × 2-history ablation isolation boundary прошла mechanical integrity checks, но оба независимых anchor judge дали 0/8 false-anchor adoption по false-anchor cells. Shared treatment тоже устоял против anchors.

Все blind semantic scores выше рассчитаны по frozen normalized participant artifact. Последующий blind raw-vs-normalized re-audit всех 16 runs M04–M07 показал, что N1 сработала в **15/16** runs, а blind judging во многих случаях считал raw-vs-normalized изменение материально значимым для winner-like interpretation. Frozen scores задним числом не меняются, потому что normalization была predeclared и treatment-independent, но diagnostic показывает, что N1 не была просто косметической formatting cleanup. См. [`evals/results/main-v0.1.7/diagnostics/REJUDGE-REPORT.md`](../../evals/results/main-v0.1.7/diagnostics/REJUDGE-REPORT.md).

Поэтому текущая интерпретация такова:

> Convergence Guard наиболее оправдан, когда высоки причинная неоднозначность, framing risk, evidence dependence или цена преждевременного решения. Наличие interaction/`COEXIST` требует явной проверки структуры, но **само по себе** не является причиной переходить к Full Mode. Isolation остаётся разумным information-boundary control, когда contamination risk существенен, но его incremental answer-quality benefit пока не установлен текущим ablation. Для напрямую разрешённых задач Full Mode обычно избыточен, если более дешёвый workflow уже достаточно хорошо разделяет живые причины.

## Классы задач

### 1. Прямо разрешимые

Типичные признаки:

- короткая причинная цепочка;
- ключевой механизм наблюдается напрямую или почти напрямую;
- альтернативы быстро исключаются;
- существует дешёвое и обратимое корректирующее действие;
- расширение пространства гипотез почти не даёт дополнительной ценности.

Пример: deployment меняет одно значение конфигурации, логи показывают возникший DNS failure, а прямой probe подтверждает, что старый target работает, а новый — нет.

**Рекомендуемый режим:** обычный single-context анализ или стандартная диагностическая процедура. Full Mode обычно не нужен.

### 2. Ограниченная неоднозначность

Типичные признаки:

- остаются 2–4 правдоподобных механизма;
- evidence частично различает их;
- одно дополнительное наблюдение или canary может существенно изменить решение;
- преждевременный выбор победителя реально опасен.

**Рекомендуемый режим:** используйте ordinary или более дешёвый structured multi-pass workflow, если он уже достаточно хорошо разделяет живые модели. Full Mode может быть оправдан, когда contamination risk, stakes или auditability requirements делают более сильные information boundaries стоящими overhead, но текущий evidence не показывает, что isolation сама по себе улучшает answer quality в этом классе. Reduced Mode остаётся явным fallback, когда настоящая isolation недоступна и пользователь принимает это ограничение.

### 3. Разрешимые задачи с сильными distractors

Типичные признаки:

- одна причинная модель в итоге поддерживается лучше;
- другая версия очень заметна по времени, интуитивно привлекательна или часто повторяется;
- несколько наблюдений совместимы с обеими версиями;
- решающее свидетельство легко пропустить.

Это один из основных классов задач для Convergence Guard. Benchmark поддерживает ценность structured multi-stage analysis здесь, но не показывает, что canonical Full Mode — или isolation отдельно — всегда лучше более дешёвого multi-pass comparator.

**Рекомендуемый режим:** Full Mode оправдан, когда ошибочное решение заметно дорого **и** более сильные information-boundary/audit controls стоят своей цены. Не заявляйте уже доказанный anti-anchoring performance gain от isolation на основании текущего evidence. Если Full Mode доступен, но избыточен, лучше использовать обычный или более дешёвый multi-pass анализ, а не переименовывать его в Reduced Mode. Reduced Mode остаётся явным fallback, когда настоящая изоляция недоступна и пользователь принимает это ограничение.

### 4. Взаимодействующие или многоуровневые причины

Типичные признаки:

- реальными могут быть несколько причин одновременно;
- один фактор создаёт уязвимость, другой запускает событие;
- два безопасных по отдельности изменения дают сбой только вместе;
- общий предшествующий фактор может заставлять несколько объяснений двигаться синхронно.

Такие задачи плохо описываются принудительным `A OR B`.

**Рекомендуемый режим:** явно моделировать `COEXIST`, interaction, nesting и разные causal roles в любом выбранном workflow. Переходить к Full Mode только когда interaction трудно разделить **и** есть ещё один material risk — например evidence dependence, framing/open-world search risk или дорогой необратимый commitment — который оправдывает сильную isolation. Если isolation недоступна и пользователь принимает ограничение, fallback остаётся Reduced Mode.

### 5. Open-world causal investigation

Типичные признаки:

- пространство релевантных гипотез заранее неизвестно;
- качество и provenance доказательств сильно различаются;
- разные источники могут иметь общее происхождение;
- исходный framing способен исключить важные причинные семьи;
- решающий эксперимент может быть невозможен;
- `INSUFFICIENT DATA TO CHOOSE` может быть правильным конечным результатом.

К этому классу могут относиться историческая атрибуция, спорные вопросы научного происхождения, стратегические расследования и сложные socio-technical failures.

**Рекомендуемый режим:** Full Mode может быть оправдан, если доступна настоящая isolation и stakes/audit requirements оправдывают расходы, особенно когда contamination является material threat. Рассматривайте isolation как threat-model control, а не как уже доказанный performance boost.

## Быстрый тест применимости

Convergence Guard становится более оправданным по мере того, как больше признаков находится в правой колонке:

| Признак | Низкая потребность в CG | Высокая потребность в CG |
|---|---|---|
| Конкурирующие причины | один очевидный механизм | несколько причинно различных живых моделей |
| Разделимость evidence | прямое различающее свидетельство | evidence совместимо с несколькими историями |
| Confounding / interaction | почти отсутствует или легко разделяется | существенно **и трудно разделяется в decision-relevant смысле** |
| Framing risk | низкий | вероятны пропущенные причинные семьи |
| Provenance evidence | прямое и независимое | косвенное, конфликтующее или общего происхождения |
| Проверяемость | есть дешёвый решающий тест | тесты дороги, медленны или неоднозначны |
| Обратимость | ошибку легко исправить | решение создаёт lock-in или большой downside |
| Цена преждевременной сходимости | низкая | высокая |

Если почти все признаки находятся в левой колонке, тяжёлый запуск Convergence Guard, вероятно, не нужен.

## Что поддерживает текущий benchmark

Вместе `main-v0.1.7`, conformance audit, normalization re-audit и targeted isolation-ablation поддерживают пять умеренных выводов:

1. Реализованный Full workflow можно выполнить end-to-end в аудируемом изолированном локальном runtime; в 8-case main set у него наблюдалось меньше unsupported winner selections на ambiguity-heavy cases, чем у single-context и реализованного Reduced treatment.
2. Самая сильная наблюдаемая workflow-level separation появилась там, где evidence dependence и framing создавали ложную уверенность, а не на прямо разрешимых задачах.
3. Более тяжёлый implemented workflow имеет существенный resource overhead, поэтому selective activation действительно важен.
4. Часть наблюдаемой пользы относится к structured multi-pass analysis вообще: shared-context multi-agent хорошо выступил по нескольким primary metrics.
5. Targeted isolation-ablation не показал incremental answer-quality защиты от isolation при протестированном explicit false-anchor manipulation, хотя сама information boundary прошла mechanical integrity checks.

Evidence всё ещё **не** устанавливает общего превосходства canonical CG над обычным анализом, независимого answer-quality выигрыша от isolation или универсального числового activation threshold. Исходный benchmark также выявил metric gap вокруг полной semantic causal-structure correctness и material raw-vs-normalized interpretation issue.

Полезный эмпирический вопрос остаётся прежним:

> В каких причинных режимах Convergence Guard улучшает качество решения настолько, что оправдывает дополнительную стоимость, а в каких добавляет только лишнюю осторожность или overhead?

Текущего результата уже достаточно для практической карты применимости с явной неопределённостью. Следующий полезный evidence-building шаг — replication на другой модели/runtime и, если isolation остаётся центральным empirical claim, более сильный pre-frozen contamination test, который сам не предупреждает shared workers, что inherited conclusion является “NOT EVIDENCE”.
