import datetime
from pathlib import Path
from typing import Tuple

import utils
from pytest_cookies.plugin import Cookies, Result


def project_info(result: Result) -> Tuple[Path, str, Path]:
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_slug = result.project_path.name
    project_dir = result.project_path / project_slug
    return result.project_path, project_slug, project_dir


def test_year_compute_in_license_file(cookies: Cookies) -> None:
    with utils.bake_in_temp_dir(cookies) as result:
        license_file_path = result.project_path / "LICENSE"
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read_text()


def test_bake_with_defaults(cookies: Cookies) -> None:
    with utils.bake_in_temp_dir(cookies) as result:
        assert result.project_path.is_dir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        expected_files = [
            "python_boilerplate",
            "tests",
            ".bumpversion.cfg",
            ".editorconfig",
            ".gitignore",
            ".pre-commit-config.yaml",
            "LICENSE",
            "Makefile",
            "pyproject.toml",
            "README.md",
            "requirements.txt",
            "requirements-dev.txt",
        ]
        for expected_file in expected_files:
            assert expected_file in found_toplevel_files


def test_bake_and_run_tests_and_style(cookies: Cookies) -> None:
    with utils.bake_in_temp_dir(cookies, dependencies=True) as result:
        assert result.project_path.is_dir()
        assert utils.run_inside_dir("make test", result.project_path) == 0
        assert utils.run_inside_dir("make check", result.project_path) == 0


def test_bake_selecting_license(cookies: Cookies) -> None:
    license_strings = {
        "MIT license": "MIT ",
        "BSD license": "Redistributions of source code must retain the above copyright notice, this",
        "ISC license": "ISC License",
        "Apache Software License 2.0": "Licensed under the Apache License, Version 2.0",
        "GNU General Public License v3": "GNU GENERAL PUBLIC LICENSE",
    }
    for license_, target_string in license_strings.items():
        context = {"open_source_license": license_}
        with utils.bake_in_temp_dir(cookies, extra_context=context) as result:
            assert target_string in (result.project_path / "LICENSE").read_text()


def test_bake_not_open_source(cookies: Cookies) -> None:
    context = {"open_source_license": "Not open source"}
    with utils.bake_in_temp_dir(cookies, extra_context=context) as result:
        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert "LICENSE" not in found_toplevel_files
        assert "License" not in (result.project_path / "README.md").read_text()


"""
def test_bake_with_no_console_script(cookies: Cookies) -> None:
    result = cookies.bake(extra_context=context)
    project_path, _, project_dir = project_info(result)
    found_project_files = [f.name for f in project_dir.iterdir()]
    assert "cli.py" not in found_project_files
    assert "main.py" in found_project_files
    assert "entry_points" not in (project_path / "setup.py").read_text()
"""
