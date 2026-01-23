from abc import ABC
from dataclasses import dataclass


@dataclass(frozen = True)
class PanelItemStatus(ABC):
    id: int
    name: str

    def __post_init__(self):
        # Clean up name: strip spaces, 16-char padded with spaces
        object.__setattr__(self, "name", self.name.strip())
