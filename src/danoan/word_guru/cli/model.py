from danoan.toml_dataclass import TomlDataClassIO

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ConfigurationFile(TomlDataClassIO):
    openai_key: Optional[str] = None
    cache_folder: Optional[Path] = None

    def __post_init__(self):
        if self.cache_folder:
            self.cache_folder = Path(self.cache_folder)
