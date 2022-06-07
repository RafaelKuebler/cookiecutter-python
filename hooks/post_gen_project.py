#!/usr/bin/env python
from pathlib import Path

SRC_DIR = Path("{{cookiecutter.project_slug}}")

if __name__ == "__main__":
    if "no" in "{{ cookiecutter.command_line_interface|lower }}":
        cli_file = SRC_DIR / "cli.py"
        cli_file.unlink()
    else:
        main_file = SRC_DIR / "main.py"
        main_file.unlink()

    if "Not open source" == "{{ cookiecutter.open_source_license }}":  # type: ignore
        Path("LICENSE").unlink()
