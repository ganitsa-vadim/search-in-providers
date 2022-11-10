# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
WHITE  := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)

.DEFAULT_GOAL := help
.PHONY: help setup run lint type flake8 mypy test testcov run clean

VENV=.venv
PYTHON=$(VENV)/bin/python

## Initialize venv and install dependencies
setup: $(VENV)/bin/activate
$(VENV)/bin/activate:
	python -m venv $(VENV)
	$(PYTHON) -m pip install pipenv==2022.1.8
	$(PYTHON) -m pipenv sync -d

## Run app
run: setup
	. ./.env
	$(PYTHON) -m app.api

## Analyze project source code for slylistic errors
lint: setup
	$(PYTHON) -m flake8 app

## Analyze project source code for typing errors
type: setup
	$(PYTHON) -m mypy app

## Run flake8
flake8: setup
	$(PYTHON) -m flake8 app

## Run mypy
mypy: setup
	$(PYTHON) -m mypy app

## Run project tests
test: setup
	$(PYTHON) -m pytest

## Run project tests and open HTML coverage report
testcov: setup
	$(PYTHON) -m pytest --cov-report=html
	xdg-open htmlcov/index.html

## Clean up project environment
clean:
	rm -rf $(VENV) *.egg-info .eggs .coverage htmlcov .pytest_cache
	find . -type f -name '*.pyc' -delete

## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = $$1; sub(/:$$/, "", helpCommand); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)15s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''
