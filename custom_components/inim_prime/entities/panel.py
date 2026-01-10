from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.const import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from inim_prime.models.system_faults import SystemFault

def create_panel_device_info(
    domain: str = DOMAIN,
) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(domain, "panel")},
        name="INIM Prime Panel",
        model="Prime",
    )

SYSTEM_FAULT_NAMES: dict[SystemFault, str] = {
    SystemFault.LOW_BATTERY: "Low Battery",
    SystemFault.NETWORK_FAULT: "Network Fault",
    SystemFault.NO_TELEPHONE_LINE: "No Telephone Line",
    SystemFault.RADIO_JAMMING: "Radio Jamming",
    SystemFault.LOW_BATTERY_WIRELESS: "Wireless Device Low Battery",
    SystemFault.GSM_FAULT: "GSM Fault",
    SystemFault.INTERNET_FAULT: "Internet Fault",
    SystemFault.SABOTAGE_FAULT: "Sabotage",
}

SYSTEM_FAULT_ICONS: dict[SystemFault, str] = {
    SystemFault.LOW_BATTERY: "mdi:battery-alert",
    SystemFault.NETWORK_FAULT: "mdi:lan-disconnect",
    SystemFault.INTERNET_FAULT: "mdi:web-off",
    SystemFault.GSM_FAULT: "mdi:signal-off",
    SystemFault.POWER_SUPPLY_FAULT: "mdi:flash-alert",
    SystemFault.SABOTAGE_FAULT: "mdi:alert-octagon",
}


class SystemFaultBinarySensor(
    CoordinatorEntity[InimPrimeDataUpdateCoordinator],
    BinarySensorEntity,
):
    """Binary sensor for a system fault."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: InimPrimeDataUpdateCoordinator,
        fault: SystemFault,
    ):
        super().__init__(coordinator)

        self._fault = fault

        self._attr_name = SYSTEM_FAULT_NAMES.get(
            fault,
            fault.name.replace("_", " ").title()
        )
        self._attr_unique_id = f"{DOMAIN}_panel_fault_{fault.name.lower()}"

        self._attr_icon = SYSTEM_FAULT_ICONS.get(
            fault,
            "mdi:alert-circle",
        )

        self._attr_device_info = create_panel_device_info()

    @property
    def is_on(self) -> bool:
        system_faults = self.coordinator.data.system_faults
        return system_faults.has_fault(self._fault)
