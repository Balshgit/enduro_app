GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)

.PHONY: help format lint lint-style lint-typing lint-complexity lint-vulnerabilities \
	up-app-dependencies down-app-dependencies \
	admin-dependencies-file api-dependencies-file

.DEFAULT_GOAL := help

API_TARGETS = api/app api/tests api/settings
ADMIN_TARGETS = admin/app admin/tests
PYTHON_TARGETS = $(API_TARGETS) $(ADMIN_TARGETS)
BASE_PYPROJECT_FILES = pyproject.toml base-pyproject.toml

## Отформатировать код и исправить простые ошибки
format:
	uv run black $(PYTHON_TARGETS) && uv run ruff check --fix $(PYTHON_TARGETS)


## Проверить стиль кода и найти возможные ошибки
lint-style:
	uv run ruff check $(PYTHON_TARGETS) && uv run black --check $(PYTHON_TARGETS)


## Проверить подсказки типов в коде
lint-type-hints:
	uv run mypy $(PYTHON_TARGETS)


## Проверить сложность кода, а также найти возможные ошибки
lint-complexity:
	uv run flake8 $(PYTHON_TARGETS)


## Проверить код.
lint: lint-style lint-type-hints lint-complexity


## Запустить локальное окружение для приложения
up-app-dependencies:
	docker compose up -d


## Отключить локальное окружение для приложения
down-app-dependencies:
	docker compose down -v


## Создать файл pyproject.toml для сервиса админки
admin-dependencies-file:
	toml-union $(BASE_PYPROJECT_FILES) admin/admin-pyproject.toml -o admin/pyproject.toml

## Создать файл pyproject.toml для api сервиса
api-dependencies-file:
	toml-union $(BASE_PYPROJECT_FILES) api/api-pyproject.toml -o api/pyproject.toml

help:
	@awk '/^[a-zA-Z\-_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = $$1; sub(/:$$/, "", helpCommand); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}make %-$(TARGET_MAX_CHAR_NUM)25s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
