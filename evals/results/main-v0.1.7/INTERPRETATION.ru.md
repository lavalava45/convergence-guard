# Основной benchmark v0.1.7 — интерпретация

Это интерпретационный слой для зафиксированного набора результатов `main-v0.1.7`. Машиночитаемый агрегат находится в `summary.json`, таблицы метрик — в `REPORT.md`.

## Что было запущено

Финальный main study состоял из 8 заранее зафиксированных cases × 4 режима × 1 repeat = **32 participant runs**. Сокращение более раннего плана с 64 до 32 runs было объявлено до запуска финальной версии: мы отказались от слабой оценки variance по двум repeats в пользу полного покрытия матрицы `case × mode`. Финальный runtime — отдельный локальный `llama-server 2.52.0` с `gemma-4-12b-it-Q6_K.gguf`, context 15 000, полным GPU offload, KV offload, одним parallel slot, SSE streaming и отключённым cross-request prompt cache.

Все **32/32 primary runs** завершились и были заморожены до calibration. Затем без ошибок завершились **32/32 calibration runs**. Semantic judging выполнялся по нейтральным ID в трёх независимых judge-контекстах, которые не видели mode name, run ID, cost, latency, число workers или приватную blind-map. Post-hoc weighted composite score не использовался.

## Основной результат

`cg-full` показал лучший средний action score и наиболее консервативный профиль premature convergence:

- premature winner: **0/8** у `cg-full`, **0/8** у shared-context multi-agent, **1/8** у single-context, **1/8** у `cg-reduced`;
- correct abstention на двух keyed-insufficient cases: **2/2** у `cg-full`, **2/2** у shared-context, **1/2** у single-context, **1/2** у `cg-reduced`;
- средний action quality: **1.875/2** у `cg-full`, 1.625 у single-context, 1.625 у shared-context и 1.500 у `cg-reduced`;
- средний recall decision-relevant mechanisms: **1.000** у `cg-full`, shared-context и single-context; 0.958 у `cg-reduced`;
- по next-test quality Full Mode **не** оказался лучшим: 1.500 у `cg-full` против 1.625 у single-context и `cg-reduced`.

Эти semantic scores относятся к frozen normalized артефактам `final.json`. В обоих keyed-insufficient Full Mode runs (M04 и M05) raw participant answer объявлял `INSUFFICIENT`, но одновременно оставлял ненулевой `preferred_cause`; predeclared normalization rule N1 очистила это поле до blind judging. Поэтому результат `2/2 correct abstentions` корректен по frozen scoring protocol, но raw-output behavior был менее чистым, чем можно подумать по одной агрегированной цифре.

Самый ясный сигнал границы применимости появился на **M05 — deceptive underdetermination**. `cg-full` и shared-context сохранили реально живые альтернативы, тогда как single-context и `cg-reduced` получили от blind judge `premature_winner=1` и `correct_abstention=0`. Это соответствует исходной гипотезе: дополнительная структура особенно полезна, когда кажущееся изобилие evidence на деле зависит от одной производной evidence-ветки и присутствует сильное framing pressure.

## Цена улучшения

Выигрыш оказался дорогим. Среднее primary-потребление на case:

| Режим | Model calls | Input tokens | Output tokens |
|---|---:|---:|---:|
| single-context | 1.000 | 924 | 748 |
| cg-reduced | 1.000 | 1 665 | 636 |
| shared-context-multi-agent | 4.375 | 6 852 | 2 220 |
| cg-full | 9.125 | 12 532 | 5 644 |

По сравнению с single-context Full Mode использовал примерно **в 9.1 раза больше model calls, в 13.6 раза больше input tokens и в 7.5 раза больше output tokens**. Поэтому benchmark поддерживает selective-use стратегию, а не правило «всегда запускать Full Mode».

