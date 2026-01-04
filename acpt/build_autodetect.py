import sys
import subprocess
import tempfile
import os

from acpt.build_shared import printer, get_os
from acpt import build_shared
from acpt.autodetect import *
from acpt.utils import _utils_execute_script


def _flush_output():
    sys.stderr.flush()
    sys.stdout.flush()


def run_autodetect():
    ###
    # Enabling Conan download cache
    ###
    printer.print_message("Enabling Conan download cache ...")

    conan_cfg_path = _utils_execute_script("conan config home", True)
    tmpdir = tempfile.mkdtemp()

    # Setting values for conan.conf - Client behaviour
    f = open(os.path.join(conan_cfg_path, "global.conf"), "a")
    f.write("general.revisions_enabled=1\n")
    f.write(f"storage.download_cache={tmpdir}\n")
    f.write("tools.system.package_manager:mode=install\n")
    f.write("tools.system.package_manager:sudo=True\n")
    f.close()

    ###
    # Detect and execute custom build.py file if existing
    ###
    has_custom_build_py, custom_build_py_path = is_custom_build_py_existing()

    if has_custom_build_py:
        printer.print_message("Custom build.py detected. Executing ...")
        _flush_output()

        new_wd = os.path.dirname(custom_build_py_path)
        if new_wd == "":
            new_wd = ".{}".format(os.sep)

        # build.py files have no knowledge about the directory structure above them.
        # Delete the env variable or BPT is appending the path a second time
        # when build.py calls BPT
        if "APT_CWD" in os.environ:
            del os.environ["APT_CWD"]

        subprocess.run("python build.py", cwd=new_wd, shell=True, check=True)
        return

    ###
    # Start the build
    ###
    cwd = os.getenv("APT_CWD", "")
    recipe = build_shared.get_recipe_path(cwd)
    builder = build_shared.get_builder(cwd=cwd)
    builder.run()
