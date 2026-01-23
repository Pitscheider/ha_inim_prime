from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen = True)
class LogEvent:
    id: int
    timestamp: datetime
    type: str
    agent: Optional[str]
    location: Optional[str]
    value: Optional[str] = None

    def __str__(self) -> str:
        parts = [
            self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            f"[#{self.id}]",
            f"type = {self.type}"
        ]

        if self.agent:
            parts.append(f"by {self.agent}")

        if self.location:
            parts.append(f"at {self.location}")

        if self.value:
            parts.append(f"({self.value})")

        return " ".join(parts)

    def __post_init__(self):
        # Use object.__setattr__ to modify fields in a frozen dataclass
        object.__setattr__(self, "type", self.type.strip())
        if self.agent:
            object.__setattr__(self, "agent", self.agent.strip())
        if self.location:
            object.__setattr__(self, "location", self.location.strip())
        if self.value:
            object.__setattr__(self, "value", self.value.strip())
