from conan import ConanFile
from conan.tools.files import collect_libs, copy


class FoobarConan(ConanFile):
    name = "foobar"
    version = "0.1.0"
    settings = "os", "compiler", "build_type", "arch"
    description = "<Description of Foobar here>"
    options = {"shared": [True, False]}
    default_options = {
        "shared": False
    }
    url = "None"
    license = "None"

    def package(self):
        copy("*")

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
