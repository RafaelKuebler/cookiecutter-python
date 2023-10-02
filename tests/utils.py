import os
import shlex
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, List

import utils
from cookiecutter.utils import rmtree
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


def run_inside_dir(command: str, dirpath: Path) -> int:
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


@contextmanager
def bake_in_temp_dir(
    cookies: Cookies,
    dependencies: bool = False,
    *args: List[Any],
    **kwargs: Dict[str, Any]
) -> Generator[Result, None, None]:
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result: Result = cookies.bake(*args, **kwargs)
    try:
        if dependencies:
            assert utils.run_inside_dir("make setup", result.project_path) == 0
        yield result
    finally:
        rmtree(result.project_path)
