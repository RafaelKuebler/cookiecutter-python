# Cookiecutter for Python

A [cookiecutter] template meant to serve as a starting point for new Python projects.

It is by no means a fully configured project. Rather, it attempt to include some commonly used tools and configuration for linters, static code checkers, pre-commit hooks, etc.

## Quickstart

Install the latest Cookiecutter:

```bash
pip install -U cookiecutter
```

Generate a Python package project:

```bash
cookiecutter https://github.com/RafaelKuebler/cookiecutter-python
```

## Features

- [Makefile] for setup, testing, and maintenance tasks
- Testing setup with [pytest] and [coverage]
- [pydantic] for app configuration parsing
- [pre-commit] for git pre-commit hooks
  - [isort] for security checks
  - [ruff] for linting
  - [bandit] for common security issues
  - [mypy] for static type hint checks
  - [black] for code formatting
  - other formatting: newline at the end of files, no trailing whitespace, etc
- Licensing: MIT, BSD license, ISC license, Apache Software License 2.0, or GNU General Public License v3

## WIP

- [bump2version](https://github.com/c4urself/bump2version)
- [Sphinx](http://sphinx-doc.org/) docs
- [Poetry](https://python-poetry.org/) v/s `requirements.txt`
- mkdocs

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

[cookiecutter]: <https://cookiecutter.readthedocs.io/>
[Makefile]: <https://www.gnu.org/software/make/manual/make.html>
[pytest]: <https://docs.pytest.org/>
[coverage]: <https://coverage.readthedocs.io/>
[pydantic]: <https://docs.pydantic.dev/>
[pre-commit]: <https://pre-commit.com/>
[isort]: <https://pycqa.github.io/isort/>
[ruff]: <https://github.com/astral-sh/ruff>
[bandit]: <https://bandit.readthedocs.io/>
[mypy]: <https://mypy.readthedocs.io/>
[black]: <https://black.readthedocs.io/>
