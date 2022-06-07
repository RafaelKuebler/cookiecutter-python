
all: setup style test

.PHONY: help
help:
	@echo "setup 	setup dev environment"
	@echo "bake 	generate project using defaults"

.PHONY: setup
setup:
	direnv allow
	. .direnv/python-*/bin/activate; \
	pip install -r requirements-dev.txt

.PHONY: test
test:
	pytest

.PHONY: bake
bake:
	cookiecutter --no-input . --overwrite-if-exists

.PHONY: style
style:
	pre-commit run --all-files
