# dotenv-check

Сверяет локальный `.env` с шаблоном `.env.example` перед запуском: показывает пропущенные, пустые, заглушечные и лишние ключи. **Значения никогда не выводятся** — ни в тексте, ни в JSON. Без зависимостей, Python 3.10+.

## Быстрый старт

```bash
python -m dotenv_check                 # .env против .env.example
python -m dotenv_check prod.env --example .env.example
python -m dotenv_check --strict --json # лишние ключи и предупреждения тоже дают код 1
```

Пример:

```text
[ERROR] MISSING_KEY: API_TOKEN
[ERROR] EMPTY_VALUE: DATABASE_URL
[WARNING] PLACEHOLDER_VALUE: SECRET_KEY
```

## Проверки

| Код | Уровень | Смысл |
| --- | --- | --- |
| `MISSING_KEY` | error | ключа из шаблона нет в `.env` |
| `EMPTY_VALUE` | error | ключ есть, но значение пустое |
| `PLACEHOLDER_VALUE` | warning | значение похоже на заглушку (`changeme`, `your_…`, `<…>`, `TODO`) |
| `EXTRA_KEY` | warning (error с `--strict`) | ключа нет в шаблоне |

Коды возврата: `0` — ок, `1` — найдены ошибки (или предупреждения при `--strict`), `2` — файл не читается или синтаксис `.env` некорректен.

## Формат

Поддерживаются `KEY=VALUE`, комментарии `#`, префикс `export `, значения в одинарных или двойных кавычках. Дубликаты ключей — ошибка парсинга.

## Ограничения

- Не интерполирует переменные вида `${OTHER}` и не читает многострочные значения.
- Проверка заглушек эвристическая.

## Разработка

```bash
python -m unittest discover -s tests -t .
```

## Лицензия

MIT — см. [LICENSE](LICENSE).

Пример заполненного файла — [examples/app.env](examples/app.env):

```bash
python -m dotenv_check examples/app.env --example .env.example --strict
```

## История изменений

См. [CHANGELOG.md](CHANGELOG.md). Политика безопасности — в [SECURITY.md](SECURITY.md).

## Использование в CI

Фрагмент для GitHub Actions (Python 3.10+, без зависимостей):

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
- name: dotenv-check
  run: python -m dotenv_check --strict
```
