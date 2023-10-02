default: help

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: setup
setup: # Setup dev environment.
	python3 -m venv .venv && \
	. .venv/bin/activate && \
	pip install -r requirements.txt

.PHONY: bake
bake: # Generate project using defaults.
	. .venv/bin/activate && \
	cookiecutter --no-input . --overwrite-if-exists

.PHONY: test
test: # Run unit tests.
	. .venv/bin/activate && \
	pytest tests/

.PHONY: maintain
maintain: # Run maintanance tooling.
	. .venv/bin/activate && \
	pur -r requirements.txt