Shared-context multi-agent оказался сильным comparator: как и Full Mode, он не получил ни одного premature winner и правильно abstain'ился в обоих keyed-insufficient cases, используя примерно вдвое меньше calls. При этом у Full Mode были выше mean action quality (1.875 против 1.625), лучше Brier в этом небольшом calibration add-on (0.007 против 0.027) и выше next-test quality (1.500 против 1.250). При восьми cases и одном repeat эти различия являются описательными, а не статистически установленными.

## Почему нельзя просто написать «Full Mode победил»

Blind semantic metrics и буквальный status token дают не полностью одинаковую картину. Совпадение declared status с hidden key составило:

- single-context: **6/8**;
- `cg-full`: **5/8**;
- shared-context multi-agent: **5/8**;
- `cg-reduced`: **4/8**.

В частности, `cg-full` объявил `INSUFFICIENT` на M06 и M07, где frozen key ожидал `COEXIST`. При этом содержательно ответы всё равно отражали важные механизмы и действия и поэтому получили хорошие оценки по frozen semantic metrics. Это выявило ограничение текущего metric set: в нём есть отдельные premature-winner и abstention metrics, но нет одной прямой semantic-метрики **causal-structure correctness**, которая одинаково штрафует все ошибки между `CHOOSE / COEXIST / INSUFFICIENT`.

Поэтому корректный вывод уже: **в этих восьми cases у Full Mode не наблюдалось unsupported winner selections и он давал наиболее сильные actions, но не доминировал по всем structural и efficiency diagnostics.** Status-mismatch pattern нужно использовать как требование к следующей версии benchmark, а не прятать за агрегатом.

## Calibration и output compliance

Средние Brier scores были очень низкими у всех режимов: 0.004 single-context, 0.007 `cg-full`, 0.015 `cg-reduced` и 0.027 shared-context. Как и было заранее оговорено в protocol, это малое число коррелированных binary claims, поэтому самостоятельный сильный calibration claim из этих цифр делать нельзя.

Normalization срабатывала часто: 5/8 Full, 5/8 single-context, 7/8 Reduced и 7/8 shared-context runs потребовали заранее зафиксированного механического ремонта, который обнуляет `preferred_cause` при `COEXIST` или `INSUFFICIENT`. Это несомненно проблема output-contract/compliance, но её нельзя считать чисто косметической: ненулевой preferred cause может одновременно нести winner-like semantic signal. Поскольку N1 была заморожена до main study и одинаково применялась ко всем режимам, использование normalized artifact процедурно корректно; однако расхождение raw и normalized — существенное ограничение интерпретации, которое следующая eval-версия должна измерять явно.

Более сложные workflows также потребовали transport retries во время primary execution: всего 6 у `cg-full`, 3 у shared-context и 0 у single-context/Reduced. Финальный standalone runtime без prompt cache завершил все frozen runs, но runtime complexity сама является частью практической цены multi-call workflows.

## Что benchmark показывает и чего не показывает

Этот результат — полезное evidence для **карты применимости**, а не универсальный рейтинг методов. В этом 8-case наборе структурированные многостадийные режимы показали меньше observed premature winner selections на самом adversarially ambiguous case, чем single-context и Reduced Mode, но их дополнительная цена часто не оправдана на простых задачах. Одновременно сильный результат shared-context показывает, что часть наблюдаемого преимущества может объясняться multi-pass analysis вообще, а не только CG-specific isolation.

Исследование **не** доказывает общего превосходства Convergence Guard. Ограничения существенны: одна локальная модель; восемь authored cases; один repeat на ячейку; только одна blind semantic оценка каждого ответа вместо replicated inter-rater judging; высокая частота normalization; и выявленный metric gap для полной causal-structure correctness. Из этого dataset нельзя честно выводить статистическую значимость или широкие population claims.

Если продолжать evidence-building, следующий полезный шаг — replication на другой модели/runtime и/или небольшой targeted re-test именно тех cases, где режимы сильнее всего разошлись, а не механическое увеличение этой же 32-run матрицы.
