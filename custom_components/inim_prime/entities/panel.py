from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.components.event import EventEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from custom_components.inim_prime.const import INIM_PRIME_DEVICE_MANUFACTURER, CONF_SERIAL_NUMBER
from inim_prime.models import LogEvent
from inim_prime.models.system_faults import SystemFault

def create_panel_device_info(
    entry: ConfigEntry,
    domain: str = DOMAIN,
) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(domain, entry.data[CONF_SERIAL_NUMBER])},
        name = "Inim Prime Panel",
        model = "Prime Panel",
        manufacturer = INIM_PRIME_DEVICE_MANUFACTURER,
        serial_number = entry.data[CONF_SERIAL_NUMBER],
    )



SYSTEM_FAULT_NAMES: dict[SystemFault, str] = {
    SystemFault.LOW_BATTERY: "Low Battery",
    SystemFault.NETWORK_FAULT: "Network Fault",
    SystemFault.NO_TELEPHONE_LINE: "No Telephone Line",
    SystemFault.RADIO_JAMMING: "Radio Jamming",
    SystemFault.LOW_BATTERY_WIRELESS: "Wireless Device Low Battery",
    SystemFault.WIRELESS_DEVICE_DISAPPEARANCE: "Wireless Device Missing",
    SystemFault.GSM_FAULT: "GSM Fault",
    SystemFault.SENSOR_DIRTY: "Sensor Dirty",
    SystemFault.ZONE_FAULT: "Zone Fault",
    SystemFault.SIRENS_FAULT: "Sirens Fault",
    SystemFault.POWER_SUPPLY_FAULT: "Power Supply Fault",
    SystemFault.RADIO_KEYBOARDS_FAULT: "Radio Keyboards Fault",
    SystemFault.SABOTAGE_FAULT: "Sabotage",
    SystemFault.INTERNET_FAULT: "Internet Fault",
}

SYSTEM_FAULT_ICONS: dict[SystemFault, str] = {
    SystemFault.LOW_BATTERY: "mdi:battery-alert",
    SystemFault.NETWORK_FAULT: "mdi:lan-disconnect",
    SystemFault.NO_TELEPHONE_LINE: "mdi:phone-off",
    SystemFault.RADIO_JAMMING: "mdi:signal-off",
    SystemFault.LOW_BATTERY_WIRELESS: "mdi:battery-alert-variant",
    SystemFault.WIRELESS_DEVICE_DISAPPEARANCE: "mdi:access-point-off",
    SystemFault.GSM_FAULT: "mdi:signal-off",
    SystemFault.SENSOR_DIRTY: "mdi:spray",
    SystemFault.ZONE_FAULT: "mdi:map-marker-alert",
    SystemFault.SIRENS_FAULT: "mdi:alarm-light-outline",
    SystemFault.POWER_SUPPLY_FAULT: "mdi:flash-alert",
    SystemFault.RADIO_KEYBOARDS_FAULT: "mdi:keyboard-off",
    SystemFault.SABOTAGE_FAULT: "mdi:alert-octagon",
    SystemFault.INTERNET_FAULT: "mdi:web-off",
}



class SystemFaultBinarySensor(
    CoordinatorEntity[InimPrimeDataUpdateCoordinator],
    BinarySensorEntity,
):
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: InimPrimeDataUpdateCoordinator,
        entry: ConfigEntry,
        fault: SystemFault,
    ):
        super().__init__(coordinator)

        self._fault = fault

        self._attr_name = SYSTEM_FAULT_NAMES.get(
            self._fault,
            self._fault.name.replace("_", " ").title()
        )

        self._attr_unique_id = f"{entry.data[CONF_SERIAL_NUMBER]}_panel_system_fault_{self._fault.name.lower()}"

        self._attr_icon = SYSTEM_FAULT_ICONS.get(
            self._fault,
            "mdi:alert-circle",
        )

        self._attr_device_info = create_panel_device_info(entry)

    @property
    def is_on(self) -> bool:
        system_faults = self.coordinator.data.system_faults
        return system_faults.has_fault(self._fault)

class PanelSupplyVoltageSensor(
    CoordinatorEntity[InimPrimeDataUpdateCoordinator],
    SensorEntity,
):
    _attr_name = "Supply Voltage"
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = "V"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_suggested_display_precision = 1

    def __init__(
        self,
        coordinator: InimPrimeDataUpdateCoordinator,
        entry: ConfigEntry,
    ):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data[CONF_SERIAL_NUMBER]}_panel_supply_voltage"
        self._attr_device_info = create_panel_device_info(entry)

    @property
    def native_value(self) -> float | None:
        """Return the supply voltage."""
        system_faults = self.coordinator.data.system_faults
        return system_faults.supply_voltage

class PanelLogEvents(
    CoordinatorEntity[InimPrimeDataUpdateCoordinator],
    EventEntity,
):
    _attr_name = "Log Events"
    _attr_event_types = ["generic"]

    def __init__(
        self,
        coordinator: InimPrimeDataUpdateCoordinator,
        entry: ConfigEntry,
    ):
        super().__init__(coordinator)

        self._attr_unique_id = f"{entry.data[CONF_SERIAL_NUMBER]}_panel_log_events"
        self._attr_device_info = create_panel_device_info(entry)

    @callback
    def handle_events(self, log_events: list[LogEvent]) -> None:
        for log_event in log_events:
            self._trigger_event(
                event_type = "generic",
                event_attributes = {
                    "timestamp": log_event.timestamp.isoformat(),
                    "type": log_event.type,
                    "agent": log_event.agent,
                    "location": log_event.location,
                }
            )
            self.async_write_ha_state(force_refresh=True)


    async def async_added_to_hass(self) -> None:
        """Register ourselves with the coordinator."""
        self.coordinator.panel_log_events_entity = self
