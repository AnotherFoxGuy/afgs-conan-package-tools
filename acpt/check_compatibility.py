import os

MINIMUM_CONFIG_FILE_VERSIONS = {
    "generate-ci-jobs": 11
}


def get_config_file_version() -> int:
    return int(os.getenv("APT_CONFIG_FILE_VERSION", 0))


def get_minimum_compatible_version(feature: str) -> int:
    if feature not in ["generate-ci-jobs", ]:
        raise ValueError("Unknown feature value {}".format(feature))

    return MINIMUM_CONFIG_FILE_VERSIONS[feature]


def is_ci_config_compatible(feature: str) -> bool:
    config_version = get_config_file_version()
    minimum_version = get_minimum_compatible_version(feature=feature)

    if config_version < minimum_version:
        return False

    return True
