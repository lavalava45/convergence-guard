# Первый browser pilot-run

Первый run по замороженному плану:

- Run ID: `P01-r1-cg-reduced`
- Case: `P01`
- Mode: `CG Reduced`
- CG commit: `fda4395`

## Один раз перед началом

1. В обычном Chrome открой `chrome://extensions`.
2. У расширения Chat On Steroids проверь, что **Allow in Incognito / Разрешить в режиме инкогнито = OFF**.
3. Открой новое окно Chrome Incognito.
4. В этом окне войди в личный Google Account и открой `gemini.google.com`.
5. Создай **Temporary chat**.
6. Внизу выбери **Gemini Pro**, если он доступен. Если Pro недоступен, выбери Gemini Flash. Запиши точное название выбранной модели: эту же модель нужно использовать во всех 8 pilot-runs.

## Основной ответ

1. Открой локальный файл `evals/browser-pilot/001-P01-cg-reduced-packet.md`.
2. Скопируй **весь файл целиком**.
3. Вставь его одним сообщением в пустой Temporary Chat.
4. Ничего не добавляй от себя и отправь.
5. Получив ответ, **до любого follow-up** скопируй первоначальный ответ в `evals/runs/pilot/P01/r1/cg-reduced/final.json`.
6. Не редактируй содержание JSON вручную. Если Gemini добавил Markdown fences или текст вокруг JSON, сохрани исходный ответ отдельно и остановись: это процедурный результат, который нельзя тихо исправлять.

## Калибровка

Только после сохранения primary answer:

1. В том же Temporary Chat вставь целиком `evals/browser-pilot/001b-P01-calibration-prompt.txt`.
2. Сохрани ответ как `evals/runs/pilot/P01/r1/cg-reduced/calibration.json`.
3. После этого закрой Temporary Chat и не продолжай его.

Не запускай второй pilot-run до проверки первого artifact/процедуры.
