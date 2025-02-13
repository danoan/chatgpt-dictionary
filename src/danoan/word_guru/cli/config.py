"""
word-guru CLI configuration
"""

from danoan.word_guru.cli import exception
from danoan.word_guru.cli import model

from functools import lru_cache
import os
from pathlib import Path
import toml
from typing import Optional


########################################
# Configuration files
########################################

WORD_GURU_ENV_VARIABLE = "WORD_GURU_CONFIGURATION_FOLDER"
WORD_GURU_CONFIGURATION_FILENAME = "word-guru-config.toml"


@lru_cache
def _get_first_configuration_filepath_within_file_hierarchy(
    base_dir: Path,
) -> Optional[Path]:
    """
    Traverses the parents of the working directory until
    the configuration file is found.
    """
    visited = set()
    folders_to_visit = [base_dir]
    while len(folders_to_visit) > 0:
        cur_folder = folders_to_visit.pop()
        if cur_folder in visited:
            break
        # TODO: logger.debug(f"Visiting {cur_folder}")
        visited.add(cur_folder)
        folders_to_visit.append(cur_folder.parent)
        for p in cur_folder.iterdir():
            if not p.is_dir():
                if p.name == WORD_GURU_CONFIGURATION_FILENAME:
                    return p
                continue
    return None


def get_configuration_folder() -> Path:
    """
    Return directory where configuration file is stored.

    First checks if a configuration file exists in the file hierarchy.
    If that is the case, return the directory where the configuration file
    is located.

    If the procedure above does not find a configuration file, return the
    value stored in the environment variable WORD_GURU_ENV_VARIABLE.

    If the environment variable is not defined, raise an error.

    Raises:
        EnvironmentVariableNotDefinedError: If the WORD_GURU_ENV_VARIABLE
                                            is not defined and a configuration file
                                            is not found in the file hierarchy
    """
    # TODO: logger.debug("Start hierarchical search of configuation file")
    config_filepath = _get_first_configuration_filepath_within_file_hierarchy(
        Path(os.getcwd())
    )
    if config_filepath:
        return config_filepath.parent

    # TODO: logger.debug(
    #     "Hierarchical search failed. Check environment variable {WORD_GURU_ENV_VARIABLE}"
    # )
    if WORD_GURU_ENV_VARIABLE in os.environ:
        return Path(os.environ[WORD_GURU_ENV_VARIABLE]).expanduser()

    raise exception.EnvironmentVariableNotDefinedError()


def get_environment_variable_value() -> Path:
    f"""
    Return the value stored by {WORD_GURU_ENV_VARIABLE}.

    Raises:
        EnvironmentVariableNotDefinedError: If the WORD_GURU_ENV_VARIABLE
                                            is not defined and a configuration file
                                            is not found in the file hierarchy
    """
    if WORD_GURU_ENV_VARIABLE in os.environ:
        return Path(os.environ[WORD_GURU_ENV_VARIABLE]).expanduser()

    raise exception.EnvironmentVariableNotDefinedError()


def get_configuration_filepath() -> Path:
    """
    Return path to word-guru configuration file.
    """
    return get_configuration_folder() / WORD_GURU_CONFIGURATION_FILENAME


def get_configuration() -> model.WordGuruConfiguration:
    """
    Return configuration object.
    """
    config_filepath = get_configuration_filepath()
    if not config_filepath.exists():
        raise exception.ConfigurationFileDoesNotExistError()

    with open(config_filepath, "r") as f:
        return model.WordGuruConfiguration(**toml.load(f))


def get_absolute_configuration_path(path: Path):
    """
    Get absolute path of a configuration parameter.

    Paths in the configuration file are given relative to the location of
    the configuration file. This function resolves to its absolute path.
    """
    if path.is_absolute():
        return path
    else:
        return get_configuration_folder() / path
