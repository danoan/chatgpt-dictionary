from danoan.toml_dataclass import TomlDataClassIO

from dataclasses import dataclass
from typing import Optional


@dataclass
class ConfigurationFile(TomlDataClassIO):
    openai_key: Optional[str] = None
