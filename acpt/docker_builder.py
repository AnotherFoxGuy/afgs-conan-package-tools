import os
import tempfile

from acpt.printer import Printer
from acpt.utils import _utils_execute_script

pt = "ConanDockerBuilder"

class ConanDockerBuilder(object):

    def __init__(self, out=None):
        self.conanfile = None
        self.os = None
        self.compiler_version = None
        self.compiler_libcxx = None
        self.compiler_cppstd = None
        self.compiler = None
        self.build_type = None
        self.arch = None
        self.printer = Printer(out)
        self.printer.print_rule()
        self.printer.print_ascci_art()
        self.temp_folder = tempfile.mkdtemp()
        self.conan_cfg_path = _utils_execute_script("conan config home", True)

    def generate_config_files(self):
        base_dockerfile = """"
        ARG BASE_IMAGE
        FROM $BASE_IMAGE
        RUN apt-get update \
            && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
                build-essential cmake wget
            && curl "https://git.anotherfoxguy.com/AnotherFoxGuy/install-scripts/raw/branch/main/install-conan.sh" | bash
            && rm -rf /var/lib/apt/lists/*
        """
        dockerfile_path = self._write_tmp_file(base_dockerfile, "Dockerfile")

        base_configfile = f""""
        image: {self.os}-{self.compiler}-{self.compiler_version}-image
        build:
            dockerfile: {dockerfile_path}
            build_context: {os.curdir}
            build_args:
                BASE_IMAGE: ubuntu:22.04
        run:
            name: {self.os}-{self.compiler}-{self.compiler_version}-container
        """
        configfile_path = self._write_tmp_file(base_configfile, "configfile")

        host_profile = f""""
        [settings]
        arch={self.arch}
        build_type={self.build_type}
        compiler={self.compiler}
        compiler.cppstd={self.compiler_cppstd}
        compiler.libcxx={self.compiler_libcxx}
        compiler.version={self.compiler_version}
        os={self.os}

        [runner]
        type=docker
        configfile={configfile_path}
        cache=shared
        remove=true
        """
        host_profile_path = self._write_conan_file(host_profile, os.path.join("profiles", "host_profile"))

        build_profile = f""""
        [settings]
        arch={self.arch}
        build_type={self.build_type}
        compiler={self.compiler}
        compiler.cppstd={self.compiler_cppstd}
        compiler.libcxx={self.compiler_libcxx}
        compiler.version={self.compiler_version}
        os={self.os}
        """
        build_profile_path = self._write_conan_file(build_profile, os.path.join("profiles", "build_profile"))

        self.printer.print_message(pt, "Generated config files")

    def run(self):
        self.printer.print_message(pt, "Starting build")
        os.system(f'conan create {self.conanfile} --version 0.1 -pr:h host_profile -pr:b build_profile')

    def _write_tmp_file(self, contents, filename):
        path = os.path.join(self.temp_folder, filename)
        f = open(path, "w")
        f.write(contents)
        f.close()
        return path

    def _write_conan_file(self, contents, filename):
        path = os.path.join(self.conan_cfg_path, filename)
        f = open(path, "w")
        f.write(contents)
        f.close()
        return path
