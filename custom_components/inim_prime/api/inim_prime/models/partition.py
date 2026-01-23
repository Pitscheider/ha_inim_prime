from dataclasses import dataclass
from enum import IntEnum

from .panel_item import PanelItemStatus


class PartitionMode(IntEnum):
    TOTAL = 1
    PARTIAL = 2
    INSTANT = 3
    DISARMED = 4


class PartitionArmMode(IntEnum):
    TOTAL = PartitionMode.TOTAL
    PARTIAL = PartitionMode.PARTIAL
    INSTANT = PartitionMode.INSTANT


class PartitionState(IntEnum):
    ALARM = 0
    READY = 1
    SABOTAGE = 2


@dataclass(frozen = True)
class PartitionStatus(PanelItemStatus):
    mode: PartitionMode
    state: PartitionState
    alarm_memory: bool

    def __str__(self) -> str:
        return (
            f"Partition {self.id}: {self.name}\n"
            f"  Mode: {self.mode.name}\n"
            f"  State: {self.state.name}\n"
            f"  Alarm memory: {'Yes' if self.alarm_memory else 'No'}"
        )


@dataclass(frozen = True)
class SetPartitionModeRequest:
    partition_id: int
    mode: PartitionMode


@dataclass(frozen = True)
class ClearPartitionAlarmMemoryRequest:
    partition_id: int
