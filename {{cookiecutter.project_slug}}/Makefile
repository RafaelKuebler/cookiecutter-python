SOURCE_DIR="{{cookiecutter.project_slug}}"

.PHONY: setup
setup:
	direnv allow
	. .direnv/python-*/bin/activate; \
	pip install -r requirements-dev.txt

.PHONY: test
test:
	PYTHONPATH=$(SOURCE_DIR) pytest tests/

.PHONY: coverage
coverage:
	PYTHONPATH=$(SOURCE_DIR) coverage run --source=$(SOURCE_DIR) -m pytest
	coverage report --include "$(SOURCE_DIR)/**/*.py"
	coverage xml -i --include "$(SOURCE_DIR)/**/*.py" -o coverage.xml
