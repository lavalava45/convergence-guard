# Почему автономные AI-агенты ломаются на длительных реальных задачах: Full Mode case study Convergence Guard

[English version](long-running-autonomous-agents-full-mode.md)

> **Оговорка о границах case study.** Этот документ — worked example Convergence Guard, выполненный 06.10.2026 по публично доступным исследованиям и benchmark evidence. Это **не** контролируемое лабораторное исследование, проведённое авторами этого репозитория, не новый benchmark для агентов и не независимая репликация процитированных экспериментов. У run не было привилегированного доступа к неопубликованным benchmark traces, приватной production telemetry, внутренностям model providers или закрытым incident reports. Поэтому выводы документа описывают то, что поддерживается приведённым публичным evidence по правилам протокола, а не заменяют первичную экспериментальную работу.

## Вопрос

Почему современные автономные AI-агенты всё ещё становятся ненадёжными на длительных реальных задачах, где нужно долго планировать, пользоваться инструментами, понимать меняющееся состояние, проверять результат, сохранять память, восстанавливаться после ошибок и доводить работу до конца? Какие причинные механизмы лучше всего объясняют падение end-to-end reliability с ростом горизонта задачи и какой класс вмешательств следует приоритизировать?

Run должен был разделять:

1. **локальную способность** — может ли модель выбрать хороший следующий шаг в изоляции;
2. **надёжность системы** — остаётся ли последовательность шагов корректной и восстанавливаемой по мере изменения состояния;
3. **сложность задачи** — глубину зависимостей, ветвление, координацию и нагрузку на проверку;
4. **архитектуру runtime** — память, представление состояния, semantics инструментов, checkpoints, rollback, retries и handoffs.

Кроме того, было запрещено заранее считать, что «более длинная задача» сама по себе является достаточным причинным объяснением.

## Почему этот кейс полезен для Convergence Guard

Эта тема особенно подвержена преждевременной сходимости, потому что сразу несколько правдоподобных объяснений могут быть истинны одновременно:

- небольшие локальные ошибки могут накапливаться;
- планирование усложняется с ростом глубины зависимостей и ветвления;
- инструменты изменяют внешнее состояние, иногда необратимо;
- наблюдения могут быть устаревшими, неполными или двусмысленными;
- ошибка может долго оставаться незамеченной;
- context, memory и handoffs могут терять значимое для задачи состояние;
- дополнительный scaffold может как помогать, так и создавать новые failure surfaces;
- более сильная base model может улучшать capability без пропорционального роста reliability.

Обычный анализ легко превращает это в длинный список «причин», не отделяя root mechanisms от mediators, moderators и downstream symptoms.

Поэтому decision problem — не просто:

> Почему агенты ошибаются?

А:

> **Какая причинная структура предсказывает, когда локально способный агент превращается в ненадёжную long-horizon систему, и какое вмешательство остаётся полезным при разных сохранившихся causal models?**

# Phase A — evidence brief и decision contract

## Decision contract

**Decision question:** какие causal families лучше всего объясняют потерю end-to-end reliability по мере роста длительности и взаимозависимости автономных tool-using задач, и какое вмешательство следует приоритизировать при текущем evidence?

**Scope:** основной evidence base охватывает software, computer-use, web/API и benchmarked digital-agent tasks. Run может reframe «long horizon» через policy complexity, state continuity, observability и recovery, но не должен без оговорок переносить benchmark results на robotics, social systems или open-ended enterprise operations.

**Target phenomenon:** система часто умеет правильно выполнять короткие или локальные подзадачи, но ненадёжно завершает более длинную реальную задачу.

**Обязательная causal chain:** где возможно, объяснение должно разделять:

```text
требования задачи
→ первая существенная ошибка или расхождение состояния
→ обнаружение / verification
→ recovery, rollback, retry или replanning
→ продолжение
→ итоговый результат задачи
```

**Запрещённые подмены:**

- human task duration → буквальное число шагов агента;
- длинный context → доказательство, что root cause — память;
- высокий benchmark capability → высокая operational reliability;
- высокий single-run success → стабильная надёжность в повторных запусках;
- self-critique агента → надёжное обнаружение ошибок;
- больше inference или больше агентов → независимое evidence;
- позднее invalid action → корневая причина всей trajectory;
- успешное завершение → доказательство безопасной или внутренне корректной trajectory;
- интуиция `p^n` → установленная модель long-horizon failure;
- recovery на одном benchmark → универсальный механизм восстановления.

**Model-discrimination criterion:** сохранившаяся causal model должна давать различающие предсказания хотя бы по части следующих величин:

- вероятность первой consequential error;
- вероятность обнаружения ошибки;
- вероятность recovery;
- распространение ошибки на последующие шаги;
- чувствительность к mutability и observability состояния;
- чувствительность к dependency depth и branching;
- чувствительность к memory/handoff architecture;
- эффект verification, rollback, retry и replanning;
- итоговый task success при контролируемом изменении этих факторов.

**Action success criterion:** intervention лучше, если на matched tasks и при фиксированной model capability он уменьшает terminal failure и unsafe side effects, сохраняя приемлемые task quality, latency и cost. Улучшение, которое лишь переносит failures, скрывает их или увеличивает unrecoverable side effects, не считается success.

**Цена ошибки:** неправильный диагноз bottleneck может привести к дорогим, но слабым вмешательствам. Дополнительный planning compute мало помогает, если проблема — stale state после side effects; дополнительная память мало помогает, если first-error hazard определяется policy complexity; verification мало помогает, если verifier не умеет локализовать ошибку или действие нельзя обратить.

**Reversibility:** на раннем этапе предпочтительны interventions, которые можно внедрять, наблюдать и откатывать на orchestration/runtime layer без обязательства к irreversible model retraining или platform-wide architecture change. Production-wide redesign persistent state создаёт больший lock-in, чем targeted verification на selected commit boundaries.

**Analysis budget:** этот public case study ограничен inspectable evidence, доступным run на 06.10.2026, и не проводит новые benchmark experiments. Material source/provenance gaps могут вызвать targeted evidence checks; empirical questions, требующие новых controlled runs, остаются experiments и не заполняются дополнительной аргументацией.

## Claim-level source policy

Run рассматривал репутацию benchmark или статьи как metadata, а не как truth label.

Для material claims проверялось:

- что именно измеряется;
- benchmark task-level, step-level или trajectory-level;
- означает ли “horizon” wall-clock time, human task duration, число действий, token count или compositional depth;
- статична ли environment или mutable;
- автоматически ли проверяются failures;
- меняет ли intervention base model, scaffold или environment;
- возникает ли gain за счёт предотвращения первой ошибки, её обнаружения, восстановления или просто выбора лучшего run;
- переиспользуют ли разные источники одни и те же task families или evaluation assumptions;
- peer-reviewed ли результат, preprint или project report;
- поддерживает ли evidence причинность, корреляцию или только feasibility.

Роли источников использовались в смысле протокола: `EVIDENCE`, `CORROBORATION`, `CONTEXT`, `LEAD ONLY` и `UNSUPPORTED`.

### Source-role map для material uses

