from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, FrozenSet


class SystemFault(IntEnum):
    # Byte 0
    RESERVED_0 = 0
    RESERVED_1 = 1
    LOW_BATTERY = 2
    NETWORK_FAULT = 3
    NO_TELEPHONE_LINE = 4
    RADIO_JAMMING = 5
    LOW_BATTERY_WIRELESS = 6
    WIRELESS_DEVICE_DISAPPEARANCE = 7

    # Byte 1
    GSM_FAULT = 8
    SENSOR_DIRTY = 9
    ZONE_FAULT = 10
    SIRENS_FAULT = 11
    POWER_SUPPLY_FAULT = 12
    RADIO_KEYBOARDS_FAULT = 13
    SABOTAGE_FAULT = 14
    INTERNET_FAULT = 15


EXPOSED_SYSTEM_FAULTS: FrozenSet[SystemFault] = frozenset({
    SystemFault.LOW_BATTERY,
    SystemFault.NETWORK_FAULT,
    SystemFault.NO_TELEPHONE_LINE,
    SystemFault.RADIO_JAMMING,
    SystemFault.LOW_BATTERY_WIRELESS,
    SystemFault.WIRELESS_DEVICE_DISAPPEARANCE,
    SystemFault.GSM_FAULT,
    SystemFault.SENSOR_DIRTY,
    SystemFault.ZONE_FAULT,
    SystemFault.SIRENS_FAULT,
    SystemFault.POWER_SUPPLY_FAULT,
    SystemFault.RADIO_KEYBOARDS_FAULT,
    SystemFault.SABOTAGE_FAULT,
    SystemFault.INTERNET_FAULT,
})


@dataclass(frozen = True)
class SystemFaultsStatus:
    supply_voltage: Optional[float]
    faults: FrozenSet[SystemFault]

    def __str__(self) -> str:
        lines = ["System Faults Status:"]

        if self.supply_voltage is not None:
            lines.append(f"  Supply voltage: {self.supply_voltage} V")

        if self.faults:
            lines.append("  Active faults:")
            for fault in sorted(self.faults, key = lambda f: f.value):
                lines.append(f"    - {fault.name}")
        else:
            lines.append("  No active faults")

        return "\n".join(lines)

    # ───────────────
    # Generic helpers
    # ───────────────

    @property
    def has_any_fault(self) -> bool:
        return bool(self.faults)

    def has_fault(self, fault: SystemFault) -> bool:
        return fault in self.faults

    def fault_count(self) -> int:
        return len(self.faults)

    # ─────────────────────
    # Exposure-aware helpers
    # ─────────────────────

    @property
    def exposed_faults(self) -> FrozenSet[SystemFault]:
        return self.faults & EXPOSED_SYSTEM_FAULTS

    @property
    def has_any_exposed_fault(self) -> bool:
        return bool(self.exposed_faults)

    @property
    def exposed_fault_count(self) -> int:
        return len(self.exposed_faults)
