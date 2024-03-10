from danoan.word_guru.cli import model, exception

import os
from pathlib import Path

ENV_WORD_GURU = "WORD_GURU_CONFIGURATION_FOLDER"


def ensure_environment_variable_exist():
    if ENV_WORD_GURU not in os.environ:
        raise exception.EnvironmentVariableIsNotSet(environment_variable=ENV_WORD_GURU)
    return os.environ[ENV_WORD_GURU]


def ensure_configuration_file_exist():
    ensure_environment_variable_exist()
    configuration_filepath = Path(os.environ[ENV_WORD_GURU]) / "config.toml"
    if not configuration_filepath.exists():
        raise exception.ConfigurationFileDoesNotExist(
            configuration_filepath=configuration_filepath
        )
    return configuration_filepath


def get_configuration_file() -> model.ConfigurationFile:
    configuration_filepath = ensure_configuration_file_exist()

    with open(configuration_filepath, "r") as f:
        return model.ConfigurationFile.read(f)
