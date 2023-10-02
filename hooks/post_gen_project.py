from pathlib import Path

SRC_DIR = Path("{{cookiecutter.project_slug}}")

if "Not open source" == "{{ cookiecutter.open_source_license }}":  # type: ignore
    Path("LICENSE").unlink()
