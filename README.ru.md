# Convergence Guard

[English](README.md)

Convergence Guard — протокол анализа решений для сложных открытых задач, где главная опасность — **преждевременная сходимость**: принять одно правдоподобное причинное объяснение или действие до того, как действительно важные альтернативы были разделены, подвергнуты стресс-тесту и сравнены.

Проект оформлен как [Agent Skill](https://agentskills.io/) и рассчитан прежде всего на агентные клиенты, которые умеют создавать действительно изолированные рабочие контексты.

![Схема Convergence Guard: общий вопрос, свидетельства и контракт решения проходят через изолированный поиск, слепой скрининг и карту причин, досье, попарное сравнение и шлюз достаточности. Возможные исходы — обоснованное действие, различающая проверка в пределах бюджета или явно обозначенная неопределённость.](assets/convergence-guard-workflow.png)

## Попробовать за 60 секунд

Если ваш агентный клиент поддерживает Agent Skills:

1. клонируйте или скачайте этот репозиторий;
2. установите или свяжите папку `convergence-guard/` с каталогом skills вашего клиента, чтобы он обнаружил `convergence-guard/SKILL.md`;
3. начните, например, с такого запроса:

```text
Используй Convergence Guard для анализа вопроса:

Почему автономные AI-агенты до сих пор плохо справляются с длительными
реальными задачами и какое вмешательство стоит приоритизировать?

Используй Full Mode только если runtime проходит isolation preflight.
Если настоящая изоляция контекстов недоступна, явно скажи об этом и переходи
к Reduced Mode только если я принимаю это ограничение. Не выбирай победителя,
если доказательств недостаточно. В конце укажи минимальное наблюдение или
эксперимент, который способен изменить решение.
```

Full Mode должен выдавать не просто несколько мнений. Он фиксирует контракт решения, ищет причинно различные альтернативы в изолированных контекстах, сокращает их без раскрытия слепых стадий друг другу, стресс-тестирует оставшиеся модели, отделяет суждение о модели от выбора действия и либо рекомендует действие, либо возвращает `INSUFFICIENT DATA TO CHOOSE`.

Full Mode не привязан к конкретному runtime, но требует реальной изоляции: клиент должен уметь обеспечивать разделение контекстов там, где протокол зависит от слепоты или независимости. Одной поддержки нескольких агентов недостаточно.

### Идея за одну минуту

Представьте: на полу разбита чашка. Рядом сидит кот, а камера ясно показывает, как он столкнул чашку со стола. Здесь **не нужны** комиссия следователей, несколько причинных моделей и длинный аудит свидетельств. Хороший обычный анализ будет быстрее и дешевле. Full Convergence Guard в такой задаче — почти как криминалистическая лаборатория для вопроса, который уже решён видеозаписью.

А теперь представьте настоящее сложное расследование. Есть несколько правдоподобных причин. Пять сообщений вроде бы подтверждают одну версию — но после проверки provenance оказывается, что все пять пересказывают один первоначальный источник. Самая очевидная история звучит убедительно, однако evidence всё ещё недостаточно, чтобы честно выбрать её вместо живой альтернативы. Именно для таких задач и создан Convergence Guard: его цель — мешать анализу слишком быстро «влюбиться» в первую красивую версию.

Именно такой паттерн появился в замороженном **implemented-workflow benchmark** `main-v0.1.7`. На M05 — специально deceptive-underdetermination case — single-context и реализованный Reduced treatment получили от blind judge по `premature_winner=1`, тогда как реализованный Full treatment и shared-context multi-agent сохранили обе реально живые альтернативы. На всех восьми cases реализованный Full treatment получил **0/8 premature winners** и самый высокий mean action quality, но стоил примерно **9.1 model calls на case вместо 1** у single-context.

Практическое правило поэтому очень простое:

> **Для простого вопроса Convergence Guard может быть пушкой по воробьям. Для сложного расследования это полезный способ не дать аналитику слишком рано принять красивую, но недостаточно подтверждённую версию.**

Benchmark не показывает, что canonical Full Mode всегда лучший. Post-benchmark conformance audit обнаружил, что `main-v0.1.7` исполнял **упрощённые реализации Full/Reduced**, а не каждую conditional rule текущей спецификации. Shared-context multi-agent тоже получил 0/8 premature winners при заметно меньшей цене, а реализованный Full workflow иногда был чрезмерно осторожен на `COEXIST` cases. Поэтому данные поддерживают **выборочный structured analysis для действительно сложных и неоднозначных решений**, а не автоматический запуск CG везде.

Следующий targeted isolation-ablation на 16 cells оставил одинаковыми model, evidence, search mandates, call count, seeds и synthesis structure и менял только доступ search workers к предыдущим выводам. Isolation boundary прошла механическую проверку, но **false-anchor adoption не возникла даже в shared treatment (0/8 по двум независимым anchor judges)**. Поэтому текущий evidence **не показывает отдельного answer-quality преимущества самой isolation** при протестированной manipulation. См. [результат isolation-ablation](evals/results/isolation-ablation-v0.1.4/INTERPRETATION.ru.md).

## Почему не просто спросить 5 агентов?

Потому что пять ответов — это ещё не пять независимых свидетельств.

- **Независимость рассуждений не равна независимости доказательств.** Агенты могут рассуждать отдельно, но опираться на один и тот же источник, набор данных, summary или унаследованное утверждение. Их согласие тогда отражает общее происхождение evidence, а не независимое подтверждение.
- **Общая рамка создаёт коррелированные ошибки.** Если все агенты начинают с одного набора кандидатов, предпосылок, памяти или framing, несколько внешне независимых веток могут воспроизвести один и тот же blind spot.
- **Голосование измеряет согласие, а не вес доказательств.** Большинство 4:1 всё ещё может быть четырьмя пересказами одной слабой предпосылки. Convergence Guard сравнивает provenance, причинные предсказания, допущения и последствия для решения, а не принимает число голосов за доказательство.
- **Иногда победителя быть не должно.** В Convergence Guard есть evidence-sufficiency gate, который позволяет вернуть `INSUFFICIENT DATA TO CHOOSE`, а не искусственно производить консенсус.

Поэтому смысл не в том, чтобы использовать больше агентов, а в том, чтобы обеспечить **структурированную независимость, контролируемые информационные границы, provenance-aware сравнение и легитимную возможность воздержаться от выбора**.

## Какую проблему он решает?

Сложный анализ часто ломается одинаково:

1. первое правдоподобное объяснение становится якорем;
2. последующие альтернативы рождаются уже внутри этого якоря;
3. несколько агентов соглашаются, потому что используют те же данные, предпосылки или рамку;
4. причинная история становится всё красивее, хотя сама причинность не доказана;
5. наиболее правдоподобную модель незаметно принимают за лучшее действие;
6. итог звучит уверенно, но не говорит, какое наблюдение должно изменить решение.

Один из центральных принципов текущей архитектуры:

> **Независимость рассуждений не равна независимости доказательств, а наиболее правдоподобная модель не всегда означает лучшее действие при неопределённости.**

В исследованиях с большим объёмом внешних свидетельств Convergence Guard также оценивает **конкретные утверждения, а не престиж источника**. Статус official, peer-reviewed, institutional, fringe или anonymous влияет на стратегию проверки, но не заменяет provenance, проверяемость и анализ общего происхождения evidence.

## Когда Convergence Guard действительно нужен?

Convergence Guard не должен автоматически усложнять любую задачу. Замороженный workflow benchmark `main-v0.1.7` даёт более широкий сигнал о границе применимости: восемь причинных режимов, четыре реализованных режима анализа и 32 participant runs — по одному repeat на каждую ячейку `case × mode`. Но его нельзя читать как полную валидацию canonical Full/Reduced specification.

- `cg-full` дал **0/8 premature winners**, **2/2 correct abstentions** на keyed-insufficient cases и самый высокий mean action quality (**1.875/2**), но дорого: в среднем около **9.1 model calls, 12.5k input tokens и 5.6k output tokens на case**;
- shared-context multi-agent тоже дал **0/8 premature winners** и **2/2 correct abstentions**, потребляя меньше ресурсов, но уступая по среднему action и next-test score;
- single-context и `cg-reduced` получили по одному premature winner на специально deceptive-underdetermination case M05;
- Full Mode **не** доминировал по всем diagnostics: его literal declared status совпал с hidden key в 5/8 cases против 6/8 у single-context, а текущий metric set не сводит все structural ошибки между `CHOOSE / COEXIST / INSUFFICIENT` к одной метрике correctness.

Важная оговорка о scoring: blind semantic judging выполнялся по **заранее нормализованным** артефактам `final.json`. Последующий blind raw-vs-normalized re-audit всех 16 runs M04–M07 показал, что N1 сработала в **15/16** runs, причём два judge во многих случаях соглашались, что repair материально менял winner-like semantic interpretation. Frozen scores остаются неизменными, поскольку normalizer был predeclared и treatment-independent, но normalization уже нельзя считать просто косметической output-cleanup. См. [normalization re-audit](evals/results/main-v0.1.7/diagnostics/REJUDGE-REPORT.md).

Поэтому результат поддерживает **selective-use** стратегию: тяжёлый structured analysis выглядит полезнее при высоком framing risk, evidence dependence, причинной неоднозначности или высокой цене преждевременного решения, но он дорог и не должен быть default для любой разрешимой задачи. Последующий conformance audit нашёл missing/partial canonical branches в executable Full/Reduced treatments v0.1.7; correction layer v0.2 теперь делает такие gaps явными и fail-closed вместо того, чтобы молча называть неполный path «Full Mode complete».

Targeted isolation-ablation добавляет ещё одну важную границу: implemented isolation boundary механически работала, но shared treatment тоже устоял против injected false anchors, поэтому **incremental quality benefit isolation остаётся недоказанным** в текущем evidence base.

См. расширенную [доказательную карту применимости](convergence-guard/references/applicability-evidence-map.ru.md) / [Applicability Evidence Map](convergence-guard/references/applicability-evidence-map.md), где отдельно показаны проверенные локальные наблюдения, гипотезы переноса и неподтверждённые утверждения, а также [руководство по применимости](convergence-guard/references/applicability.ru.md) / [English version](convergence-guard/references/applicability.md). Источники: [main benchmark metrics](evals/results/main-v0.1.7/REPORT.md), [интерпретация main](evals/results/main-v0.1.7/INTERPRETATION.ru.md), [v0.2 conformance matrix](evals/protocol/v0.2/CONFORMANCE-MATRIX.md), [интерпретация isolation](evals/results/isolation-ablation-v0.1.4/INTERPRETATION.ru.md) / [English](evals/results/isolation-ablation-v0.1.4/INTERPRETATION.md). Ранний technical pilot сохранён в [evals/PILOT-REPORT-v0.1.md](evals/PILOT-REPORT-v0.1.md).

## Текущий процесс

Протокол теперь организован в пять больших фаз:

```text
A. УСТАНОВИТЬ ЗАДАЧУ РЕШЕНИЯ
   происхождение фактов → контракт решения → проверка рамки / внешний взгляд

B. ИССЛЕДОВАТЬ ПРОСТРАНСТВО ПРИЧИН
   3 изолированных поисковых мандата
   → проверка покрытия
   → расширение до 4–5 только при реальной необходимости

C. СОКРАТИТЬ ПРОСТРАНСТВО БЕЗ ЯКОРЕНИЯ
   независимый скрининг ║ слепая карта причинных моделей
   → условный аудит границ
   → обычно 2–3 финалиста; после проверки покрытия / свидетельств набор может схлопнуться до 1 или 0 + отдельная information probe при необходимости

D. СТРЕСС-ТЕСТ И СТОЛКНОВЕНИЕ
   независимые причинные досье
   → чувствительность к несущим допущениям
   → аудит общих искажений
   → попарное столкновение решений
   → условное независимое второе мнение

E. СОЙТИСЬ К ДЕЙСТВИЮ И ПРОВЕРКЕ
   суждение о модели ≠ выбор действия
   → проверка достаточности доказательств
   → лучшее действие или INSUFFICIENT DATA TO CHOOSE
   → минимальное наблюдение / эксперимент, способный изменить решение
```

## Что изменилось относительно v0.1.0

`v0.2.4` сохраняет упрощённую архитектуру v0.2, правила runtime-изоляции v0.2.1 и claim-level provenance discipline из v0.2.2. Correction layer v0.2.3 и доказательная карта v0.2.4 добавляют рекомендации по выборочной активации и явные уровни подтверждения применимости:

- поиск начинается с 3 изолированных workers и расширяется до 5 только при плохом покрытии;
- скрининг и слепое картирование запускаются параллельно в свежих контекстах;
- аудит границ причинных семейств теперь условный;
- обычно остаются 2–3 финалиста; после проверки покрытия набор может честно схлопнуться до одного настоящего выжившего или ни одной поддержанной модели — слабые варианты не повышаются ради формата;
- модели могут быть взаимоисключающими, сосуществующими, вложенными или взаимодействующими;
- связность причинной истории отделена от проверки самой причинности;
- несколько почти одинаковых моделей не считаются независимым подтверждением;
- dossier-worker больше не обязан сравниваться с соперником, которого он не видел;
- стресс-тест выбирает действительно критичные предпосылки по неопределённости, причинному рычагу и влиянию на решение;
- общий blind spot может отправить процесс за новыми данными или в новый причинный поиск, а не только к запасным вариантам из того же пула;
- pairwise collision сравнивает конфликтующие последствия для решений и не заставляет совместимые причины искусственно «побеждать» друг друга;
- появился отдельный слой выбора действия с учётом потерь, сожаления об ошибке, обратимости и ценности сохранения вариантов;
- формально определён Reduced Mode для сред без настоящей изоляции workers;
- material claims оцениваются по provenance, inspectability, common evidence ancestry, противоречиям и source role, а не по одной репутации источника;
- material new evidence, найденное внутри blind branch, должно пройти shared evidence checkpoint, прежде чем сможет изменить downstream decision.

## Структура репозитория

```text
Convergence Guard/
├── .gitattributes
├── README.md
├── README.ru.md
├── CHANGELOG.md
├── CHANGELOG.ru.md
├── DESIGN.md
├── DESIGN.ru.md
├── LICENSE
├── ATTRIBUTION.md
├── ATTRIBUTION.ru.md
├── THIRD_PARTY_NOTICES.md
├── examples/
│   ├── jack-the-ripper-full-mode.md
│   ├── jack-the-ripper-full-mode.ru.md
│   ├── long-running-autonomous-agents-full-mode.md
│   ├── long-running-autonomous-agents-full-mode.ru.md
│   ├── sars-cov-2-origins-full-mode.md
│   └── sars-cov-2-origins-full-mode.ru.md
└── convergence-guard/
    ├── SKILL.md
    └── references/
        ├── explained-simply.md
        ├── explained-simply.ru.md
        ├── applicability.md
        ├── applicability.ru.md
        ├── protocol-details.md
        ├── protocol-details.ru.md
        ├── reduced-mode.md
        ├── reduced-mode.ru.md
        └── protocol.ru.md
```

`convergence-guard/` — устанавливаемая папка skill. Устанавливать нужно всю папку вместе с `references/`; одного `SKILL.md` недостаточно для полного Full/Reduced Mode, если адаптер явно не встраивает необходимые reference-файлы. Имя папки совпадает с `name: convergence-guard` в `SKILL.md`.

`protocol.ru.md` сохранён как **исторический русский протокол v0.1.0**. Это уже не каноническая спецификация текущего `v0.2.4`; runtime-specific формулировки в нём нейтрализованы для публичного репозитория.

## Документация

| English | Russian | Назначение |
|---|---|---|
| [README.md](README.md) | [README.ru.md](README.ru.md) | обзор проекта |
| [CHANGELOG.md](CHANGELOG.md) | [CHANGELOG.ru.md](CHANGELOG.ru.md) | история релизов |
| [DESIGN.md](DESIGN.md) | [DESIGN.ru.md](DESIGN.ru.md) | threat model и архитектурное обоснование |
| [ROADMAP.md](ROADMAP.md) | [ROADMAP.ru.md](ROADMAP.ru.md) | приостановка разработки, условная проверка пользы, упрощение и критерии остановки |
| [ATTRIBUTION.md](ATTRIBUTION.md) | [ATTRIBUTION.ru.md](ATTRIBUTION.ru.md) | происхождение и граница влияния |
| [explained-simply.md](convergence-guard/references/explained-simply.md) | [explained-simply.ru.md](convergence-guard/references/explained-simply.ru.md) | простое объяснение метода |
| [applicability.md](convergence-guard/references/applicability.md) | [applicability.ru.md](convergence-guard/references/applicability.ru.md) | когда CG, вероятно, полезен, а когда избыточен |
| [applicability-evidence-map.md](convergence-guard/references/applicability-evidence-map.md) | [applicability-evidence-map.ru.md](convergence-guard/references/applicability-evidence-map.ru.md) | 8 проверенных сценариев, 12 возможных областей и уровни доказательности |
| [protocol-details.md](convergence-guard/references/protocol-details.md) | [protocol-details.ru.md](convergence-guard/references/protocol-details.ru.md) | подробные правила протокола |
| [reduced-mode.md](convergence-guard/references/reduced-mode.md) | [reduced-mode.ru.md](convergence-guard/references/reduced-mode.ru.md) | fallback для одного контекста |

Текущие двуязычные примечания к выпуску: [Release Notes v0.2.4](RELEASE-NOTES-v0.2.4.md).

## Публичные примеры

Опубликованные разборы:

- [English: Jack the Ripper — Full Mode case study](examples/jack-the-ripper-full-mode.md)
- [Русский: Джек Потрошитель — пример Full Mode](examples/jack-the-ripper-full-mode.ru.md)
- [English: Why autonomous AI agents fail on long-running real-world tasks — Full Mode case study](examples/long-running-autonomous-agents-full-mode.md)
- [Русский: Почему автономные AI-агенты ломаются на длительных реальных задачах — Full Mode case study](examples/long-running-autonomous-agents-full-mode.ru.md)
- [English: SARS-CoV-2 origins — Full Mode case study](examples/sars-cov-2-origins-full-mode.md)
- [Русский: Происхождение SARS-CoV-2 — пример Full Mode](examples/sars-cov-2-origins-full-mode.ru.md)

В примерах сохранены контракт решения, provenance-aware evidence brief, причинно различные поисковые мандаты, coverage gate, слепое сокращение, досье финалистов, adjudication, условное second-opinion review, evidence-sufficiency gate и наблюдение, способное изменить решение.

> **Граница примеров:** эти case studies демонстрируют работу протокола decision analysis над evidence, доступным конкретному run. Они не заменяют лабораторное исследование, полевое расследование, судебную или криминалистическую экспертизу, уголовное расследование, разведывательный анализ, юридическое заключение или другую профильную первичную работу. Если первичное или непубличное evidence недоступно, пример сохраняет это ограничение и не превращает institutional assessment в прямое подтверждение underlying event.

## Full Mode и Reduced Mode

**Full Mode** требует настоящих изолированных worker/agent-контекстов для операций, где независимость или слепота являются частью гарантии метода.

**Reduced Mode** — явно маркируемый запасной режим для одного контекста. Он сохраняет форму анализа, но не способен воспроизвести information-boundary и blindness guarantees настоящей изоляции и не должен выдаваться за эквивалент Full Mode.

## Язык и локализация

Канонический agent-facing `SKILL.md` написан на английском для переносимости между клиентами. Сам skill требует отвечать на языке пользователя, если пользователь не попросил другой язык.

Публичная человекочитаемая документация по возможности поддерживается парами English/Russian. У текущих explanatory и operational references есть русские sibling-файлы; устанавливаемый `SKILL.md` остаётся каноническим английским. Историческая полная русская спецификация `v0.1.0` сохранена отдельно в `convergence-guard/references/protocol.ru.md`.

## Установка

Нужно установить или связать папку `convergence-guard/` с каталогом skills конкретного агентного клиента.

Совместимый клиент должен обнаружить `convergence-guard/SKILL.md` и использовать его `name` и `description` для определения релевантности.

## Статус

**Исследовательский pre-release. Последний tagged release: v0.2.4.**

**Активная разработка новых функций приостановлена.** См. [исследовательский план и критерии остановки](ROADMAP.ru.md). Мы сохраняем существующий research preview, не обещая новых тестов или продвижения.

Текущий исследовательский выпуск — [v0.2.4](https://github.com/lavalava45/convergence-guard/releases/tag/v0.2.4). Он включает прежний замороженный benchmark реализованных workflows, исправления после аудита соответствия, аудит normalization, targeted isolation ablation и новую двуязычную доказательную карту применимости. Он **не доказывает** широкого межотраслевого превосходства или измеренного преимущества canonical Full v0.2. Приватные ключи и mapping судей намеренно не опубликованы, поэтому публичный архив позволяет проверять входные данные, код, manifests и агрегаты, но не полностью независимо повторить judging только из публичных файлов; см. [ограничения воспроизводимости](evals/README.md#reproducibility-boundary). Более поздние изменения фиксируются в [CHANGELOG.ru.md](CHANGELOG.ru.md).

Метод уже прошёл первый архитектурный и методологический аудит и содержит публичные Full Mode examples: историческую attribution-задачу, актуальный научный вопрос с асимметричным evidence и современную задачу надёжности AI-агентов. За двух-case technical pilot теперь последовал замороженный comparative benchmark `main-v0.1.7`: 8 cases × 4 modes × 1 repeat = 32 participant runs, затем 32 calibration runs и blind semantic judging по нейтральным answer IDs. Это evidence для карты применимости, а не универсальный superiority claim: в этом наборе из восьми cases у Full Mode не наблюдалось premature winners и он дал самые сильные средние actions, но стоил значительно дороже и всё ещё показывал structural/status mismatches на части coexistence cases.

## Происхождение

Early versions of this protocol were inspired by Udit Akhouri's ADHD divergent-ideation skill. The current method substantially redesigns the workflow around causal models, information isolation, adversarial comparison, assumption stress-testing, and falsifiable convergence.

Эта формулировка сохранена как канонический текст атрибуции. Подробности — в [ATTRIBUTION.md](ATTRIBUTION.md) и [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Лицензия

MIT. См. [LICENSE](LICENSE).
