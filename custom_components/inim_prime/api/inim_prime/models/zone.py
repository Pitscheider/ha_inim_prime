from dataclasses import dataclass
from enum import IntEnum

from inim_prime.models.panel_item import PanelItemStatus


class ZoneState(IntEnum):
    FAULT = 0
    READY = 1
    ALARM = 2
    SHORT_CIRCUIT = 3


@dataclass(frozen = True)
class ZoneStatus(PanelItemStatus):
    terminal: int  # "tl" - zone terminal
    state: ZoneState  # "st" - 0=fault, 1=ready, 2=alarm, 3=short circuit
    alarm_memory: bool  # "mm" - False=not present, True=present
    excluded: bool

    def __str__(self) -> str:
        return (
            f"Zone {self.id}: {self.name} (Terminal {self.terminal})\n"
            f"  State: {self.state.name}\n"
            f"  Alarm memory: {'Yes' if self.alarm_memory else 'No'}\n"
            f"  Excluded: {'Yes' if self.excluded else 'No'}"
        )

    def short_str(self) -> str:
        return f"Zone {self.id}: {self.name}"


from dataclasses import dataclass


@dataclass(frozen = True)
class ZoneExclusionSetRequest:
    zone_id: int
    exclude: bool = True  # True = excluded, False = included
