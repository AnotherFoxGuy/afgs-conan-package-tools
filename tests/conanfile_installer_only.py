from conan import ConanFile
from conan.tools.files import get, collect_libs
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout


class LibnameConan(ConanFile):
    name = "libname"
    version = "1.0.0"
    description = "Keep it short"
    topics = ("libname", "logging")
    url = "https://github.com/afgs/community"
    homepage = "https://github.com/original_author/original_lib"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports_sources = ["CMakeLists.txt"]

    settings = "os", "arch", "compiler", "build_type"

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        for req in self.conan_data["requirements"]:
            self.requires(req)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_module_file_name", "Libname")
        self.cpp_info.set_property("cmake_module_target_name", "Libname::Libname")
        self.cpp_info.set_property("cmake_file_name", "Libname")
        self.cpp_info.set_property("cmake_target_name", "Libname::Libname")
        self.cpp_info.libs = collect_libs(self)

