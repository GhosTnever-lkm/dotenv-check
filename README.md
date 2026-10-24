# dotenv-check

[![CI](https://github.com/GhosTnever-lkm/dotenv-check/actions/workflows/ci.yml/badge.svg)](https://github.com/GhosTnever-lkm/dotenv-check/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/GhosTnever-lkm/dotenv-check)](https://github.com/GhosTnever-lkm/dotenv-check/releases/latest)

Сверяет локальный `.env` с шаблоном `.env.example` перед запуском: показывает пропущенные, пустые, заглушечные и лишние ключи. **Значения никогда не выводятся** — ни в тексте, ни в JSON. Без зависимостей, Python 3.10+.

## Быстрый старт

Скачайте wheel из [последнего релиза](https://github.com/GhosTnever-lkm/dotenv-check/releases/latest) и установите:

```bash
python -m pip install dotenv_check-0.1.3-py3-none-any.whl
```

Затем запустите:

```bash
dotenv-check                           # .env против .env.example
python -m dotenv_check prod.env --example .env.example
python -m dotenv_check --strict --json # лишние ключи и предупреждения тоже дают код 1
python -m dotenv_check --ignore CI_TOKEN   # пропустить ключ, нужный только в CI
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

Поддерживаются `KEY=VALUE`, комментарии целой строки и в конце значения, префикс `export `, значения в одинарных или двойных кавычках. В двойных кавычках кавычка считается экранированной, если перед ней стоит нечётное число обратных слешей. Незакрытые кавычки и дубликаты ключей — ошибка парсинга.

## Ограничения

- Не интерполирует переменные вида `${OTHER}` и не читает многострочные значения.
- Проверка заглушек эвристическая.

## Разработка

```bash
python -m unittest discover -s tests -t .
```

## Поддержка и Pro-версия

Базовая версия остаётся бесплатной; отдельный Pro-выпуск пока не опубликован. Нужны дополнительные правила шаблонов или CI-интеграция? [Опишите сценарий в запросе](https://github.com/GhosTnever-lkm/dotenv-check/issues/new).

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
