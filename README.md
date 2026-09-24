# Resumetto Phone MVP

Небольшой standalone-MVP для поиска телефонных номеров, опубликованных непосредственно в вакансиях.

## Что делает

Pipeline принимает нормализованные вакансии и:

1. сначала проверяет структурированные `contacts`;
2. затем ищет кандидатов в `description`;
3. валидирует кандидатов библиотекой `phonenumbers`;
4. нормализует валидные номера в E.164;
5. удаляет дубликаты после нормализации;
6. возвращает вакансии, в которых найден хотя бы один валидный телефон.

Телефон никогда не ищется во внешнем интернете и не генерируется.

## Стек

- Python 3.11+
- Pydantic
- phonenumbers
- httpx
- python-dotenv
- pytest

## Установка

Рекомендуется запускать проект в виртуальном окружении.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Запуск на fixtures

```bash
resumetto analyze fixtures --output-dir output
```

Или без установленной entry point-команды:

```bash
python -m app analyze fixtures --output-dir output
```

После запуска создаются:

- `output/results.json` — результаты анализа;
- `output/results.csv` — результаты в CSV;
- `output/errors.csv` — ошибки отдельных вакансий.

Для вывода только вакансий с найденным телефоном:

```bash
resumetto analyze fixtures --output-dir output --only-with-phone
```

## Тесты

```bash
pytest
```

## Evaluation

В проекте есть отдельный synthetic evaluation dataset из 110 вакансий:

- 70 вакансий с телефоном;
- 40 вакансий без телефона.

Запуск:

```bash
resumetto analyze fixtures_eval --output-dir output_eval
python evaluation/evaluate_results.py output_eval/results.json
```

Текущий результат на этом датасете:

```text
Gold:      110
Results:   110
TP:        69
FP:        0
FN:        1
TN:        40
Precision: 100.00%
Recall:    98.57%
```

Это synthetic dataset для проверки реализации, а не репрезентативная выборка HH.ru.

Единственный false negative связан с номером `+44 7700 900123`, который отклоняется
`phonenumbers` как невалидный. Валидация `is_valid_number()` намеренно не ослабляется,
чтобы не превращать произвольные длинные числовые идентификаторы в телефоны.

## Конфигурация

`.env.example`:

```text
HH_API_TOKEN=
DEFAULT_PHONE_REGION=RU
HTTP_TIMEOUT=10
```