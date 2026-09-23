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

## Архитектура

```text
HH API / fixtures
       |
       v
  VacancyInput
       |
       v
  PhoneExtractor
       |
       v
 phonenumbers
       |
       v
  E.164 + dedup
       |
       v
VacancyPhoneResult
```

Основные компоненты:

- `app/models.py` — входные и выходные модели;
- `app/phones/extractor.py` — поиск кандидатов, контекстная фильтрация и deduplication;
- `app/phones/normalizer.py` — parsing, validation и E.164 normalization;
- `app/pipeline.py` — анализ одной вакансии и batch processing;
- `app/sources/fixtures.py` — загрузка fixtures;
- `app/sources/hh.py` — отдельный adapter для HH.ru API;
- `app/cli.py` — CLI и запись JSON/CSV.

CLI в текущем MVP работает с fixtures. HH API adapter отделён от основного pipeline,
поэтому источник данных можно заменить без изменения phone detection logic.

## Почему без LLM

Для первой версии задачи LLM не требуется. Номер телефона можно определять
детерминированным pipeline: regex используется только для поиска кандидатов,
а `phonenumbers` выполняет parsing и validation.

Это также позволяет не генерировать контакты и не искать их за пределами самой вакансии.

## Ограничения

- Evaluation dataset synthetic и небольшой.
- Текущая версия определяет только телефоны.
- Для номеров без country code используется `DEFAULT_PHONE_REGION`.
- Автоматический поиск вакансий через HH API не является частью CLI-команды `analyze`;
  для API есть отдельный `HHClient` adapter.

## Конфигурация

`.env.example`:

```text
HH_API_TOKEN=
DEFAULT_PHONE_REGION=RU
HTTP_TIMEOUT=10
```

Секреты не должны добавляться в Git. Файл `.env` находится в `.gitignore`.

## Структура проекта

```text
.
├── app/
│   ├── cli.py
│   ├── models.py
│   ├── pipeline.py
│   ├── phones/
│   │   ├── extractor.py
│   │   └── normalizer.py
│   └── sources/
│       ├── fixtures.py
│       └── hh.py
├── evaluation/
│   ├── REPORT.md
│   ├── evaluate_results.py
│   └── gold.csv
├── fixtures/
│   └── sample.json
├── fixtures_eval/
│   └── evaluation.json
├── tests/
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```
