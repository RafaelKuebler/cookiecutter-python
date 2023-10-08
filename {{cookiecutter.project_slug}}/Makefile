default: help

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done


SOURCE_DIR="{{cookiecutter.project_slug}}"

.PHONY: setup
setup: # Setup dev environment.
	python3 -m venv .venv && \
	. .venv/bin/activate && \
	pip install -r requirements.txt && \
	pip install -r requirements-dev.txt --use-pep517 && \
	pre-commit install

.PHONY: test
test: # Run all tests.
	. .venv/bin/activate && \
	PYTHONPATH=$(SOURCE_DIR) pytest

.PHONY: coverage
coverage: # Run test coverage.
	. .venv/bin/activate && \
	PYTHONPATH=$(SOURCE_DIR) coverage run --source=$(SOURCE_DIR) -m pytest && \
	coverage report --include "$(SOURCE_DIR)/**/*.py" && \
	coverage xml -i --include "$(SOURCE_DIR)/**/*.py" -o coverage.xml

.PHONY: check
check: # Perform style checks
	. .venv/bin/activate && \
	pre-commit run --all-files


.PHONY: maintain
maintain: # Run maintanance tooling.
	. .venv/bin/activate && \
	pre-commit autoupdate && \
	pur -r requirements.txt && \
	pur -r requirements-dev.txt
