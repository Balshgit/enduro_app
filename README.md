# EnduroApp

Python API для enduro app.

# Разработка:

Описание структуры проекта и правила разработки

## Работа с зависимостями проекта

В качестве пакетного менеджера используется uv ([инструкция по установке](https://docs.astral.sh/uv/#installation))

### Полезные команды

- Для установки Python-интерпретатора можно использовать команду `uv python install <версия>`
- Создать виртуальное окружение для проекта – `uv venv` или `uv venv --python 3.14.1`
- Создать виртуальное окружение для проекта вне проекта `uv venv /path/to/virtual_env`. 
При этом в переменные окружения необходимо добавить переменную `UV_PROJECT_ENVIRONMENT=/path/to/virtual_env`.
В pycharm это можно задать в настройках `File | Settings | Tools | Terminal | Environment Variables`
- Активировать виртуальное окружение:
    - macOS и Linux: `source .venv/bin/activate`
    - Windows: `source .venv/bin/activate`
- Для добавления зависимостей
    - Необходимые для работы проекта – `uv add <package_name>`
    - Необходимые для разработки (не будут установлены в Docker-образ проекта) – `uv add --dev <package_name>`
- Синхронизировать зависимости текущего окружения с lock-файлом – `uv sync`

## Переменные окружения

При старте работы над проектом в директории `settings/environments` создайте два файла:

- **`.env`** — для локальной разработки
- **`.env.tests`** — для тестов

Оба файла можно заполнить опираясь на шаблон `.env.local.template`:
```bash
cp -f settings/environments/.env.local.template settings/environments/.env \
&& cp -f settings/environments/.env.local.runtests settings/environments/.env.tests
```

### Обновление файлов зависимостей

#### Обновление базовых зависимостей:

Для обновления базовых зависимостей обновляем 2 файла:
- pyproject.toml
- base-pyproject.toml


Для обновления зависимостей самих сервисов дополнительно обновляем файлы

- admin/admin-pyproject.toml - для зависимостей сервиса админки
- api/api-pyproject.toml - для зависимостей сервиса api


## Создание файлов зависимостей для обоих сервисов
Сбор файлов зависимостей для админки и api можно смотреть здесь 
можно посмотреть [здесь](./docs/development/dependencies.md).