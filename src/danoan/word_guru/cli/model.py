from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class WordGuruConfiguration:
    openai_key: Optional[str] = None
    cache_path: Optional[Path] = None

    def __post_init__(self):
        if self.cache_path:
            self.cache_path = Path(self.cache_path)

    def __asdict__(self):
        d = asdict(self)
        if self.cache_path:
            d["cache_path"] = str(self.cache_path)

        return d
