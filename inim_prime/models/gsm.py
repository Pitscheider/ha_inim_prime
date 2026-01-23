from dataclasses import dataclass
from typing import Optional


@dataclass(frozen = True)
class GSMSStatus:
    supply_voltage: Optional[float]
    firmware_version: Optional[str]
    operator: Optional[str]
    signal_strength: Optional[int]  # percentage 0 - 100%
    credit: Optional[str]

    def __str__(self) -> str:
        parts = ["GSM Status:"]

        if self.supply_voltage is not None:
            parts.append(f"  Supply voltage: {self.supply_voltage} V")

        if self.firmware_version:
            parts.append(f"  Firmware version: {self.firmware_version}")

        if self.operator:
            parts.append(f"  Operator: {self.operator}")

        if self.signal_strength is not None:
            parts.append(f"  Signal strength: {self.signal_strength} %")

        if self.credit:
            parts.append(f"  Credit: {self.credit}")

        return "\n".join(parts)
