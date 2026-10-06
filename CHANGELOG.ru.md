# История изменений

[English version](CHANGELOG.md)

## Unreleased

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
