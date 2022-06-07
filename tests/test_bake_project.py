import datetime
import importlib
import os
import shlex
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, List, Tuple

from click.testing import CliRunner
from cookiecutter.utils import rmtree
from pytest import CaptureFixture
from pytest_cookies.plugin import Cookies, Result


@contextmanager
def inside_dir(dirpath: Path) -> Generator[None, None, None]:
    """
    Execute code from inside the given directory
    :param dirpath: Path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(str(dirpath))
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies: Cookies, *args: List[Any], **kwargs: Dict[str, Any]) -> Generator[Result, None, None]:
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result: Result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(result.project_path)


def run_inside_dir(command: str, dirpath: Path) -> int:
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


def project_info(result: Result) -> Tuple[Path, str, Path]:
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_slug = result.project_path.name
    project_dir = result.project_path / project_slug
    return result.project_path, project_slug, project_dir


def test_year_compute_in_license_file(cookies: Cookies) -> None:
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project_path / "LICENSE"
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read_text()


def test_bake_with_defaults(cookies: Cookies) -> None:
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path.is_dir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        expected_files = ["setup.py", "python_boilerplate", "tests"]
        for expected_file in expected_files:
            assert expected_file in found_toplevel_files


def test_bake_and_run_tests(cookies: Cookies) -> None:
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path.is_dir()
        assert run_inside_dir("make test", result.project_path) == 0


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
        with bake_in_temp_dir(cookies, extra_context=context) as result:
            assert target_string in (result.project_path / "LICENSE").read_text()
            assert license_ in (result.project_path / "setup.py").read_text()


def test_bake_not_open_source(cookies: Cookies) -> None:
    context = {"open_source_license": "Not open source"}
    with bake_in_temp_dir(cookies, extra_context=context) as result:
        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert "setup.py" in found_toplevel_files
        assert "LICENSE" not in found_toplevel_files
        assert "License" not in (result.project_path / "README.md").read_text()


def test_bake_with_no_console_script(cookies: Cookies) -> None:
    context = {"command_line_interface": "No command-line interface"}
    result = cookies.bake(extra_context=context)
    project_path, _, project_dir = project_info(result)
    found_project_files = [f.name for f in project_dir.iterdir()]
    assert "cli.py" not in found_project_files
    assert "main.py" in found_project_files
    assert "entry_points" not in (project_path / "setup.py").read_text()


def test_bake_with_console_script_files(cookies: Cookies) -> None:
    context = {"command_line_interface": "Click"}
    result = cookies.bake(extra_context=context)
    project_path, _, project_dir = project_info(result)
    found_project_files = [f.name for f in project_dir.iterdir()]
    assert "cli.py" in found_project_files
    assert "main.py" not in found_project_files

    setup_path = project_path / "setup.py"
    with open(setup_path, "r", encoding="utf-8") as setup_file:
        assert "entry_points" in setup_file.read()


def test_bake_with_argparse_console_script_files(cookies: Cookies) -> None:
    context = {"command_line_interface": "Argparse"}
    result = cookies.bake(extra_context=context)
    project_path, _, project_dir = project_info(result)
    found_project_files = [f.name for f in project_dir.iterdir()]
    assert "cli.py" in found_project_files
    assert "main.py" not in found_project_files

    setup_path = project_path / "setup.py"
    with open(setup_path, "r", encoding="utf-8") as setup_file:
        assert "entry_points" in setup_file.read()


def test_bake_with_console_script_cli(cookies: Cookies) -> None:
    context = {"command_line_interface": "Click"}
    result = cookies.bake(extra_context=context)
    _, project_slug, project_dir = project_info(result)
    module_path = project_dir / "cli.py"
    module_name = ".".join([project_slug, "cli"])
    spec = importlib.util.spec_from_file_location(module_name, module_path)  # type: ignore
    cli = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(cli)
    runner = CliRunner()
    noarg_result = runner.invoke(cli.main)
    assert noarg_result.exit_code == 0
    noarg_output = f"Replace this message by putting your code into {project_slug}"
    assert noarg_output in noarg_result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message" in help_result.output


def test_bake_with_argparse_console_script_cli(cookies: Cookies, capsys: CaptureFixture) -> None:
    context = {"command_line_interface": "Argparse"}
    result = cookies.bake(extra_context=context)
    _, project_slug, project_dir = project_info(result)
    module_path = project_dir / "cli.py"
    module_name = ".".join([project_slug, "cli"])
    spec = importlib.util.spec_from_file_location(module_name, module_path)  # type: ignore
    cli = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(cli)

    exit_code = cli.main()
    assert exit_code == 0
    noarg_output = f"Replace this message by putting your code into {project_slug}"
    assert noarg_output in capsys.readouterr().out
