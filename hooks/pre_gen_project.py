import os
import re
import sys

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

module_name = "{{ cookiecutter.project_slug }}"

module_name_no_dash = re.match(MODULE_REGEX, module_name)
if not module_name_no_dash:
    print(
        f"ERROR: The project slug ({module_name}) is not a valid Python module name."
        "Please do not use a - and use _ instead"
    )
    sys.exit(1)  # cancel the project baking

os.system("git init")
