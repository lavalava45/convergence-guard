# История изменений

[English version](CHANGELOG.md)

## Unreleased

## v0.2.3 — исследовательский pre-release (2026-10-08)

- добавлен post-benchmark correction layer eval v0.2: canonical-rule conformance matrix, self-contained Reduced packet, раздельная schema causal/action/next-test/protocol-completion, fail-closed accounting для triggered conditional stages и отдельные v0.2 tests;
- добавлен blind raw-vs-normalized re-audit M04–M07; N1 сработала в 15/16 runs, а два независимых judge показали, что normalization часто материально меняла winner-like semantic interpretation, поэтому raw-vs-normalized disagreement теперь отдельный diagnostic, а не косметическая compliance-note;
- завершён targeted isolation-ablation `v0.1.4` после прозрачного versioning execution-only failures: 16/16 valid cells, 64/64 responses с frozen standalone endpoint, isolated-pair integrity PASS и 0/8 false-anchor adoptions по двум независимым anchor judges;
- isolation claims соответственно сужены: information boundary механически подтверждена, но этот четырёх-case ablation не показал incremental answer-quality защиты isolation сверх shared workflow с явной anti-anchoring инструкцией;
- `main-v0.1.7` в публичной документации переклассифицирован как implemented-workflow benchmark, а не полная валидация canonical Full/Reduced execution;
- в canonical skill добавлен benchmark-informed selective activation triage: для напрямую разрешённых, дешёвых в проверке и обратимых cases предпочтителен обычный анализ; Full Mode следует включать главным образом при сохраняющейся causal ambiguity, когда evidence dependence, framing/open-world risk, трудно разделимые confounding/interaction или дорогой необратимый commitment оправдывают overhead;
- после post-benchmark аудита усилены stage boundaries Full Mode: явный allowlist для C3 boundary critic, удалён неоднозначный помеченный "outside alternative" из D2, задан явный routing для premortem/stakeholder findings и полный D3 second-opinion contract для inputs/disposition/reconciliation;
- causal-structure judgment и action sufficiency явно разведены: поддержанный `COEXISTING`/`INTERACTING` model judgment больше не должен затираться `INSUFFICIENT DATA TO CHOOSE` для решения о действии;
- benchmark claims уточнены: blind semantic scores относятся к заранее нормализованным artifacts; raw Full outputs M04/M05 всё ещё содержали ненулевой `preferred_cause`, который frozen rule N1 очистила до judging;
- applicability guide обновлён от pilot-era hypotheses к результатам завершённого `main-v0.1.7`, а исходные документы планирования 64-run study получили явные historical-status notes;
- завершён замороженный comparative benchmark `main-v0.1.7`: 8 cases × 4 modes × 1 repeat = 32 primary runs, затем 32/32 calibration completions и blind semantic judging по нейтральным answer IDs;
- добавлены машиночитаемые и человекочитаемые main-study results в `evals/results/main-v0.1.7/`, включая парную English/Russian интерпретацию и явные caveats по resource cost, calibration, normalization и ограничениям metric set;
- задокументирован финальный dedicated runtime `llama-server 2.52.0` без prompt cache, на котором frozen study был завершён после предыдущих transport/cache failures управляемого LM Studio backend;
- добавлено парное English/Russian руководство по применимости с классами задач, быстрым activation test и явными примерами, когда CG может быть избыточным или полезным;
- задокументирован автоматический локальный technical pilot на двух cases, включая сигнал over-analysis / over-abstention на P01 и корректную работу с недоопределённостью на P02;
- добавлена детерминированная normalization policy v0.1 для механически противоречивого `preferred_cause` при non-choice status с сохранением raw-answer и полным audit trail;
- уточнено краткое описание устанавливаемого skill и явно указано, что полная установка включает рабочий пакет `references/`;
- добавлены правила API/fresh-request для построения isolation-dependent workers без унаследованного session state;
- разрешён один настоящий финалист после проверки покрытия / недостающих свидетельств; dossier, sensitivity и shared-bias review сохраняются, а пропускается только pairwise collision;
- введён явный статус `PENDING` для существенно пересмотренных гипотез, чтобы прерванный или ограниченный бюджетом повторный проход не наследовал устаревшую валидацию;
- добавлен необязательный information-probe mini-dossier, который остаётся отдельным от finalist dossiers и adjudication;
- исправлен шлюз достаточности: оправданные проверки, способные изменить выбор, выполняются до принятия обязательства;
- в разрешённые входы слепого mapper добавлены общая сводка свидетельств и контракт решения;
- задан явный исход без найденной выполнимой различающей проверки, отдельно от достаточности для действия и отложенных проверок;
- корректирующие циклы ограничены общим бюджетом прохода и правилом остановки при отсутствии прогресса;
- отрицательный isolation smoke test отделён от подтверждения границы средствами runtime, включая последующий retrieval/tool access.

- в README добавлены 60-second Quick Start и короткий раздел «Почему не просто спросить 5 агентов?»;
- требования к runtime сделаны vendor-neutral; implementation-specific runtime profile файлы удалены из публичного репозитория.
- добавлен третий двуязычный Full Mode worked example о надёжности long-running autonomous agents: отдельно рассмотрены policy-complexity, closed-loop state integrity и persistent-state/coordination mechanisms, а engineering priority выведен как risk-adaptive verification/recovery при causal uncertainty.

## v0.2.2 — pre-release

- добавлены DESIGN.md / DESIGN.ru.md с самостоятельным threat model и архитектурным обоснованием от первых принципов;
- зафиксированы traceability threat→control, остаточные риски, отвергнутые архитектурные альтернативы и открытые вопросы для evaluation suite.
- добавлена claim-level source-quality policy: репутация источника определяет приоритет проверки, но не заменяет provenance, inspectability, evidence ancestry, обработку противоречий и replication;
- разделено подтверждение того, что документ или институт **заявляет X**, и подтверждение самого X;
- введены явные роли источников: EVIDENCE, CORROBORATION, CONTEXT, LEAD ONLY и UNSUPPORTED.
- добавлен второй публичный Full Mode пример о происхождении SARS-CoV-2 с парными English/Russian версиями, анализом source dependency, явной обработкой inaccessible evidence и раздельными model/evidence-sufficiency judgments;
- добавлена явная оговорка о границах публичных примеров: worked runs демонстрируют протокол и не заменяют лабораторные, криминалистические, уголовные, разведывательные, юридические или иные профильные первичные расследования.
- текущая публичная документация и metadata устанавливаемого skill синхронизированы с v0.2.2.

## v0.2.1 — pre-release

- ужесточены требования Full Mode к границам контекста;
- добавлены явный runtime isolation preflight и правила восстановления после сбоев;
- уточнено, что согласие workers не является evidential independence;
- сохранены адаптивная начальная когорта из трёх search workers и слепое сокращение в Phase C;
- добавлена парная англо-русская человекочитаемая документация;
- добавлен первый публичный Full Mode пример: кейс идентификации Джека Потрошителя;
- публичная документация синхронизирована с v0.2.1.
