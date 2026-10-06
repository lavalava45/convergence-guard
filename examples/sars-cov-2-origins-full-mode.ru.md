# Происхождение SARS-CoV-2: пример Convergence Guard Full Mode

[English version](sars-cov-2-origins-full-mode.md)

> **Оговорка о статусе примера.** Этот документ — разбор работы Convergence Guard, выполненный 2026-10-06 по публично доступным данным. Он **не является** оригинальным лабораторным исследованием, полевым эпидемиологическим расследованием, судебной или криминалистической экспертизой, уголовным расследованием, разведывательной оценкой или установлением юридической ответственности. У run не было привилегированного доступа к лабораторным журналам, засекреченным данным, частным медицинским записям, неопубликованным биологическим образцам или другим непубличным материалам. Поэтому выводы здесь относятся к тому, **что позволяют заключить приведённые публичные свидетельства по правилам протокола**, а не заменяют первичную научную или следственную работу.

## Исследовательский вопрос

Какой причинный сценарий происхождения SARS-CoV-2 и начала пандемии COVID-19 лучше всего поддерживается совокупностью публично доступных свидетельств по состоянию на 6 октября 2026 года? Достаточны ли данные, чтобы предпочесть один сценарий с обоснованной уверенностью, или корректный результат — `INSUFFICIENT DATA TO CHOOSE`?

Run **не** начинался с заранее заданного исчерпывающего списка публичных гипотез. От него требовалось самостоятельно сформировать причинно различные семейства моделей из evidence и сохранить outside alternative, если публичные данные допускают существенный путь, не совпадающий с привычными версиями.

## Почему этот кейс подходит для Convergence Guard

Вопрос объединяет сразу несколько типов ошибок, против которых построен протокол:

- политически и институционально спорные источники;
- неполные и частично недоступные первичные записи;
- несколько исследований, повторно использующих одни и те же образцы или списки случаев;
- сильный соблазн принять **возможность механизма** за доказательство того, что событие произошло;
- сильный соблазн принять раннее место усиления вспышки за место первого заражения;
- геномные наблюдения, совместимые сразу с несколькими причинными путями;
- разведывательные оценки, чья исходная evidence base частично засекречена;
- отсутствующие данные, которые легко ошибочно превратить либо в «доказательство отсутствия», либо в «доказательство сокрытия».

Поэтому центральный вопрос метода здесь не «у какой стороны больше аргументов?», а другой: **замыкает ли хоть одна модель решающие причинные переходы свидетельствами, которые достаточно прямы, различающи, проверяемы и независимы?**

## Без solo baseline

В отличие от первого публичного примера в этом репозитории, здесь намеренно **не было предварительного solo-analysis baseline**. Пользователь прямо потребовал новый независимый Full Mode run с нуля и запретил передавать прежние выводы в этапы, зависящие от изоляции.

Это важно, потому что даже скрытый впоследствии предварительный фаворит может повлиять на формулировку поисковых мандатов или ожидания координатора. Здесь поиск начинался с общего factual brief и decision contract, а не с заранее выбранной версии.

# Phase A — evidence brief и decision contract

## Контракт решения

**Вопрос решения:** какое причинное семейство лучше всего поддерживается публично проверяемыми данными и достаточно ли этой поддержки для обоснованной причинной атрибуции?

**Граница задачи:** как минимум разделять три стадии, которые в публичной дискуссии часто сливаются в одну историю:

1. **ближайшее вирусное происхождение / контекст приобретения** — откуда биологически пришёл вирус или его непосредственный предшественник;
2. **первое причинно значимое заражение человека** — каким путём линия, запустившая пандемию, попала в человека;
3. **устойчивая передача / amplification** — каким образом заражение превратилось в самоподдерживающуюся вспышку и где произошло раннее усиление передачи.

Поэтому модель может одновременно предполагать естественное происхождение вируса и research-associated заражение человека; либо первое заражение вне Huanan с последующим сильным amplification на рынке.

**Запрещённые подмены:**

- возможность лабораторной или полевой работы → факт research accident;
- amplification на рынке → доказательство первого spillover именно на рынке;
- престиж источника → истинность его содержательного утверждения;
- засекреченное или недоступное обоснование → подтверждённый факт;
- отсутствие найденного intermediate host → доказательство laboratory origin;
- отсутствие публичного incident report → доказательство отсутствия лабораторного инцидента;
- несколько публикаций одного dataset → независимое подтверждение.

**Критерий успеха:** предпочитаемая модель должна лучше конкурентов объяснять действительно различающие наблюдения, выдерживать проверку provenance и common evidence ancestry и лучше замыкать свои несущие причинные переходы.

**Цена ошибки:** ложная атрибуция может исказить научную и biosafety-политику, меры по wildlife trade, международные отношения, общественное доверие и вопросы ответственности. Сохранить неопределённость лучше, чем превратить правдоподобие в факт.

## Claim-level source policy

Run оценивал **конкретные утверждения**, а не присваивал целым институтам, журналам, правительствам, activist-группам или разведывательным структурам глобальный статус «надёжный/ненадёжный».

Для material claims по возможности проверялось:

