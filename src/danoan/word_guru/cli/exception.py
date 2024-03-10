from pathlib import Path


class EnvironmentVariableIsNotSet(Exception):
    def __init__(self, environment_variable: str):
        self.environment_variable = environment_variable


class ConfigurationFileDoesNotExist(Exception):
    def __init__(self, configuration_filepath: Path):
        self.configuration_filepath = configuration_filepath
