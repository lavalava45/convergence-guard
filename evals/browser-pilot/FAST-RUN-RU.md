# Ускоренный browser pilot

Модель для всех participant runs: `flash extended`.

CG Full не выполняется в consumer Gemini browser runtime: browser Temporary Chat не получил runtime-level isolation PASS по требованиям `ISOLATION-PREFLIGHT.md`. Слоты `P01-r1-cg-full` и `P02-r1-cg-full` заранее отмечены `invalid / INCONCLUSIVE`; это не Reduced Mode и не пропуск результата после просмотра ответа.

## Уже завершено

1. `P01-r1-cg-reduced` — complete.
2. `P01-r1-shared-context-multi-agent` — complete.

## Оставшийся порядок

### 3. P01 single-context

Новый Temporary Chat:

1. отправить `003-P01-single-context-packet.md`;
2. primary JSON не исправлять; принести его в ChatGPT для freeze/validation;
3. после PASS в том же Temporary Chat отправить `003b-P01-single-context-calibration.txt`;
4. принести calibration JSON.

### 4. P01 cg-full

Не запускать. Manifest заранее фиксирует `invalid / isolation_preflight=INCONCLUSIVE`.

### 5. P02 shared-context-multi-agent

Новый Temporary Chat. Между A/B/C не возвращаться в ChatGPT:

1. `005a-P02-shared-context-analyst-A-packet.md`;
2. после ответа A — `005b-P02-shared-context-analyst-B.txt`;
3. после ответа B — `005c-P02-shared-context-analyst-C.txt`;
4. после ответа C — `005d-P02-shared-context-synthesizer.txt`;
5. primary Synthesizer JSON не исправлять; принести его вместе с A/B/C в ChatGPT для freeze/validation;
6. после PASS — `005e-P02-shared-context-calibration.txt`;
7. принести calibration JSON.

### 6. P02 single-context

Новый Temporary Chat:

1. `006-P02-single-context-packet.md`;
2. primary JSON принести для freeze/validation;
3. после PASS — `006b-P02-single-context-calibration.txt`;
4. принести calibration JSON.

### 7. P02 cg-full

Не запускать. Manifest заранее фиксирует `invalid / isolation_preflight=INCONCLUSIVE`.

### 8. P02 cg-reduced

Новый Temporary Chat:

1. `008-P02-cg-reduced-packet.md`;
2. primary JSON принести для freeze/validation;
3. после PASS — `008b-P02-cg-reduced-calibration.txt`;
4. принести calibration JSON.

## Правила ускоренного режима

- каждый новый treatment начинается в новом Temporary Chat;
- модель всегда `flash extended`;
- не переносить ответы предыдущего treatment;
- не исправлять ответы Gemini вручную;
- calibration только после freeze/validation primary answer;
- для shared-context A/B/C остаются в одном Temporary Chat и намеренно видят предыдущий shared journal;
- cg-full не симулировать через обычные Temporary Chats без isolation PASS.
