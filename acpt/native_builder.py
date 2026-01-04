import os
import tempfile

from acpt.printer import Printer
from acpt.utils import _utils_execute_script

pt = "ConanNativeBuilder"


class ConanNativeBuilder(object):

    def __init__(self,
                 name=None,
                 out=None,
                 conanfile=None,
                 version=None,
                 username=None,
                 channel=None,
                 compiler_version=None,
                 compiler_libcxx=None,
                 compiler_cppstd=None,
                 compiler=None,
                 build_type=None,
                 arch=None,
                 remote=None
                 ):
        self.name = name
        self.conanfile = conanfile
        self.version = version
        self.user = username
        self.channel = channel
        self.compiler_version = compiler_version
        self.compiler_libcxx = compiler_libcxx
        self.compiler_cppstd = compiler_cppstd
        self.compiler = compiler
        self.build_type = build_type
        self.arch = arch
        self.remote = remote
        self.temp_folder = tempfile.mkdtemp()
        self.conan_cfg_path = _utils_execute_script("conan config home", True)

        self.printer = Printer(out)
        self.printer.print_rule()
        self.printer.print_ascci_art()

    def generate_config_files(self):
        host_profile = f""""
        [settings]
        arch={self.arch}
        build_type={self.build_type}
        compiler={self.compiler}
        compiler.cppstd={self.compiler_cppstd}
        compiler.libcxx={self.compiler_libcxx}
        compiler.version={self.compiler_version}
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
        """
        build_profile_path = self._write_conan_file(build_profile, os.path.join("profiles", "build_profile"))

        self.printer.print_message(pt, "Generated config files")

    def run(self):
        self.printer.print_message(pt, "Starting build")
        cmd_build = f"conan create {self.conanfile}"
        cmd_build += f" --version {self.version} -b missing"

        cmd_upload = f"conan upload {self.name}/{self.version}"

        if self.user and self.channel:
            cmd_build += f" --user {self.user} --channel {self.channel} "
            cmd_upload += f"@{self.user}/{self.channel} "

        os.system(f'{cmd_build} -pr:h host_profile -pr:b build_profile')
        os.system(f'{cmd_upload} -r {self.remote}')

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
