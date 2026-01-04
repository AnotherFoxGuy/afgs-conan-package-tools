import json
import os
import subprocess


def prepare_env(config: json):
    def _set_env_variable(var_name: str, value: str):
        print("{} = {}".format(var_name, value))
        os.environ[var_name] = value
        if compiler in ["VISUAL", "MSVC"]:
            os.system('echo {}={}>> {}'.format(var_name, value, os.getenv("GITHUB_ENV")))
        else:
            subprocess.run(
                'echo "{}={}" >> $GITHUB_ENV'.format(var_name, value),
                shell=True
            )

    compiler = config["compiler"]
    compiler_version = config["version"]
    build_type = config.get("buildType", "")

    _set_env_variable("APT_CWD", config["cwd"])
    _set_env_variable("CONAN_VERSION", config["recipe_version"])

    if compiler == "APPLE_CLANG":
        if "." not in compiler_version:
            compiler_version = "{}.0".format(compiler_version)

    _set_env_variable("CONAN_{}_VERSIONS".format(compiler), compiler_version)

    if build_type != "":
        _set_env_variable("CONAN_BUILD_TYPES", build_type)

    if compiler == "APPLE_CLANG":
        xcode_mapping = {
            "9.1": "/Applications/Xcode_9.4.1.app",
            "10.0": "/Applications/Xcode_10.3.app",
            "11.0": "/Applications/Xcode_11.5.app",
            "12.0": "/Applications/Xcode_12.4.app",
            "13.0": "/Applications/Xcode_13.2.1.app",
            "13.1": "/Applications/Xcode_13.4.1.app",
            "14.0": "/Applications/Xcode_14.0.1.app",
        }
        if compiler_version in xcode_mapping:
            subprocess.run(
                'sudo xcode-select -switch "{}"'.format(xcode_mapping[compiler_version]),
                shell=True
            )
            print('executing: xcode-select -switch "{}"'.format(xcode_mapping[compiler_version]))

        subprocess.run(
            'clang++ --version',
            shell=True
        )

    if compiler == "GCC" or compiler == "CLANG":
        subprocess.run('docker system prune --all --force --volumes', shell=True)
        subprocess.run('sudo rm -rf "/usr/local/share/boost"', shell=True)
        subprocess.run('sudo rm -rf "$AGENT_TOOLSDIRECTORY/CodeQL"', shell=True)
        subprocess.run('sudo rm -rf "$AGENT_TOOLSDIRECTORY/Ruby"', shell=True)
        subprocess.run('sudo rm -rf "$AGENT_TOOLSDIRECTORY/boost"', shell=True)
        subprocess.run('sudo rm -rf "$AGENT_TOOLSDIRECTORY/go"', shell=True)
        subprocess.run('sudo rm -rf "$AGENT_TOOLSDIRECTORY/node"', shell=True)

    subprocess.run("conan profile detect", shell=True)
