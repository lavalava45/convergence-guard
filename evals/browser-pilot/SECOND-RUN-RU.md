# Второй browser pilot-run

Второй run по замороженному плану:

- Run ID: `P01-r1-shared-context-multi-agent`
- Case: `P01`
- Mode: `shared-context-multi-agent`
- Eval commit: `fda4395b37c782de3e6d79ab41d59b208d39e88f`

## Перед запуском

1. Не начинай run, пока точное название Gemini-модели первого run не записано в manifest.
2. Используй ту же самую модель и те же доступные настройки, что в первом run.
3. Открой новое Chrome Incognito window.
4. Убедись, что Chat On Steroids extension не разрешён в Incognito.
5. Открой Gemini и создай новый Temporary Chat.
6. Не переносить в него ответы или calibration из первого run.

## Shared-context последовательность

Все четыре participant calls выполняются в ОДНОМ Temporary Chat. Ответы A/B/C намеренно остаются видимыми следующим проходам как shared journal.

1. Отправь целиком `002a-P01-shared-context-analyst-A-packet.md`.
2. Получив ответ Analyst A, ничего не исправляй. Отправь целиком `002b-P01-shared-context-analyst-B.txt`.
3. Получив ответ Analyst B, отправь целиком `002c-P01-shared-context-analyst-C.txt`.
4. Получив ответ Analyst C, отправь целиком `002d-P01-shared-context-synthesizer.txt`.
5. Ответ synthesizer считается primary final answer. Не исправляй его и не проси Gemini переделать формат.
6. Сразу принеси сюда сырой synthesizer answer для freeze и validation.

## Calibration

Calibration не отправлять, пока primary synthesizer answer не сохранён и не прошёл процедуру freeze/validation.

После разрешения на calibration в том же Temporary Chat используется:

`002e-P01-shared-context-calibration.txt`

После calibration Temporary Chat закрывается и больше не используется.
