# Запуск тестов

## Локальный запуск тестов:

Активация виртуального окружения

```bash
source .venv/bin/activate
```

Локальный запуск через консоль

```bash
cd app
DJANGO_SETTINGS_MODULE=infra.settings STAGE=runtests LOCALTEST=1 uv run -m pytest tests/integration -vv
```

Запуск в docker compose

```bash
cd ../ или cd enduro_app
docker compose run admin run-tests
```