- где находится ближайший доступный первичный источник;
- можно ли проверить underlying evidence;
- доступны ли методы и raw data;
- насколько наблюдение близко ко времени события;
- не происходят ли несколько публикаций из одного dataset, briefing или документа;
- какие существуют противоречащие данные;
- какие incentives или conflicts могли повлиять на сообщение или отбор данных;
- какую роль источник играет именно здесь: `EVIDENCE`, `CORROBORATION`, `CONTEXT`, `LEAD ONLY` или `UNSUPPORTED`.

Постоянно сохранялось различие:

> **CONFIRMED:** организация или документ утверждает X  
> не означает  
> **CONFIRMED:** сам X действительно произошёл.

## Основные factual anchors

### 1. Huanan был исключительно ранним узлом вспышки

Worobey et al. сообщили, что самые ранние известные случаи COVID-19 декабря 2019 года, включая случаи без зарегистрированной прямой связи с рынком, географически концентрировались вокруг Huanan Seafood Wholesale Market, где в конце 2019 года продавались живые млекопитающие, восприимчивые к SARS-CoV-2.

Это значимое evidence того, что Huanan был очень ранним эпидемиологическим узлом и местом amplification. Но оно **само по себе не устанавливает первое animal→human transmission event**.

Источник: [Worobey et al., *Science* (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9348750/).

### 2. Environmental samples рынка были положительными; sampled animals — нет

China CDC сообщил о 923 environmental samples, собранных после закрытия рынка; SARS-CoV-2 был обнаружен в 74. Одновременно 457 animal-related samples от 18 видов дали отрицательный результат на нуклеиновую кислоту SARS-CoV-2.

Отрицательные animal samples — это реальное negative evidence. Но его различающая сила ограничена: sampling начался уже после закрытия рынка и не представлял собой полного pre-closure набора живых восприимчивых животных, продававшихся в причинно значимый период.

Источник: [Liu et al., *Nature* (2023)](https://www.nature.com/articles/s41586-023-06043-2).

### 3. Генетический материал восприимчивых диких животных встречался в части положительных market samples

В анализе *Cell* 2024 года по metagenomic data China CDC в SARS-CoV-2-positive пробах из wildlife stall был найден генетический материал, в том числе raccoon dogs, civets и bamboo rats; рядом с этим stall также наблюдалась повышенная SARS-CoV-2 positivity.

Это усиливает свидетельство, что восприимчивые животные и заражённая вирусом среда находились в одном и том же раннем market micro-environment. Но поскольку это environmental samples, взятые после значительной human transmission, они **не устанавливают заражение конкретного животного и не определяют направление передачи**.

Источник: [Crits-Christoph et al., *Cell* (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11427129/).

### 4. Сильнейшие market datasets имеют общее происхождение

Значительная часть Huanan environmental, metagenomic, wildlife-DNA и stall-localization evidence происходит из одного и того же корпуса post-closure samples China CDC. Повторный анализ может извлечь новые сведения, исправить методы и раскрыть ранее неиспользованные признаки, но он не превращает одно биологическое sampling event в несколько независимых выборок.

Аналогично несколько spatial analyses ранних случаев повторно используют перекрывающиеся early Wuhan case records.

### 5. Пространственная локализация оспаривается

Опубликованные статистические критики указывают, что концентрация ранних случаев вокруг Huanan сама по себе не идентифицирует рынок как origin и может быть чувствительна к ascertainment bias и допущениям spatial methods.

Источники: [Stoyan & Chiu, JRSS A (2024)](https://academic.oup.com/jrsssa/article/187/3/710/7557954); [Weissman, JRSS A (2024)](https://academic.oup.com/jrsssa/article/187/3/720/7632556).

Эти работы сильнее ослабляют утверждение **«первый spillover произошёл на Huanan»**, чем более узкое утверждение **«Huanan был крупным ранним узлом вспышки»**.

### 6. Ранние линии A/B информативны, но не являются несущим доказательством

Pekar et al. интерпретировали раннее разнообразие SARS-CoV-2 как наиболее согласующееся как минимум с двумя cross-species transmissions. В erratum 2023 года была исправлена ошибка в коде, из-за которой Bayes factors в пользу multiple introductions были завышены; исправленный анализ всё ещё предпочитал multiple introductions, но отдельно подчеркнул disagreement между вариантами rooting.

Источники: [Pekar et al., *Science* (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9348752/); [erratum 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC13244787/).

Поэтому run считал «две ранние линии» возможным support для repeated spillover, но не позволял этому аргументу единолично определять origin.

### 7. Естественная bat-sarbecovirus ancestry поддерживается сильно, но плохо различает некоторые пути

Field studies задокументировали большое естественное разнообразие и рекомбинацию среди bat SARS-related coronaviruses, включая вирусы, способные использовать human ACE2 или имеющие родственные receptor-binding свойства.

Это сильно поддерживает естественную эволюционную ancestry. Но естественное происхождение совместимо как с обычным wildlife exposure, так и с research-associated exposure к естественно существующему вирусу.

Источники: [Hu et al., *PLOS Pathogens* (2017)](https://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1006698) и [Temmam et al., *Nature* (2022)](https://www.nature.com/articles/s41586-022-04532-4).

### 8. До вспышки существовали релевантные field- и laboratory-workflows

Публичные pre-pandemic публикации показывают, что исследователи Wuhan Institute of Virology и партнёры собирали bat coronaviruses, выделяли живые SARS-related viruses, использовали cell culture и reverse-genetics systems в исследованиях родственных коронавирусов.

Это прямое evidence **capability и возможных exposure pathways**. Это не прямое evidence того, что SARS-CoV-2 или достаточно близкий progenitor находился в лаборатории до вспышки или что сотрудник был заражён.

Источники: [Hu et al. (2017)](https://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1006698); [Menachery et al., PNAS (2016)](https://pubmed.ncbi.nlm.nih.gov/26976607/); [WIV1 reverse-genetics work, *Journal of Virology* (2016)](https://journals.asm.org/doi/10.1128/jvi.03079-15).

### 9. Лабораторная адаптация биологически возможна; её участие в цепочке SARS-CoV-2 не установлено

В работе *PLOS Pathogens* 2025 года сообщалось, что bat sarbecovirus WIV1-CoV, вероятно, приобрёл adaptive spike mutation при propagation in cell culture. Это показывает, что лабораторное размножение может приводить к функционально значимой адаптации в релевантном классе вирусов.

Для этого run это `CORROBORATION` осуществимости механизма, а не evidence того, что SARS-CoV-2 прошёл такой путь.

Источник: [Tse et al., *PLOS Pathogens* (2025)](https://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1013123).

### 10. DEFUSE подтверждает существование proposal, а не его выполнение

Proposal DEFUSE 2018 года material, потому что документирует предложенную экспериментальную работу с bat coronaviruses, включая cleavage-site-related work. Но proposal — это evidence исследовательского намерения/capability, а не доказательство выполнения предложенной работы или создания SARS-CoV-2. Публично доступный DARPA program-manager summary не рекомендовал предложение к финансированию.

Публичные копии документов: [DEFUSE proposal](https://usrtk.org/wp-content/uploads/2023/01/defuse-proposal.pdf); [DARPA PM summary](https://drasticresearch.org/wp-content/uploads/2021/09/hr00118s017-preempt-fp-019-pm-summary-selectable-not-recommended.pdf).

### 11. Публичные intelligence assessments подтверждают наличие оценок, а не автоматически их скрытое evidence

ODNI report 2023 года документировал расхождение взглядов внутри U.S. Intelligence Community, coronavirus research в WIV и biosafety concerns, одновременно указывая на отсутствие direct evidence конкретного research-related incident и отсутствие известного pre-pandemic holding SARS-CoV-2 или близкого progenitor в WIV.

Источник: [ODNI, *Potential Links Between the Wuhan Institute of Virology and the Origins of COVID-19* (2023)](https://archive.dni.gov/files/ODNI/documents/assessments/Report-on-Potential-Links-Between-the-Wuhan-Institute-of-Virology-and-the-Origins-of-COVID-19-20230623.pdf).

В июне 2026 года ODNI опубликовал дополнительные материалы в сопровождении press release, прямо утверждавшего Wuhan-research origin и заявлявшего о manipulation of earlier intelligence processes. Существование и формулировка этой оценки подтверждены. Но там, где underlying evidence остаётся непубличным, сам substantive event нельзя автоматически повысить до `CONFIRMED` только из-за institutional assertion.

Источник: [ODNI release, 18 июня 2026](https://archive.dni.gov/index.php/newsroom/press-releases/press-releases-2026/4166-pr-11-26).

### 12. Критически важные данные для проверки всех сильных путей остаются недоступными

WHO SAGO в assessment 2025 года указала, что weight of available evidence, рассмотренного группой, склоняется к zoonotic spillover, но одновременно зафиксировала отсутствие данных, необходимых для оценки laboratory-related event; поэтому такой путь нельзя ни подтвердить, ни исключить. SAGO также перечислила недостающие early human sequences, animal/supply-chain information, laboratory-work documentation, biosafety records и staff-health information.

Источник: [WHO SAGO, *Independent assessment of the origins of SARS-CoV-2* (2025)](https://www.who.int/publications/m/item/independent-assessment-of-the-origins-of-sars-cov-2-from-the-scientific-advisory-group-for-the-origins-of-novel-pathogens).

Этот report использовался как прозрачный synthesis и источник сведений о том, какие материалы SAGO рассмотрела и какие запросила, а не как authority, чьё заключение автоматически определяет результат.

# Phase A reframe — что именно требуется объяснить?

Fresh reframe reviewer обнаружил скрытое допущение обычной публичной постановки: «происхождение вируса» и «начало устойчивой передачи среди людей» часто рассматриваются как одно неделимое событие.

Более строгая постановка разделила:

1. ближайшую вирусную ancestry или контекст приобретения;
2. первое причинно значимое заражение человека;
3. establishment и amplification устойчивой human transmission.

Это различие существенно: естественный вирус может попасть к человеку через research contact, а первое заражение вне Huanan может закончиться мощным amplification на Huanan.

Reviewer также потребовал сохранить outside/hybrid route, поскольку публичные evidence не гарантируют, что знакомые именованные сценарии исчерпывают причинное пространство.

# Phase B — изолированный причинный поиск

Три fresh search mandates различались по областям causal identification, а не по ролям адвокатов заранее выбранных версий.

## Mandate 1 — entry ecology и supply networks

Проверить, где и как естественно циркулирующий вирус мог попасть к людям через wildlife trade, farms, traders, transport, vendors, markets или распределённую supply network. Отделить первое заражение от последующего market amplification.

## Mandate 2 — research-contact pathways

Проверить field-sampling exposure, transport/handling samples, laboratory exposure к неизменённому natural virus, culture/passaging/adaptation и targeted recombinant work. Строго отделять evidence capability от evidence того, что событие произошло.

## Mandate 3 — genomic и early-transmission identification

Проверить, какие переходы origin вообще можно идентифицировать по ранним genomes, phylogeny, molecular features, root uncertainty, ранним lineages и timing — и какие наблюдения одинаково ожидаемы при конкурирующих acquisition routes.

Во время recovery research-contact branch был повторён в fresh context. Совпадение выводов повторных workers **не считалось независимым real-world evidence**.

## Coverage gate

Начальный поиск покрыл три существенно разные области:

- wildlife/trade entry и supply ecology;
- research-associated exposure mechanisms;
- genomic/early-transmission identification.

Coverage gate не обнаружил отдельного причинного региона, ради которого стоило бы добавлять workers просто для увеличения их количества. Open-world outside alternative был сохранён отдельно.

# Phase C — neutral candidates, screening и blind causal mapping

До сокращения пространства были зафиксированы восемь нейтральных candidate IDs:

| ID | Причинный механизм |
|---|---|
| N1 | Direct wildlife spillover на Huanan или рядом → market amplification |
| N2 | Upstream wildlife/supply-chain spillover → заражённый человек или животное достигает Huanan → amplification |
| N3 | Distributed wildlife/supply-network spillovers → Huanan становится главным amplification/detection node |
| N4 | Researcher заражается естественным вирусом во время field sampling → transmission в Wuhan |
| N5 | Laboratory exposure к неизменённому естественному вирусу → transmission в Wuhan |
| N6 | Laboratory exposure после culture/passaging/animal adaptation → transmission в Wuhan |
| N7 | Laboratory exposure при targeted recombinant/chimeric/engineered work → transmission в Wuhan |
| N8 | Первое заражение происходит где-то ещё неизвестным механизмом → human introduction на Huanan |

Fresh contract screener и fresh blind causal mapper работали независимо. До заморозки результатов ни один не видел output другого.

## Результат screening

Screener получил:

- **N1:** mixed support, partial causal chain; identification threatened из-за directionality и ascertainment;
- **N2:** mixed support, но upstream source и first infection остаются неидентифицированными;
- **N3:** более слабая поддержка, поскольку repeated spillovers требуют дополнительного evidence, а A/B inference исправлялся и чувствителен к rooting;
- **N4/N5:** механистически связны, но слабо поддержаны как реальные события, потому что публично отсутствует конкретная цепочка virus→exposure→infection;
- **N6/N7:** слабая event-level support и дополнительные неподтверждённые переходы alteration/manipulation + exposure;
- **N8:** не прошёл как полное причинное объяснение, поскольку оставляет acquisition mechanism неопределённым, но остался полезным outside residual.

Повторяющийся danger flag для research-associated models — **capability → occurrence**. Для direct-Huanan model — **market association → first spillover**.

## Blind causal map

Mapper сохранил внутренние различия и организовал жизнеспособные модели в три higher-order families:

### F-WILDLIFE

`N1 + N2 + N3`: явное семейство альтернативных wildlife/trade routes. Их support нельзя объединять так, будто все подмодели одновременно доказаны.

### F-RESEARCH-NATURAL

`N4 + N5`: research-associated exposure к естественно существующему вирусу — либо в field, либо после попадания неизменённого virus/sample в лабораторию.

### F-RESEARCH-ALTERED

`N6 + N7`: research-associated exposure, где причинным звеном является culture/passaging/adaptation или targeted genetic manipulation.

### N8-R — outside / hybrid / unknown

Сохранён как open-world complement. Ему запрещено получать поддержку только из-за неполноты именованных моделей.

## Boundary audit

Fresh boundary critic признал три higher-order families пригодными для finalist slate только при условии, что их внутренние submodels остаются видимыми и evidence не суммируется между взаимоисключающими маршрутами.

Он также зафиксировал endpoint: основной вопрос относится к пути, который породил **pandemic-establishing lineage**; буквально самое первое заражение SARS-CoV-2 любого человека остаётся отдельной sensitivity-задачей.

# Phase D — независимые dossiers финалистов

## Finalist A — wildlife/trade-associated natural entry

### Механизм

Естественно эволюционировавшая bat sarbecovirus lineage достигает людей через wildlife ecology и trade — непосредственно на Huanan либо выше по supply chain; затем Huanan становится крупным ранним amplification node.

### Strongest support

Сильнейший bundle находится сравнительно близко к событию:

1. ранние известные случаи концентрировались вокруг Huanan;
2. незадолго до закрытия там продавались живые восприимчивые млекопитающие;
3. SARS-CoV-2 был широко обнаружен в post-closure environmental samples рынка;
4. в части SARS-CoV-2-positive wildlife-stall samples присутствовала susceptible-wildlife DNA;
5. естественная bat-sarbecovirus ecology даёт связный upstream reservoir.

Этот bundle показывает больше, чем общую возможность механизма: susceptible wildlife, virus contamination и ранний human outbreak node оказываются в одном причинном окружении.

### Strongest contrary evidence / limitations

- ни одно pre-closure market animal публично не показано заражённым SARS-CoV-2;
- не найден direct progenitor или intermediate-host virus;
- все 457 sampled animal-related specimens были отрицательными;
- environmental samples собирались после заметной human transmission, поэтому human shedding способна воспроизвести значительную часть market signal;
- spatial inference ранних cases уязвим для неполного ascertainment и критики методов;
- upstream farms, traders, transporters и vendors публично не прослежены в полную infection chain.

### Что модель объясняет лучше ближайших конкурентов

Она объясняет сочетание ранней Huanan epidemiology, реально продававшихся восприимчивых животных, virus-positive wildlife-stall environments и wildlife genetic material **без необходимости сначала предположить непоказанное research possession/exposure event**.

### Что она не объясняет уникально

Естественно выглядящий genome, Huanan amplification, post-closure contamination рынка, неудачу поиска источника спустя годы и быструю human-to-human transmission объясняют и некоторые research-associated routes.

### Что существенно усилит модель

- аутентифицированный pre-closure infected animal specimen;
- basal SARS-CoV-2 или near-progenitor sequence от прослеженного животного или supply-chain node;
- заражение supplier/vendor/transporter, предшествующее известной market transmission и связанное с ней genome + provenance.

### Что существенно ослабит модель

- надёжно задокументированная sustained human chain, явно предшествующая Huanan и не связанная с wildlife trade;
- действительно полные archived animal/supplier data причинно значимого периода с отрицательным результатом;
- прямо показанный альтернативный переход precursor → first pandemic-establishing human infection.

## Finalist B — research-associated exposure к естественному вирусу

### Механизм

Естественно существующий precursor встречается во время field sampling или попадает в research facility; researcher или связанный worker заражается без причинно значимого engineering/adaptation step и запускает обычную human transmission. Huanan после этого всё ещё может стать ранним amplification node.

### Strongest support

Публичное evidence прямо устанавливает:

- extensive bat-coronavirus field sampling;
- handling и transport samples;
- isolation и culture живых SARS-related coronaviruses;
- реальный occupational exposure pathway;
- biosafety concerns и laboratory work на containment levels, релевантных risk assessment.

Семейство также объясняет, каким образом исследователи из Wuhan могли контактировать с вирусами из удалённой bat ecology.

### Strongest contrary evidence / limitations

Решающий event bridge публично отсутствует:

`relevant natural precursor → documented research possession/exposure → infected worker → onward transmission`.

Нет публично проверенного pre-outbreak SARS-CoV-2/near-progenitor holding, staff seroconversion с matching sequence, specific incident record или прослеженной worker→community chain.

### Что модель объясняет лучше wildlife/trade routes

Она объясняет, как редкий bat virus из удалённых field sites мог достичь Wuhan-associated human без необходимости показывать местное wildlife animal, доставившее его в город через trade.

### Что обе семьи объясняют одинаково

Natural viral ancestry, genome без обязательного engineering signature, Huanan amplification после introduction и отсутствие positive market animal после удаления причинно значимых животных.

### Что существенно усилит модель

Аутентифицированный датированный pre-December-2019 field или laboratory sample с near-progenitor sequence плюс соответствующие staff exposure, seroconversion, clinical specimen либо incident/access records.

### Что существенно ослабит модель

Полные и независимо проверяемые holdings/raw-read/field-roster/staff-serology records, исключающие relevant exposure в критическое окно, особенно вместе с прямой animal-source chain.

## Finalist C — research-associated altered/passaged/engineered virus

### Механизм

Natural precursor приобретается через research и затем изменяется через culture/passaging/animal adaptation или targeted recombinant work; exposure event заражает человека и запускает transmission.

### Strongest support

Публичная база подтверждает:

- релевантные reverse-genetics и live-virus capability;
- предложенные experimental designs вроде DEFUSE;
- биологическую возможность cell-culture adaptation у bat sarbecoviruses;
- общий accident-risk pathway.

### Strongest contrary evidence / limitations

Эта семья обязана замкнуть все переходы natural-virus research family **плюс дополнительный alteration step**. Публичное evidence сейчас не даёт цепочку:

`near progenitor → specific alteration/passaging history → SARS-CoV-2-like intermediate → exposure → infected worker → pandemic seeding`.

DEFUSE — proposal, а не доказательство исполнения. Furin cleavage site и другие genomic features не являются уникальными markers engineering. Обратное также неверно: отсутствие очевидного engineering signature не исключает все laboratory routes, особенно natural-virus family.

### Что существенно усилит модель

Аутентифицированные pre-outbreak construct, passage, raw-read, freezer или animal-work records, генетически связывающие известный precursor с SARS-CoV-2, вместе с evidence exposure и onward transmission.

### Что существенно ослабит модель

Полный audited research inventory и raw-data record, исключающие relevant precursor и experimental lineage, либо прямо задокументированная wildlife-source chain, предшествующая human transmission.

# Shared-bias и source-dependency audit

Slate-level audit показал, что apparent volume evidence по обе стороны увеличивается из-за common ancestry.

## Market branch

```text
China CDC post-closure Huanan samples
→ Nature 2023 surveillance paper
→ metagenomic / wildlife-DNA reanalyses
→ stall-localization and host-provenance analyses
```

Это не независимые biological collections.

## Early-case branch

```text
перекрывающиеся early Wuhan case records
→ geospatial analyses
→ reanalyses и statistical critiques
```

Разные statistical papers могут полезно спорить друг с другом, но не создают новых пациентов.

## Early-genome branch

```text
редкие и перекрывающиеся early human sequences
→ lineage/root inference
→ multiple-introduction models
→ corrections и reanalyses
```

Rooting и sampling assumptions распространяются на всю ветку.

## Research-origin branch

```text
field/lab programs + publications + grants/proposals
→ media / congressional / institutional summaries
→ intelligence и policy assessments
```

Многие downstream claims независимо подтверждают существование релевантных программ, но повторение не устанавливает независимо pandemic-producing incident.

## Institutional assessments

Разные government agencies также могут использовать общие intelligence streams. Пока common ancestry неизвестно, run не предполагал ни полной независимости, ни полной зависимости. Если underlying evidence classified, подтверждается само assessment, но его скрытая evidence base остаётся недоступной.

# Assumption sensitivity

Решающей sensitivity оказался не точный number of early spillovers. Wildlife family оставалась жизнеспособной даже при удалении two-introduction argument.

Самое load-bearing assumption — содержит ли Huanan evidence **какую-то информацию об upstream animal/trade entry process**, а не полностью ли объясняется downstream human amplification плюс ascertainment.

- Если Huanan wildlife/environment evidence действительно несёт upstream signal, wildlife/trade family сохраняет существенное evidential advantage.
- Если Huanan pattern полностью воспроизводится downstream amplification, human shedding и ascertainment, относительное преимущество резко уменьшается, и результат приближается к полной non-identification.

Для research-associated families главное допущение не в том, была ли такая работа возможна — это установлено, — а существовал ли event-specific precursor→exposure→infection bridge. Публичные данные этого не разрешают.

# Pairwise collisions

## Wildlife vs research-natural

**Различающий prediction:** wildlife ожидает прослеживаемый infected animal/supply-chain bridge; research-natural — аутентифицированный precursor в field/lab research плюс occupational infection bridge.

**Наблюдения, объяснимые обеими:** natural ancestry, non-engineered genome, Huanan amplification, post-closure market contamination.

**Текущее model preference:** wildlife/trade, потому что его positive evidence ближе во времени и пространстве к признанной ранней вспышке и не состоит только из capability.

**Flip observation:** near-progenitor в pre-outbreak research sample плюс надёжное exposure/infection evidence резко усилит research-natural; infected ancestral animal с traceable supply provenance — wildlife.

## Wildlife vs research-altered

**Различающий prediction:** wildlife ожидает animal/supply-chain bridge; research-altered — precursor holdings плюс construct/passage/intermediate records и exposure.

**Наблюдение с низкой discriminating value:** furin cleavage site сам по себе. Он не является уникальным marker ни одного route.

**Текущее model preference:** wildlife/trade.

## Research-natural vs research-altered

**Различающий prediction:** altered-virus models требуют evidence причинной alteration/adaptation history; natural-virus research exposure — нет.

**Текущий результат:** `UNDETERMINED` между ними при условии, что research-associated event вообще произошёл: public record не устанавливает event-specific precursor ни для одного пути и не показывает SARS-CoV-2-producing alteration chain.

# Second-opinion trigger

Fresh independent second opinion был запущен, потому что:

- apparent leading family существенно зависит от спорного и внутренне коррелированного Huanan evidence complex;
- решающие animal, early-human, laboratory и staff data остаются недоступными;
- ранняя phylogenetic evidence чувствительна к rooting и sampling;
- institutional assessments расходятся, а часть их evidence base непублична;
- цена over-attribution высока.

Second-opinion reviewer восстанавливал decisive inference из raw provenance и neutral candidate claims, не получая preferred winner.

Его вывод сохранил ключевое различие:

> **Wildlife/trade-associated natural entry — лучше всего поддержанное семейство в публичных данных, но evidence не замыкает причинную цепь достаточно сильно для окончательной family-level attribution.**

# Phase E — model judgment и evidence-sufficiency judgment

Convergence Guard требует формулировать их отдельно.

## Model judgment

**Лучше всего поддержанное семейство:** wildlife/trade-associated natural entry, при Huanan как крупном очень раннем amplification node.

Внутри этой семьи публичные данные **не позволяют надёжно различить**:

- first spillover непосредственно на Huanan;
- spillover выше по wildlife supply chain с последующим introduction на Huanan;
- более распределённый multi-spillover supply-network process.

Research-associated exposure к естественно существующему вирусу остаётся живой альтернативой, поскольку соответствующие field/laboratory exposure pathways существовали, а критические records для проверки события публично недоступны.

Research-associated altered/passaged/engineered routes также механистически возможны, но требуют дополнительного ненаблюдаемого причинного шага и сейчас имеют более слабую event-specific public support.

Outside/hybrid/unknown alternative остаётся открытым и не получает поддержки «по остаточному принципу».

## Evidence-sufficiency judgment

**`INSUFFICIENT DATA TO CHOOSE` для обоснованной причинной атрибуции pandemic-establishing route.**

Это **не** утверждение, что все families одинаково поддержаны.

Результат состоит из четырёх пунктов:

1. wildlife/trade family имеет наиболее сильное **относительное** public evidence;
2. его решающий animal→human bridge всё ещё не наблюдался напрямую;
3. ключевое evidence для проверки research-associated routes остаётся недоступным или отсутствует публично;
4. поэтому relative preference не достигает порога протокола для уверенной causal attribution.

Численные вероятности не назначались: public evidence не поддерживает такую точность.

# Популярные аргументы, ослабшие после provenance/discriminability проверки

### «Статистика доказала origin на Huanan, значит первый spillover произошёл там»

Слишком сильное утверждение. Huanan хорошо поддержан как early outbreak node; spatial clustering сам по себе не доказывает first infection site, а опубликованные критики показывают проблемы ascertainment и spatial identification.

### «Raccoon-dog DNA в positive swab доказывает заражённого raccoon dog»

Слишком сильное утверждение. Оно подтверждает co-location wildlife genetic material и SARS-CoV-2 в environmental sample, но не устанавливает, какой организм выделил viral RNA и каково было направление transmission.

### «Все 457 animal samples отрицательны — значит animal source не было»

Слишком сильное утверждение. Negative samples важны, но они собраны после закрытия рынка и не являются полным sample живых животных критического pre-closure периода или upstream supply chain.

### «Lineages A и B доказывают два zoonotic spillovers»

Аргумент слабее, чем выглядел в первоначальном варианте 2022 года. Corrected analysis всё ещё предпочитает multiple introductions, но code correction уменьшила Bayes-factor strength, а rooting disagreement остаётся material.

### «DEFUSE доказывает engineering SARS-CoV-2»

Нет. DEFUSE доказывает, что конкретные исследовательские идеи были предложены. Он не доказывает execution, создание SARS-CoV-2, exposure или pandemic seeding.

### «Furin cleavage site доказывает engineering»

Нет. Его можно обсуждать и в natural-evolution, и в laboratory scenarios, но по публичным данным он не является уникальным диагностическим признаком.

### «Нет явного engineering signature — значит laboratory route исключён»

Нет. Research-associated exposure к естественному вирусу вообще не требует engineering, а некоторые reverse-genetics approaches не обязаны оставлять простой диагностический signature.

### «Разведывательное агентство предпочитает X, значит X подтверждён»

Нет. Подтверждается то, что agency вынесло assessment с определённым stated confidence. Classified или иное недоступное support нельзя считать независимо проверенным evidence в публичном run.

# Наиболее ценное decision-changing evidence

Один practically attainable класс evidence имеет наибольшую ценность:

> **аутентифицированный pre-outbreak biological specimen с проверяемым provenance, raw sequence data и exposure metadata, который соединяет precursor с первым pandemic-establishing human infection.**

Для wildlife route это мог бы быть pre-closure animal или upstream supply-chain specimen с basal SARS-CoV-2/near-progenitor lineage и прослеживаемым путём к раннему human infection.

Для research-associated route — датированный pre-outbreak field/laboratory sample или construct с near-progenitor sequence плюс совпадающие worker exposure, seroconversion/clinical sequence, incident/access records и onward transmission link.

Такой класс evidence имеет значительно большую decision value, чем новые комментарии, новые institutional confidence statements или очередной reanalysis тех же post-closure market samples.

# Runtime integrity note

Run использовал fresh isolated worker contexts на этапах, где ценность процедуры зависела от blindness: causal search, screening, mapping, boundary review, finalist dossiers, slate adjudication и second opinion.

Runtime profile Chat On Steroids требует isolation smoke test. Один первоначальный parent-boundary smoke-test worker не успел вернуть результат и завершился по timeout. Граница была затем перепроверена; sibling isolation также проверялась; persistence positive control подтвердил, что revived workers сохраняют собственную историю и поэтому не должны повторно использоваться для blind roles. Первоначальный timeout здесь раскрывается явно, а не скрывается.

Во время recovery некоторые analytical roles повторялись в fresh contexts. Совпадение результатов повторных workers никогда не считалось independent real-world evidence; учитывались provenance и замороженные reasoning artifacts.

# Что этот пример показывает о методе

Главный методологический результат — не новое factual claim о SARS-CoV-2, а разделение утверждений, которые обычно незаметно сливаются:

> **Естественная bat-sarbecovirus ancestry поддерживается сильно.**  
> не означает  
> **pandemic-establishing infection произошёл через обычный wildlife trade.**  
> а это, в свою очередь, не означает  
> **точный first spillover произошёл на Huanan.**

Аналогично:

> **релевантные coronavirus research и exposure pathways существовали**  
> не означает  
> **research-associated infection вызвал пандемию.**

После устранения этих скрытых слияний публичные данные дают **relative preference** wildlife/trade family, но не проходят более строгий evidence-sufficiency threshold для causal attribution.

# Источники

1. WHO SAGO. *Independent assessment of the origins of SARS-CoV-2* (27 June 2025).  
   https://www.who.int/publications/m/item/independent-assessment-of-the-origins-of-sars-cov-2-from-the-scientific-advisory-group-for-the-origins-of-novel-pathogens
2. Worobey M. et al. *The Huanan Seafood Wholesale Market in Wuhan was the early epicenter of the COVID-19 pandemic*. *Science* 377 (2022). DOI: 10.1126/science.abp8715.  
   https://pmc.ncbi.nlm.nih.gov/articles/PMC9348750/
3. Pekar J.E. et al. *The molecular epidemiology of multiple zoonotic origins of SARS-CoV-2*. *Science* 377 (2022). DOI: 10.1126/science.abp8337.  
   https://pmc.ncbi.nlm.nih.gov/articles/PMC9348752/
4. *Erratum for “The molecular epidemiology of multiple zoonotic origins of SARS-CoV-2”*. *Science* 382 (2023). DOI: 10.1126/science.adl0585.  
   https://pmc.ncbi.nlm.nih.gov/articles/PMC13244787/
5. Liu W.J. et al. *Surveillance of SARS-CoV-2 at the Huanan Seafood Market*. *Nature* (2023).  
   https://www.nature.com/articles/s41586-023-06043-2
6. Crits-Christoph A. et al. *Genetic tracing of market wildlife and viruses at the epicenter of the COVID-19 pandemic*. *Cell* 187 (2024). DOI: 10.1016/j.cell.2024.08.010.  
   https://pmc.ncbi.nlm.nih.gov/articles/PMC11427129/
7. Stoyan D., Chiu S.N. *Statistics did not prove that the Huanan Seafood Wholesale Market was the early epicentre of the COVID-19 pandemic*. *JRSS A* 187 (2024).  
   https://academic.oup.com/jrsssa/article/187/3/710/7557954
8. Weissman M.B. *Proximity ascertainment bias in early COVID case locations*. *JRSS A* 187 (2024).  
   https://academic.oup.com/jrsssa/article/187/3/720/7632556
9. Hu B. et al. *Discovery of a rich gene pool of bat SARS-related coronaviruses provides new insights into the origin of SARS coronavirus*. *PLOS Pathogens* 13 (2017). DOI: 10.1371/journal.ppat.1006698.  
   https://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1006698
10. Temmam S. et al. *Bat coronaviruses related to SARS-CoV-2 and infectious for human cells*. *Nature* 604 (2022).  
    https://www.nature.com/articles/s41586-022-04532-4
11. Menachery V.D. et al. *SARS-like WIV1-CoV poised for human emergence*. *PNAS* 113 (2016). DOI: 10.1073/pnas.1517719113.  
    https://pubmed.ncbi.nlm.nih.gov/26976607/
12. Zeng L.P. et al. *Bat Severe Acute Respiratory Syndrome-Like Coronavirus WIV1 Encodes an Extra Accessory Protein, ORFX...* *Journal of Virology* (2016).  
    https://journals.asm.org/doi/10.1128/jvi.03079-15
13. Tse A.L. et al. *Bat sarbecovirus WIV1-CoV bears an adaptive mutation that alters spike dynamics and enhances ACE2 binding*. *PLOS Pathogens* (2025).  
    https://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1013123
14. EcoHealth Alliance. *Project DEFUSE* proposal (2018), public document copy.  
    https://usrtk.org/wp-content/uploads/2023/01/defuse-proposal.pdf
15. DARPA PREEMPT program-manager summary for the DEFUSE proposal, public document copy.  
    https://drasticresearch.org/wp-content/uploads/2021/09/hr00118s017-preempt-fp-019-pm-summary-selectable-not-recommended.pdf
16. Office of the Director of National Intelligence. *Potential Links Between the Wuhan Institute of Virology and the Origins of COVID-19* (23 June 2023).  
    https://archive.dni.gov/files/ODNI/documents/assessments/Report-on-Potential-Links-Between-the-Wuhan-Institute-of-Virology-and-the-Origins-of-COVID-19-20230623.pdf
17. Office of the Director of National Intelligence. Public release of additional COVID-origin materials (18 June 2026).  
    https://archive.dni.gov/index.php/newsroom/press-releases/press-releases-2026/4166-pr-11-26

---

**Граница case study:** этот файл фиксирует методологический run по публичным данным. Новое primary evidence, corrections к использованным исследованиям, новые released records или более сильная causal identification могут изменить результат. Convergence Guard — протокол decision analysis, а не источник научного авторитета.