| Source group | Роль в этом run | Material use / dependency note |
|---|---|---|
| HCAST + METR | EVIDENCE / CORROBORATION | horizon-dependent success; из-за пересекающегося software-task framing не считаются полностью независимым evidence |
| HORIZON | EVIDENCE | controlled compositional-depth degradation и cross-domain failure patterns |
| Traverse | EVIDENCE | measurements first-error, detection, recovery, cascade и diffuse failures |
| ToolSandbox, τ-bench, τ²-bench | EVIDENCE / CORROBORATION | stateful tool use, repeated-run reliability и shared-state coordination |
| Rabanser et al. | CORROBORATION | разделение capability/reliability по нескольким reliability dimensions |
| DeepVerifier, GUI-RobustEval/RoTS | EVIDENCE | specialized verification и recovery как measurable intervention surfaces |
| Atomix, AgentRewind | EVIDENCE | transactional/checkpoint runtime mechanisms способны менять recovery outcomes |
| AMA-Bench | EVIDENCE | качество persistent memory зависит от causal/objective state representation, а не только от retrieval volume |
| MD5 state-tracking experiment | EVIDENCE (counterexample) | длинные dependent chains способны работать при controlled state/tool semantics; ослабляет “length alone” |
| UltraHorizon | CORROBORATION | extreme-horizon gap и evidence, что simple scaling alone недостаточен в этом benchmark |

## Основные factual anchors

### 1. Success резко падает на задачах с большей human-equivalent длительностью

HCAST содержит 189 software-related задач и 563 human baselines общей длительностью более 1 500 часов. В опубликованной оценке frontier agents успешно решали примерно **70–80%** задач, на которые skilled humans тратили менее часа, но **менее 20%** задач длительностью более четырёх человеческих часов.

Это сильное evidence существования horizon-dependent reliability gap в исследованном task distribution.

Но это **не** показывает, что сама elapsed duration является механизмом. Human completion time — proxy сложности и масштаба задачи, а не прямое число agent actions или state transitions.

Источники:

