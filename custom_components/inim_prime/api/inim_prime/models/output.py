from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

from inim_prime.models.panel_item import PanelItemStatus


class OutputType(IntEnum):
    NORMAL_HYBRID = 0
    DIMMING = 1
    DAC = 2
    VOLT_0_10V = 3


@dataclass(frozen = True)
class OutputStatus(PanelItemStatus):
    terminal: int  # "tl" - output terminal
    state: int
    type: OutputType
    voltage: Optional[float] = None  # "v" only for dimming outputs
    power: Optional[float] = None  # "p" only for dimming outputs
    cos_phi: Optional[float] = None  # "c" only for dimming outputs

    @property
    def is_dimming(self) -> bool:
        return self.type == OutputType.DIMMING

    def __str__(self) -> str:
        base = (
            f"Output {self.id}: {self.name} (Terminal {self.terminal})\n"
            f"  Type: {self.type.name}\n"
            f"  State: {self.state}"
        )
        if self.is_dimming:
            base += (
                f"\n  Voltage: {self.voltage if self.voltage is not None else 'N/A'}"
                f"\n  Power: {self.power if self.power is not None else 'N/A'}"
                f"\n  Cos φ: {self.cos_phi if self.cos_phi is not None else 'N/A'}"
            )
        return base


@dataclass(frozen = True)
class OutputSetRequest:
    output_id: int
    value: int  # 0 = off, 1 = on, 1..100 = dimming