- [Rein et al., *HCAST: Human-Calibrated Autonomy Software Tasks* (2025)](https://arxiv.org/abs/2503.17354)
- [METR, *Task-Completion Time Horizons of Frontier AI Models* — обновление 08.05.2026](https://metr.org/time-horizons/)

Текущая методология METR использует более ста разнообразных software tasks и прямо указывает, что измерения выше 16 human-hours ненадёжны для имеющегося suite. Поэтому run рассматривал сам факт horizon degradation как более сильный вывод, чем точную универсальную границу «часов автономности».

### 2. Контролируемый compositional depth создаёт breaking regions, а не одну гладкую универсальную кривую

HORIZON спроектирован так, чтобы прямее варьировать intrinsic task horizon. Авторы собрали **3 100+ trajectories** в web navigation, operating systems, databases и embodied tasks, увеличивая dependency и compositional depth.

Наблюдаемая картина — не просто «больше шагов, чуть хуже». По мере роста compositional horizon performance входит в task-dependent breaking regions, а состав failures различается между доменами.

Это evidence против единственного объяснения через «context length» и в пользу семейства **policy-complexity / compositional breakpoint**.

Источник: [Wang et al., *The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break* (2026)](https://arxiv.org/abs/2604.11978).

### 3. После первой ошибки агент часто не обнаруживает её и не восстанавливается

Исследование Traverse 2026 года анализирует **2 518 agent trajectories** в software engineering, computer use и science и классифицирует **6 967 ошибок** в 78 failure types.

Trajectory-level результаты показывают повторяющуюся failure signature:

- после первой локализуемой ошибки агент восстанавливается лишь в **30,5%** применимых runs;
- в **38,5%** его собственное reasoning так и не отмечает ошибку;
- в **72,6%** он продолжает действовать или объявляет задачу завершённой, не исправив ошибку;
- в software engineering неправильный шаг сопровождается следующим неправильным шагом в **40,4%** случаев против **3,0%** после корректного шага — примерно **13,7×**;
- в computer use аналогичные значения — **58,1%** против **5,3%**, примерно **10,9×**.

Это прямое evidence того, что long-horizon failure часто **коррелирован и path-dependent**, а не является последовательностью независимых одинаковых trials.

При этом та же работа фиксирует важную границу: **588 failed runs, то есть 23% всех 2 518 trajectories, не имели единственной decisive first mistake**. Поэтому long-horizon reliability нельзя свести к универсальной теории «найди первую ошибку».

Источник: [Rahman et al., *Locating Hidden Failures Makes Long-Horizon Agents More Reliable* (2026)](https://arxiv.org/abs/2609.17930).

### 4. Feedback среды может быть не менее важен, чем self-awareness агента

Traverse показывает cross-domain contrast: software-engineering agents часто не замечают собственную ошибку, но всё же способны восстановиться, потому что tests, tracebacks, compiler errors и другие сигналы среды делают проблему видимой. Computer-use environments часто дают более слабую или неоднозначную обратную связь, и recovery там существенно хуже.

Это поддерживает модель **closed-loop state integrity**, где важной единицей является не отдельный reasoning step, а цикл:

```text
прочитать authoritative state
→ проверить предпосылки
→ выполнить действие
→ наблюдать последствия
→ проверить postconditions
→ исправить / откатить / перепланировать или продолжить
```

### 5. Stateful tool use сложнее stateless tool calling

ToolSandbox специально оценивает stateful execution, implicit dependencies между tool calls, on-policy conversation и промежуточные milestones. Авторы показывают, что задачи с **State Dependency**, **Canonicalization** и **Insufficient Information** остаются сложными даже для сильных моделей.

Результат mechanistically relevant для causal hypothesis: tool call может быть локально корректным, но глобально неверным, если выполнен против неправильного состояния, в неправильном порядке или без информации, которую следовало получить раньше.

Источник: [Lu et al., *ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities*, Findings of NAACL 2025](https://aclanthology.org/2025.findings-naacl.65/).

### 6. Надёжность повторных запусков может оставаться слабой даже при приемлемом pass@1

В τ-bench state-of-the-art function-calling agents в исходной оценке завершали **менее 50%** задач, а repeated-run consistency была заметно хуже: retail `pass^8` оказался ниже **25%**.

Это отделяет «агент иногда умеет решить задачу» от «система надёжна при повторении задач этого класса».

Источник: [Yao et al., *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains*, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b126cc38b8638e07bef37e7b2bb72bf-Abstract-Conference.html).

### 7. Shared mutable state и coordination создают отдельную failure surface

τ²-bench расширяет setting так, что и агент, и пользователь могут воздействовать на общую dynamic environment. В telecom domain переход от no-user control к **dual control** приводит к заметному падению performance.

Benchmark отдельно анализирует reasoning errors и communication/coordination errors. Поэтому система может ломаться даже при локальной компетентности участников: они расходятся в представлении о том, кто что изменил, какое действие уже произошло и какое состояние теперь действительно.

Источник: [Barres et al., *τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment*, ICML 2026](https://proceedings.mlr.press/v306/barres26a.html).

### 8. Reliability не растёт автоматически вместе с headline capability

Rabanser et al. определяют двенадцать metrics по consistency, robustness, predictability и safety и оценивают **15 models** на двух agent benchmarks. Центральный результат: недавние capability gains дали лишь **небольшие улучшения reliability** по этим измерениям.

Это ослабляет гипотезу, что long-horizon problem решится просто с появлением более сильной next-token policy.

Источник: [Rabanser et al., *Towards a Science of AI Agent Reliability*, ICML 2026](https://proceedings.mlr.press/v306/rabanser26a.html).

### 9. Специализированная verification помогает, но generic self-judgment недостаточен

DeepVerifier использует rubric-guided verification для deep-research agents. По опубликованным результатам verifier превосходит vanilla agent-as-judge и LLM-judge baselines на **12–48%** по meta-evaluation F1 и даёт **8–11% accuracy gains** на сложных subsets GAIA и XBench-DeepResearch при iterative test-time refinement с сильными closed-source models.

Traverse независимо показывает, что общие frontier judges плохо локализуют первую ошибку: даже лучший из оценённых judges правильно находит first mistake менее чем в трети organic-failure runs.

Совместно эти результаты поддерживают два утверждения:

1. verification — реальная intervention surface;
2. «попросить сильную модель проверить trajectory» ещё не означает надёжный verifier.

Источники:

- [Wan et al., *Inference-Time Scaling of Verification: Self-Evolving Deep Research Agents via Test-Time Rubric-Guided Verification*, Findings of ACL 2026](https://aclanthology.org/2026.findings-acl.1243/)
- [Rahman et al., Traverse (2026)](https://arxiv.org/abs/2609.17930)

### 10. Recovery можно измерять и тренировать отдельно

GUI-RobustEval содержит **1 216 executable test cases** для измерения восстановления после policy-induced GUI errors. Связанный robustness-driven trajectory synthesis специально обучает recovery behavior.

RoTS-32B сообщает **47,4% success на OSWorld** и **33,8% All-Pass@4**, демонстрируя более сильное recovery behavior относительно сравниваемого open baseline.

Причинно важен не сам leaderboard score, а то, что recovery можно выделить как отдельную trainable и measurable capability, а не прятать внутри final success.

Источник: [Bu et al., *Recovering Policy-Induced Errors: Benchmarking and Trajectory Synthesis for Robust GUI Agents*, ICML 2026](https://proceedings.mlr.press/v306/bu26b.html).

### 11. Transactional tool semantics способны предотвращать усиление ошибок через внешние side effects

Atomix рассматривает multi-step tool effects почти как transactions: calls отслеживаются, часть effects можно задерживать, commit можно связывать с progress conditions, а уже externalized effects — компенсировать при abort.

При fault injection авторы сообщают, что transactional retry повышает task success, а progress-aware commit усиливает isolation при speculation и contention.

Это не доказывает, что каждому агенту нужна database-style transaction system. Но показывает, что часть внешне «reasoning failures» можно превратить в recoverable execution failures, изменив semantics вокруг state mutation.

Источник: [Mohammadi et al., *Atomix: Timely, Transactional Tool Use for Reliable Agentic Workflows* (2026)](https://arxiv.org/abs/2602.14849).

### 12. Checkpointing и agent context, и environment state может улучшать recovery

AgentRewind сохраняет согласованные checkpoints agent context и controlled environment state, после чего позволяет системе вернуться к более ранней точке и продолжить execution, сохранив полезную информацию из неудачной попытки.

На long-horizon engineering benchmark и исследованных configurations авторы сообщают улучшение task success и checklist progress относительно сравниваемых baselines.

Это evidence в пользу того, что recovery — архитектурная проблема: одного rewind текста недостаточно, когда внешний мир уже изменён.

Источник: [Zhuang et al., *AgentRewind: Recoverable Execution for Long-Horizon LLM Agents* (2026)](https://arxiv.org/abs/2608.14380).

### 13. Длинная память не равна хорошему представлению состояния

AMA-Bench оценивает agent memory по trajectories, состоящим из states, actions, observations и tool outputs. Авторы сообщают, что существующие memory systems работают хуже, в частности потому, что теряют **causal and objective information** и слишком зависят от lossy similarity retrieval.

Их causality-graph + tool-augmented AMA-Agent достигает **57,22%** accuracy — на **11,16 percentage points** выше strongest reported baseline.

Это поддерживает persistent-state family, но сужает её: проблема не просто в том, чтобы «помнить больше tokens», а в сохранении task-relevant структуры, необходимой для восстановления текущего state и unresolved obligations.

Источник: [Zhao et al., *AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications*, ICML 2026](https://proceedings.mlr.press/v306/zhao26bs.html).

### 14. Контролируемая задача из 196 calls — counterexample к тезису «сама длина неизбежно ломает систему»

Preprint 2026 года проверяет exact state tracking, заставляя модель вычислять MD5 через **196 зависимых tool calls в 64 rounds**, при этом каждое intermediate state сверяется с ground-truth trace.

В опубликованном setup gpt-oss-120b переносил состояние через всю цепочку и возвращал корректный digest в большинстве завершённых deterministic-tool runs.

Эксперимент узкий и мало похож на open-ended real-world task. Именно поэтому он полезен: он показывает, что **длинная зависимая цепочка сама по себе недостаточна для failure**, если interpretation проста, state точен, tools контролируются, а verification сильна.

Источник: [Pai & Xian, *Long-Horizon State Tracking in LLMs: Executing MD5 through a Deep Sequence of Dependent Tool Calls* (2026)](https://arxiv.org/abs/2609.00012).

### 15. Ultra-long-horizon benchmarks сохраняют разрыв даже при попытке простого scaling

UltraHorizon оценивает long-horizon partially observable exploration tasks. В standard configurations trajectories в среднем превышают **35k tokens и 60 tool calls**, а в самых тяжёлых settings — **200k tokens и 400 tool calls**.

Авторы сообщают, что state-of-the-art agents существенно отстают от humans, simple scaling не решает benchmark, а наблюдаемые failures группируются вокруг in-context locking и фундаментальных capability gaps.

Это поддерживает сохранение нескольких causal families: часть failures архитектурна и связана с recoverability, а часть отражает реальные ограничения policy capability.

Источник: [Luo et al., *UltraHorizon: Benchmarking Agent Capabilities in Ultra Long-Horizon Scenarios*, ICML 2026](https://proceedings.mlr.press/v306/luo26ai.html).

# Phase A reframe — что именно является «horizon problem»?

Outside-view check изменил постановку.

Наивная формулировка:

> Чем больше шагов, тем больше возможностей ошибиться; значит, длинные задачи ломаются потому, что ошибки перемножаются.

Направление интуитивно разумно, но причинно неполно. Если бы каждый шаг имел независимую вероятность корректности `p`, success для `n` шагов мог бы напоминать `p^n`. Но evidence нарушает предпосылки такой toy model:

- ошибки становятся **коррелированными** после первой ошибки;
- некоторые mistakes recoverable, другие — нет;
- некоторые environments быстро показывают ошибку, другие скрывают её;
- часть failures diffuse и не имеет одной first mistake;
- task complexity способна нелинейно расти с dependency depth;
- shared state и side effects создают path dependence;
- длинные deterministic chains могут работать при строгом state tracking и verification.

Поэтому run переопределил terminal failure как взаимодействие как минимум двух hazards:

1. **попадание в плохую trajectory** — вероятность material planning, reasoning, coordination, perception или execution error;
2. **неспособность локализовать ошибку** — вероятность, что система не обнаружит, не обратит, не компенсирует или не перепланирует её до того, как ошибка загрязнит дальнейшее state.

Третий фактор определяет persistence во времени и между actors:

3. **потеря task state** — вероятность того, что система больше не хранит верное представление о том, что истинно, сделано, ожидается, проверено и кому принадлежит.

Это концептуальная decomposition, а не fitted probabilistic law.

# Phase B — isolated causal search

Завершённый run использовал четыре причинно различные search regions. Публичный текст суммирует mandates и не воспроизводит worker-specific reasoning.

## Mandate 1 — error propagation, observability и recovery

Искать механизмы, при которых локально переживаемая ошибка становится terminal, потому что:

- environment её не раскрывает;
- агент её не замечает;
- verification запаздывает или слабая;
- side effects меняют последующие preconditions;
- rollback или compensation недоступны;
- replanning начинается уже из corrupted state.

Эта region дала модели post-first-error cascade, weak observability, transactionality и recovery capacity.

## Mandate 2 — effective policy complexity

Искать failure, сохраняющийся даже в относительно static, observable и reversible environments.

Фокус:

- dependency depth;
- branching и contingent planning;
- decomposition;
- search по action sequences;
- long-range constraints;
- plan adaptation;
- распределение test-time reasoning compute.

Эта region дала модель **policy-complexity breakpoint**: после task-dependent порога policy перестаёт строить или поддерживать достаточно хороший action plan ещё до того, как state corruption становится главной проблемой.

## Mandate 3 — persistent state, memory и coordination architecture

Искать механизмы, где проблема — не один bad local action, а потеря согласованного представления о:

- текущем world state;
- выполненной работе;
- unresolved obligations;
- causal dependencies;
- ownership и handoff state;
- уже проверенном;
- том, что нельзя повторять.

Эта region включала memory systems, externalized state, checkpointing, context compaction, shared-state coordination и handoffs.

## Mandate 4 — разделение capability/reliability и counterexamples

Coverage gate сохранил дополнительную region, потому что первые три иначе могли бы сделать horizon degradation самоочевидным.

Она искала:

- длинные chains, которые **работают**;
- случаи, где stronger models улучшают local capability, но не reliability пропорционально;
- benchmark confounds;
- различие human duration и agent action horizon;
- interventions, меняющие runtime semantics без изменения model weights.

MD5 state-tracking result, reliability work и transactional/recovery studies были особенно важны, потому что не позволяют превратить «long = doomed» в нефальсифицируемое объяснение.

## Coverage gate

После четвёртой region coverage признано достаточным, потому что в candidate space присутствовали:

- генерация first error;
- propagation и containment ошибок;
- mutable-state / partial-observability effects;
- persistent-memory и coordination effects;
- policy-complexity limits;
- runtime/scaffold effects;
- counterexamples к length-only explanations.

Дополнительная ветка не создавала бы materially different causal region.

# Phase C — neutral candidates, screening и blind causal mapping

Candidate wording была neutralized перед reduction. Screening и causal mapping в исходном run выполнялись как отдельные fresh operations.

## Screening result

Сохранились три различимых model families:

- **F1 — CLOSED-LOOP STATE INTEGRITY**
- **F2 — EFFECTIVE POLICY-COMPLEXITY BREAKPOINT**
- **F3 — PERSISTENT-STATE & COORDINATION ARCHITECTURE**

Чистая independent-`p^n` accumulation model осталась лишь как слабая baseline intuition, а не finalist.

Чистая модель «context window size» не сохранилась как отдельное family, потому что memory effects лучше описывались F3, а длинные контролируемые sequences способны работать.

Чистая модель «tool unreliability» также была понижена: tool failures важны, но более сильное причинное различие — изменяет ли failure canonical state и умеет ли система его обнаружить и исправить.

## Blind causal map

### F1 — CLOSED-LOOP STATE INTEGRITY

**Claim:** в большом классе state-changing tasks главная потеря long-horizon reliability возникает потому, что локальные ошибки или stale assumptions сохраняются в canonical state без достаточно быстрого detection, verification, rollback, retry или replanning.

**Core mechanism:**

```text
state estimate
→ action
→ external state mutation
→ incomplete / stale observation
→ undetected mismatch
→ последующие решения опираются на неверный state
→ correlated cascade
```

**Основные predictions:**

- wrong steps резко повышают downstream error risk;
- richer environment feedback улучшает recovery;
- postcondition checks уменьшают terminal failure даже без изменения base model;
- rollback/compensation особенно важны вокруг state-changing actions;
- одна и та же policy работает лучше в instrumented reversible environments, чем в opaque irreversible environments.

### F2 — EFFECTIVE POLICY-COMPLEXITY BREAKPOINT

**Claim:** часть long-horizon degradation вызвана нелинейным ростом сложности построения и адаптации policy по мере роста dependency depth, branching, constraints и subgoal interactions.

**Core mechanism:**

```text
больше взаимозависимых obligations
→ более крупная effective policy/search problem
→ decomposition или planning quality пересекает task-dependent threshold
→ вероятность первой material error резко растёт
```

**Основные predictions:**

- sharp break может сохраняться в static, fully observable, reversible tasks;
- рост dependency depth вреднее, чем добавление такого же объёма независимой работы;
- дополнительная state verification помогает после ошибок, но не убирает рост first-error hazard;
- hierarchical planning или targeted test-time search сдвигают breakpoint.

### F3 — PERSISTENT-STATE & COORDINATION ARCHITECTURE

**Claim:** длинные задачи становятся ненадёжными, когда система не имеет durable causally meaningful representation состояния, commitments, progress, ownership и unresolved requirements на переходах context growth, handoff, retry или multi-actor work.

**Core mechanism:**

```text
history grows / actors change / context compacted
→ task-relevant state неполно summarised, retrieved или handed off
→ current belief state расходится с canonical task/world state
→ duplicated, omitted, conflicting или misordered work
→ terminal inconsistency
```

**Основные predictions:**

- failures учащаются вокруг compaction, resume, handoff и multi-actor boundaries;
- explicit persistent state помогает даже без усиления base-model reasoning;
- causally structured memory лучше similarity-only retrieval на stateful tasks;
- coordination failures появляются, когда несколько parties могут менять shared state.

## Relations between finalists

Mapper определил эти families в основном как **INTERACTING**, а не mutually exclusive.

Типичная causal composition:

```text
F2 повышает hazard первой consequential error
          ↓
F1 определяет, будет ли ошибка обнаружена и локализована
          ↓
F3 определяет, сохранится ли coherent state во времени, retries и handoffs
```

Вес семейства зависит от task class. Static theorem-search или code-design problem может сильнее зависеть от F2. GUI или operational workflow с irreversible side effects — от F1. Multi-session или multi-actor workflow — от F3.

## Boundary audit

Главный boundary question: не являются ли F1 и F3 дубликатами.

Они оставлены отдельно, потому что дают разные predictions:

- F1 способен сломаться в одном uninterrupted session с идеальной памятью, если система действует по stale state и не проверяет последствия.
- F3 способен сломаться при локально проверенных действиях, если система теряет durable representation commitments или ownership между handoffs и context transitions.

F2 также не объединён с F3, потому что policy complexity может создать breakpoint в static environment с контролируемой memory и external state.

# Phase D — independent finalist dossiers

## Finalist A — closed-loop state integrity

### Mechanism

Long-running agent — feedback controller внутри изменяющейся environment. Он не просто генерирует текст: он многократно оценивает state, выбирает actions, наблюдает consequences и обновляет beliefs.

Reliability падает, когда этот loop остаётся open или weakly closed:

1. агент действует по неполному state estimate;
2. tool, user или environment меняют мир;
3. агент получает неоднозначное, задержанное или частичное evidence результата;
4. не перечитывает authoritative state;
5. не проверяет postcondition;
6. downstream decisions наследуют mismatch;
7. recovery дорожает по мере накопления side effects.

### Strongest support

- Traverse прямо измеряет correlated post-error cascades и низкий recovery.
- ToolSandbox показывает сложность implicit state dependencies.
- τ²-bench показывает degradation, когда другой actor способен менять shared state.
- GUI-RobustEval выделяет recovery как отдельную measurable capability.
- Atomix и AgentRewind показывают, что commit, rollback, compensation и checkpoint semantics могут менять outcomes без изменения underlying model.

### Strongest contrary evidence / limitations

- Многие failures начинаются с reasoning/planning errors ещё до consequential state mutation.
- Существенная часть failed trajectories не имеет одной localizable first mistake.
- HORIZON показывает breaking regions, где сама policy complexity существенна.
- Более сильная verification может быть дорогой и сама ошибаться.

### Что эта модель объясняет лучше ближайших конкурентов

Она объясняет, почему локально способный агент может катастрофически сломаться после одного wrong action и почему одна и та же policy ведёт себя по-разному в environments с сильным и слабым feedback.

### Что она не объясняет уникально

Она не объясняет, почему вероятность **первой** material error растёт с compositional depth в static tasks. Также сама по себе не объясняет state loss через длинные pauses или handoffs.

### Что materially усилит модель

Контролируемый эксперимент, где при фиксированной policy complexity authoritative, observable, verifiable и reversible state резко уменьшает terminal failure и downstream error multiplier.

### Что materially ослабит модель

Результат, при котором long-horizon failure почти не меняется после полного state observability, postcondition checking всех consequential actions и безопасной reversibility failed actions.

## Finalist B — effective policy-complexity breakpoint

### Mechanism

Агент должен строить policy над interacting subgoals, constraints, branches и future dependencies. По мере роста effective search/composition problem ранее достаточная reasoning policy может пересечь нелинейный threshold.

Важная переменная — не raw chain length, а сложность поддержания globally coherent policy.

### Strongest support

- HORIZON специально повышает task composition и показывает horizon-dependent breaking behavior.
- UltraHorizon показывает persistent gaps и capability-limited failure в long-horizon-focused evaluation.
- MD5 counterexample показывает, что длинная dependency chain может работать при очень регулярной policy и exact state, ослабляя «length alone», но сохраняя complexity как real variable.
- Traverse показывает, что reasoning/planning errors непропорционально часто выступают originating mistakes, хотя action errors доминируют в позднем visible cascade.

### Strongest contrary evidence / limitations

- Benchmark extension levels остаются proxies реальной task complexity.
- Failure taxonomies часто классифицируют observable failure, а не fundamental bottleneck.
- Better runtime feedback способен спасти trajectories с planning errors, поэтому policy quality не определяет terminal outcome в одиночку.
- Model и scaffold changes часто confounded.

### Что эта модель объясняет лучше ближайших конкурентов

Она объясняет, почему performance может collapse ещё до крупного state-corruption event и почему verification не способна полностью спасти policy, которая не умеет построить viable plan.

### Что она не объясняет уникально

Она не объясняет большие cross-environment differences в recovery после сходных local errors и большие gains от checkpoint/transaction mechanisms под injected faults.

### Что materially усилит модель

Factorial benchmark, где dependency depth или branching сильно повышают **first-material-error probability** даже при static, fully observable, reversible и continuously verified state.

### Что materially ослабит модель

Результат, где apparent breakpoint в основном исчезает после контроля state observability и recovery, то есть «planning complexity» оказывается proxy накопленного state divergence.

## Finalist C — persistent-state & coordination architecture

### Mechanism

Long-running system нужна durable representation того, что истинно сейчас, что уже сделано, что осталось, какие constraints действуют и какой actor отвечает за obligation.

Одного raw transcript недостаточно. Similarity-based retrieval также может быть недостаточно. Architecture должна сохранять causally relevant state через:

- context growth;
- compaction;
- retries;
- restart/resume;
- worker handoff;
- user-agent coordination;
- multiple agents;
- external system updates.

### Strongest support

- AMA-Bench показывает слабость существующих long-horizon memory systems и пользу causality-structured memory.
- τ²-bench показывает shared-state coordination difficulty.
- AgentRewind улучшает outcomes checkpointing'ом и context, и environment state.
- ToolSandbox показывает важность implicit state dependencies.
- Long-horizon multi-actor settings создают failures, которые нельзя свести к local next-step competence одной модели.

### Strongest contrary evidence / limitations

- Некоторые single-session failures возникают без очевидной memory/handoff проблемы.
- MD5 result показывает, что exact state можно пронести через длинную chain в узком controlled setting.
- Persistent memory способна сохранять неверные beliefs так же хорошо, как верные.
- External state stores могут создавать stale или contradictory sources of truth при слабой commit semantics.

### Что эта модель объясняет лучше ближайших конкурентов

Она объясняет omissions, duplicated work, stale commitments, inconsistent handoffs и coordination failures, способные пережить local verification.

### Что она не объясняет уникально

Она не объясняет, почему single agent с perfect persistent state всё ещё может упереться в planning breakpoint и почему один wrong external action может каскадировать даже при отличной memory.

### Что materially усилит модель

Контролируемый эксперимент, показывающий, что externalized causal state и explicit handoff/ownership records существенно снижают failures при фиксированных model, task complexity и verification policy.

### Что materially ослабит модель

Результат, где persistent-state architecture почти не влияет после контроля policy complexity и closed-loop recovery.

# Shared-bias и source-dependency audit

## Концентрация на software и computer-use

HCAST, METR time-horizon work, SWE-style trajectories, OS tasks и несколько recovery studies сильно смещены в сторону software/computer-use environments.

Это делает evidence особенно релевантным coding и digital operations, но слабее переносимым на robotics, long-running social interaction, multi-user enterprise work и scientific field operations.

## Зависимость от определения benchmark

“Horizon” означает разные вещи:

- HCAST / METR: human task duration;
- HORIZON: intrinsic/compositional task horizon;
- Traverse: trajectory structure и first-error localization;
- MD5: exact dependent tool-call depth;
- τ / τ²: multi-turn stateful interaction;
- UltraHorizon: очень большие token/tool-call trajectories при partial observability.

Согласованность результатов полезна, но эти измерения нельзя выдавать за взаимозаменяемые оценки одной latent quantity.

## Зависимость от failure taxonomy

Несколько исследований используют human или LLM-assisted labels вроде planning, memory, environment, action и reasoning failure. Они полезны описательно, но не дают автоматической causal identification.

Поздний “invalid action” может быть symptom более раннего wrong state estimate. “Planning error” может быть downstream от missing information. Поэтому run использовал taxonomy как evidence о том, **где проявляются failures**, а не как прямое доказательство fundamental cause.

## Scaffold confounding

Model, prompting, tools, memory, retry policy и orchestrator часто меняются одновременно.

Поэтому benchmark score измеряет **agent system**, а не чистое свойство foundation model. Это одна из причин, почему финальный judgment отделяет policy capability от system reliability.

## Intervention-study selection

DeepVerifier, RoTS, AgentRewind и Atomix вмешиваются каждый в свою failure surface. Их положительные результаты показывают, что поверхность actionable, но не доказывают, что она является dominant bottleneck для любого task class.

## Preprint против peer-reviewed evidence

Часть наиболее прямых работ 2026 года — Traverse, HORIZON, Atomix, AgentRewind и MD5 state-tracking experiment — на момент run была публичными preprints. Peer-reviewed работы ICML/ACL/NAACL/ICLR получали более сильный provenance status там, где claims пересекались, но один только preprint-status не использовался как причина отбросить evidence.

## Survivorship и terminal-score bias

Pass/fail metrics способны скрывать unsafe или incorrect intermediate behavior. И наоборот, анализ только failed trajectories скрывает recoverable mistakes.

Traverse особенно полезен, потому что отдельно рассматривает mistakes, recovery и final outcome, но даже его first-mistake analysis сознательно не покрывает diffuse failures без unique turning point.

# Assumption sensitivity

## Assumption 1 — «Проблема в основном сводится к independent per-step error multiplication»

**Result: THREATENED.**

Интуиция `p^n` объясняет хрупкость длинных chains, но Traverse показывает сильную conditional dependence после errors, а MD5 даёт узкий counterexample, где 196-call dependent sequence часто завершается успешно при tightly controlled state и tool semantics.

Relevant errors не являются ни одинаковыми, ни независимыми.

## Assumption 2 — «У каждого failed run есть одна decisive first mistake»

**Result: FAIL как универсальная предпосылка.**

Traverse фиксирует сотни failed trajectories без одной localizable decisive first mistake. Надёжная architecture должна работать и с discrete faults, и с gradual drift.

## Assumption 3 — «Более сильная base model в основном решит reliability»

**Result: THREATENED.**

Capability растёт, но ICML reliability study показывает лишь небольшие reliability gains по нескольким operational dimensions, а UltraHorizon — persistent failure при simple scaling.

Это не означает, что scaling бесполезен. Это означает, что model scaling и reliability engineering — разные intervention levers.

## Assumption 4 — «Verification дешёвая и надёжная»

**Result: THREATENED.**

Generic frontier judges плохо локализуют trajectory errors. Specialized verification способна улучшить results, но требует inference и сама имеет false positives, false negatives и latency.

Поэтому verification должна быть **risk-adaptive**, а не автоматически выполняться после каждого trivial action.

## Assumption 5 — «Rollback решает recovery»

**Result: CONDITIONAL.**

Rollback силён только тогда, когда relevant state действительно можно восстановить или компенсировать. External writes, messages, payments, user actions и irreversible operations требуют transaction boundaries или compensating semantics, а не просто восстановления LLM transcript.

# Pairwise collisions

## F1 closed-loop state integrity vs F2 policy-complexity breakpoint

**Decision-conflicting prediction:** что произойдёт, если task complexity возрастает, но environment остаётся static, fully observable, continuously verified и reversible?

- **F1** предсказывает, что значительная часть terminal-failure growth будет подавлена, потому что mistakes не смогут незаметно загрязнять дальнейший canonical state.
- **F2** предсказывает, что существенный first-error breakpoint сохранится, потому что построение policy всё равно усложняется с dependency depth и branching.

Текущее evidence поддерживает оба эффекта. HORIZON и UltraHorizon сохраняют F2; Traverse, ToolSandbox, RoTS, Atomix и AgentRewind показывают, что containment сильно меняет terminal outcomes.

**Collision result:** ни одна модель не доминирует универсально. F2 лучше объясняет **entry into error** при controlled state; F1 — **превращение ошибки в terminal failure** в mutable environment.

## F1 closed-loop state integrity vs F3 persistent-state architecture

**Decision-conflicting prediction:** должен ли reliability ухудшаться в одном uninterrupted session без handoff/compaction, но с consequential side effects и слабыми postcondition checks?

- **F1:** да — достаточно stale или unverified external state.
- **F3:** сильнейший эффект ожидается вокруг persistence boundaries: compaction, resume, handoff, multi-actor coordination.

И наоборот, если каждое local action хорошо verified, но задача многократно проходит handoff/compaction boundaries, F3 предсказывает failures, которые F1 одна не объясняет.

**Collision result:** F1 и F3 различимы, но complementary. F1 — про **control-loop integrity вокруг actions**; F3 — про **continuity canonical task state во времени и между actors**.

## F2 policy-complexity breakpoint vs F3 persistent-state architecture

**Decision-conflicting prediction:** если той же highly compositional task дать external causal state ledger с perfect persistence, но не усилить planning policy, исчезнет ли breakpoint?

- **F3:** большая доля long-horizon failures должна уйти, если dominant были lost obligations, stale summaries и handoff inconsistency.
- **F2:** существенный breakpoint должен сохраниться, если policy по-прежнему не умеет синтезировать или адаптировать coherent plan над dependency structure.

**Collision result:** текущего evidence недостаточно, чтобы количественно разделить вклад. AMA-Bench поддерживает F3; HORIZON и UltraHorizon — F2. В reviewed sources этого run нет достаточно крупного исследования, независимо варьирующего обе переменные.

# Slate-level adjudication

Adjudication отверг premise, что evidence поддерживает одну универсальную root cause.

Три finalists описывают разные части failure process:

| Family | Лучшее толкование | Main causal locus |
|---|---|---|
| F1 — Closed-loop state integrity | errors становятся опасными, потому что state divergence не обнаруживается и не локализуется | error propagation / recovery |
| F2 — Policy-complexity breakpoint | вероятность первой material error растёт с effective planning complexity | error generation |
| F3 — Persistent-state & coordination architecture | система теряет верное представление commitments и state во времени/между actors | state continuity |

Поэтому adjudicator рассматривает families как **interacting и task-class dependent**.

Самое сильное общее causal statement, поддерживаемое evidence:

> Long-horizon agent failure плохо объясняется одной длиной задачи. Reliability падает, когда растущая policy complexity повышает вероятность входа в плохую trajectory, а imperfect observability, verification, recoverability и persistent-state architecture определяют, будет ли эта ошибка локализована или усилена.

Это уже и точнее, и уже, чем утверждение, что один механизм является «главной причиной».

## Second-opinion trigger

В исходном run был triggered независимый blind second opinion, потому что pairwise adjudication оставил global dominance relation между двумя сильнейшими широкими объяснениями unresolved: evidence для universal winner оставалось слабым, а правдоподобный counterfactual мог сдвинуть relative weight между upstream policy-complexity failure и downstream closed-loop state/recovery failure. В терминах текущего протокола это weak-winner / unresolved-comparison trigger.

Second opinion **не** установил universal winner. Независимый reviewer сохранил task-class-dependent трактовку и признал публичное evidence недостаточным, чтобы выбрать один из этих механизмов как globally dominant.

Он также сохранил ту же практическую асимметрию:

- прямого head-to-head evidence, показывающего, что closed-loop verification/recovery универсально сильнее как causal fix, чем better planning, нет;
- однако targeted closed-loop control на state-changing или commit boundaries остаётся более robust **near-term engineering action**, потому что ограничивает propagation при нескольких surviving causal models.

Это подтверждение рассматривалось как robustness check inference, а не как дополнительное real-world evidence.

# Phase E — model judgment, action judgment и evidence sufficiency

## Model judgment

Evidence **недостаточно, чтобы выбрать одно universal causal family** как dominant explanation для всех long-running real-world agent tasks.

Лучшая поддержанная структура — interaction:

```text
effective policy complexity
        ↓
first-error / drift hazard
        ↓
closed-loop detection and containment
        ↓
persistent-state continuity во времени и между actors
        ↓
terminal reliability
```

Вес каждого этапа меняется между tasks.

В static, но combinatorially difficult task может доминировать F2. В operational workflow с external side effects — F1. В multi-session или multi-actor work F3 может стать load-bearing.

## Action judgment

Несмотря на отсутствие universal causal winner, evidence достаточно, чтобы приоритизировать одно **cross-model engineering intervention**:

> **Добавлять risk-adaptive closed-loop control вокруг state-changing actions.**

Практически:

1. **Перед consequential action читать authoritative state.**
2. **Явно представлять intended postcondition.**
3. **Где возможно, выполнять действие через idempotent, transactional или compensatable semantics.**
4. **После action повторно читать authoritative state.**
5. **Проверять postcondition способом, достаточно независимым от action-generation path, когда stakes это оправдывают.**
6. **При mismatch останавливать propagation и выбирать retry, rollback, compensation или replanning.**
7. **Checkpoint durable task state на meaningful commit boundaries.**

Это не означает «verify всё после каждого шага». Цена verification должна масштабироваться с:

- irreversibility;
- blast radius;
- observability;
- downstream dependency;
- стоимостью rollback;
- uncertainty текущего state estimate.

### Сравнение feasible actions

Run качественно сравнил четыре near-term action classes по surviving models:

| Action | Expected downside / regret при ошибочном выборе | Reversibility / lock-in | Option & information value | Cross-model fit |
|---|---|---|---|---|
| **A1. Risk-adaptive closed-loop verification/recovery на consequential boundaries** | дополнительные tool calls, latency, verifier mistakes; может не снижать генерацию first errors | высокая reversibility при добавлении на orchestration boundaries; можно внедрять постепенно | высокая: даёт trajectory evidence о detection/recovery и одновременно ограничивает propagation | прямо полезен при F1; защищает при F2; создаёт commit/checkpoint substrate для F3 |
| **A2. Сначала stronger planning / больше test-time reasoning** | можно потратить значительный compute, не исправив stale-state и recovery failures | умеренно reversible, но cost масштабируется на каждый run | средняя: показывает сдвиг first-error hazard, но слабее защищает после errors | сильнее всего при F2; слабее защищает при F1/F3 |
| **A3. Сначала redesign persistent memory / coordination state** | архитектурная сложность; риск сохранять wrong beliefs или создать competing sources of truth | ниже reversibility и выше integration lock-in, чем у A1 | высокая для handoff/memory questions, но медленнее и system-specific | сильнее всего при F3; неполно для F1/F2 |
| **A4. Проверять каждый шаг / добавить blanket redundancy** | высокая latency и cost; false alarms; можно умножить correlated judgments без улучшения state integrity | технически reversible, но operationally дорог | низкая-средняя: poor targeting скрывает источник value | широкое, но неэффективное; current evidence не оправдывает как default |

Numeric utility scores не назначались, потому что evidence их не поддерживает.

**Qualitative dominance:** A1 даёт наименьший regret по трём plausible causal families, оставаясь относительно reversible и informative. A2 и A3 остаются важными targeted follow-ons, если discriminating measurements покажут dominance first-error generation или persistence boundaries. A4 не оправдан как default: evidence поддерживает selective risk-adaptive verification, а не blanket checking.

### Почему это приоритетнее generic «больше агентов» или «больше reasoning»

Intervention сохраняется при самом широком наборе plausible models:

- Если доминирует **F1**, он напрямую атакует core propagation mechanism.
- Если доминирует **F2**, он не предотвратит каждую planning error, но способен не дать одной ошибке загрязнить остаток задачи.
- Если доминирует **F3**, commit checkpoints и authoritative state updates создают durable substrate для memory/handoff systems.

Это **robust action under causal uncertainty**, а не доказательство, что F1 является universal winner.

## Evidence-sufficiency judgment

Для causal question:

> **Какой один механизм является универсальной первичной причиной long-horizon agent failure?**

run возвращает:

> **INSUFFICIENT DATA TO CHOOSE**

Для engineering decision:

> **Какой класс interventions стоит приоритизировать до широкого deployment long-running state-changing agents?**

evidence достаточно, чтобы рекомендовать:

> **risk-adaptive closed-loop state verification и recovery на consequential state transitions.**

Это центральное различие Convergence Guard: **неопределённость модели не означает action paralysis, если одно intervention robust по всему plausible model set.**

# Популярные объяснения, ослабленные evidence

### «Long tasks ломаются потому, что per-step accuracy перемножается как p^n.»

Полезная интуиция, но слишком простая. Errors correlated, recovery зависит от environment, а длинные controlled chains могут работать.

### «Bottleneck — context window.»

Иногда важен, но недостаточен. Memory architecture, causal state representation, state mutability, planning complexity и recovery влияют независимо.

### «Просто используйте более сильную модель.»

Stronger models помогают, но reliability metrics не растут синхронно с headline capability, а simple scaling не устраняет long-horizon failure в приведённом evidence.

### «Пусть агент делает reflection после каждого шага.»

Generic self-judgment не является надёжным failure detector. Specialized verification помогает, но сама имеет cost и error modes.

### «Запустите пять агентов и проголосуйте.»

Agreement не доказывает evidential independence, а voting не восстанавливает corrupted external state.

### «Checkpointing решает проблему.»

Checkpoint помогает только если сохранён правильный state, а external effects reversible или compensatable. Checkpoint может идеально сохранить уже ошибочную belief.

### «Первая ошибка объясняет любой failed trajectory.»

Как universal statement — неверно. Traverse содержит существенный класс diffuse failures без одной decisive first mistake.

# Highest-value decision-changing experiment

Главный недостающий кусок evidence — контролируемый **factorial reliability benchmark**, который независимо варьирует три finalists вместо одновременной замены всего agent stack.

## Proposed benchmark

Использовать matched tasks с одинаковой semantic goal и примерно одинаковой local action difficulty. Независимо менять:

### Factor A — policy complexity

- shallow independent subtasks;
- deeper dependency chains;
- branching/contingent plans;
- interacting constraints.

### Factor B — state architecture

- transcript-only;
- external flat state ledger;
- causally structured persistent state с explicit obligations, ownership и verified facts.

### Factor C — closed-loop recovery

- без mandatory verification;
- postcondition verification;
- verification + retry;
- verification + rollback/compensation + replan.

### Factor D — свойства environment

Где возможно, перекрёстно менять:

- static vs mutable state;
- fully observable vs partially observable;
- reversible vs irreversible/compensatable actions;
- single actor vs dual/multi-actor control.

## Измерять больше, чем final pass/fail

Для каждого run фиксировать:

- позицию first material error;
- существует ли unique first error;
- `P(first material error)` для каждой experimental cell;
- `P(terminal failure | first material error)` для каждой experimental cell;
- error type;
- detection latency;
- был detector internal или environmental;
- recovery attempt;
- recovery success;
- число state divergences;
- число unverified consequential actions;
- stale-state reads;
- duplicated или omitted obligations;
- rollback/compensation success;
- terminal success;
- repeated-run consistency;
- unsafe side effects даже в nominally successful runs.

## Discriminating predictions

**F2 получает поддержку**, если рост dependency depth сильно повышает first-error hazard даже при fully observable, persistent, verified и reversible state.

**F1 получает поддержку**, если strong postcondition checks и rollback резко уменьшают `P(terminal failure | first material error)` и downstream error correlation при сравнительно неизменной `P(first material error)`.

**F3 получает поддержку**, если causally structured persistent state резко уменьшает failures вокруг context growth, handoff, resume и multi-actor boundaries при фиксированных model и verification policy.

Interaction terms не менее важны, чем main effects. Наиболее правдоподобный результат — не один winner, а карта **какой механизм доминирует в каком task regime**.

## Minimum practical discriminating pilot

Полный factorial benchmark выше — research-grade design. **Самый дешёвый practical next step, способный изменить near-term engineering decision**, меньше:

- заранее выбрать **8 stateful tool-use tasks** как минимум из двух task types;
- зафиксировать base model, prompts, tool set, planning budget и task definitions;
- выполнить **2×2 architecture ablation**:
  1. baseline — без added closed-loop guard и без structured persistent ledger;
  2. closed-loop guard only — authoritative pre-read, explicit postcondition, post-read, targeted retry/rollback/replan;
  3. persistent ledger only — explicit durable facts, obligations, ownership и verified completion state;
  4. guard + persistent ledger;
- повторить каждую task **три независимых раза в каждой cell**, всего 96 trajectories.

Pilot должен измерять `P(first material error)`, `P(terminal failure | first material error)`, detection latency, recovery success, unsafe/irreversible side effects, дополнительные tool calls, latency и final task success.

### Decision-changing patterns

- **Сохранить A1 как near-term priority**, если guard conditions последовательно снижают conditional terminal failure в обоих task types, first-error frequency остаётся broadly similar, а дополнительный cost/latency operationally приемлем.
- **Сдвинуть priority к A2 / policy capability**, если основная потеря performance идёт через растущий first-error rate, а guard почти не снижает conditional terminal failure.
- **Сдвинуть priority к A3 / persistent-state architecture**, если ledger conditions дают более ясный gain, особенно на resume/handoff/long-context boundaries, а guard alone почти не помогает.
- **Принять staged hybrid**, если guard и ledger effects complementary или combined cell даёт material interaction.

### Guardrails и stopping rule

- First material error и terminal outcome оценивать по frozen criteria, определённым до раскрытия condition labels там, где это практически возможно.
- Не менять prompts, tools или planning budget в середине pilot.
- Учитывать added verification cost и verifier-caused failures, а не только recovered runs.
- Остановиться после preregistered 96 trajectories; не расширять pilot до появления желаемого вывода.
- Если результаты mixed между двумя task types, сохранить `INSUFFICIENT DATA TO CHOOSE` для universal causal winner и использовать task-specific pattern, а не усреднять различия.

Этот pilot недостаточно велик для universal theory. Его более узкая цель — проверить, выдерживает ли текущий **A1 engineering priority** controlled ablation до инвестиций в большой factorial benchmark.

# Runtime integrity note

Исходный Full Mode run использовал fresh isolated worker contexts для стадий, где ценность зависела от blindness или independence, включая causal search, reduction, finalist dossiers и slate-level adjudication.

Публичный case study не считает согласие workers independent real-world evidence. Claims опираются на приведённые внешние источники, а worker outputs используются только для структурирования competing causal models и их сравнения.

# Что этот пример показывает о методе

Этот case полезен именно потому, что итог — не «мы нашли одну истинную причину, почему агенты ломаются».

Протокол заставил разделить несколько утверждений, которые обычная дискуссия легко сливает:

> **На более длинных задачах success ниже**
> не означает
> **сама длина задачи является причиной.**

> **Planning errors часто начинают failure**
> не означает
> **одного better planning достаточно для reliability.**

> **Memory важна**
> не означает
> **решение — больший context window.**

> **Universal causal winner не найден**
> не означает
> **никакое engineering action нельзя обосновать.**

Поэтому strongest output run состоит из двух judgments:

1. **Causal attribution:** текущее evidence поддерживает interacting task-dependent model и недостаточно для выбора одной universal primary cause.
2. **Decision under uncertainty:** closed-loop verification и recovery вокруг consequential state changes — robust priority по всему surviving model set.

Разделение между **тем, что истинно о причине**, и **тем, что рационально делать дальше**, — одна из центральных design goals Convergence Guard.

# Источники

Primary или nearest-available sources, использованные в публичном evidence brief:

1. Rein, D. et al. (2025). **HCAST: Human-Calibrated Autonomy Software Tasks.**
   https://arxiv.org/abs/2503.17354

2. METR (обновлено 08.05.2026). **Task-Completion Time Horizons of Frontier AI Models.**
   https://metr.org/time-horizons/

3. Wang, X. J. et al. (2026). **The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break.**
   https://arxiv.org/abs/2604.11978

4. Rahman, S. et al. (2026). **Locating Hidden Failures Makes Long-Horizon Agents More Reliable.**
   https://arxiv.org/abs/2609.17930

5. Lu, J. et al. (2025). **ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities.** Findings of NAACL 2025.
   https://aclanthology.org/2025.findings-naacl.65/

6. Yao, S. et al. (2025). **τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.** ICLR 2025.
   https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b126cc38b8638e07bef37e7b2bb72bf-Abstract-Conference.html

7. Barres, V. et al. (2026). **τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment.** ICML 2026.
   https://proceedings.mlr.press/v306/barres26a.html

8. Rabanser, S. et al. (2026). **Towards a Science of AI Agent Reliability.** ICML 2026.
   https://proceedings.mlr.press/v306/rabanser26a.html

9. Wan, Y. et al. (2026). **Inference-Time Scaling of Verification: Self-Evolving Deep Research Agents via Test-Time Rubric-Guided Verification.** Findings of ACL 2026.
   https://aclanthology.org/2026.findings-acl.1243/

10. Bu, T. et al. (2026). **Recovering Policy-Induced Errors: Benchmarking and Trajectory Synthesis for Robust GUI Agents.** ICML 2026.
    https://proceedings.mlr.press/v306/bu26b.html

11. Mohammadi, B. et al. (2026). **Atomix: Timely, Transactional Tool Use for Reliable Agentic Workflows.**
    https://arxiv.org/abs/2602.14849

12. Zhuang, Y. et al. (2026). **AgentRewind: Recoverable Execution for Long-Horizon LLM Agents.**
    https://arxiv.org/abs/2608.14380

13. Zhao, Y. et al. (2026). **AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications.** ICML 2026.
    https://proceedings.mlr.press/v306/zhao26bs.html

14. Pai, D. M. & Xian, L. (2026). **Long-Horizon State Tracking in LLMs: Executing MD5 through a Deep Sequence of Dependent Tool Calls.**
    https://arxiv.org/abs/2609.00012

15. Luo, H. et al. (2026). **UltraHorizon: Benchmarking Agent Capabilities in Ultra Long-Horizon Scenarios.** ICML 2026.
    https://proceedings.mlr.press/v306/luo26ai.html

Список источников намеренно heterogeneous, потому что decision question охватывает planning, reliability, stateful tool use, recovery, memory, coordination и benchmark methodology. Run не считал несколько papers независимым corroboration только потому, что они пришли к похожим conclusions; source ancestry, task overlap и intervention scope рассматривались отдельно.
