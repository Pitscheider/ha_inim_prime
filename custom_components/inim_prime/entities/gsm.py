from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from custom_components.inim_prime.const import INIM_PRIME_DEVICE_MANUFACTURER


def create_gsm_device_info(
    entry: ConfigEntry,
    domain: str = DOMAIN,
    sw_version: str = None
) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(domain, f"{entry.entry_id}_gsm")},
        name="GSM",
        model="Prime GSM",
        manufacturer=INIM_PRIME_DEVICE_MANUFACTURER,
        via_device=(domain, entry.entry_id),
        sw_version=sw_version,
    )

class GSMSupplyVoltageSensor(
    CoordinatorEntity[InimPrimeDataUpdateCoordinator],
    SensorEntity,
):
    _attr_name = "Supply Voltage"
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = "V"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
            self,
            coordinator: InimPrimeDataUpdateCoordinator,
            entry: ConfigEntry,
    ):
        super().__init__(coordinator)

        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_gsm_supply_voltage"

        self._attr_device_info = create_gsm_device_info(
            entry=entry,
            sw_version=self.coordinator.data.gsm.firmware_version,
        )

    @property
    def native_value(self) -> float | None:
        gsm = self.coordinator.data.gsm
        return gsm.supply_voltage


class GSMOperatorSensor(
    CoordinatorEntity[InimPrimeDataUpdateCoordinator],
    SensorEntity,
):
    _attr_name = "Operator"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:cellphone-wireless"

    def __init__(
            self,
            coordinator: InimPrimeDataUpdateCoordinator,
            entry: ConfigEntry,
    ):
        super().__init__(coordinator)

        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_gsm_operator"

        self._attr_device_info = create_gsm_device_info(
            entry=entry,
            sw_version=self.coordinator.data.gsm.firmware_version
        )

    @property
    def native_value(self) -> str | None:
        gsm = self.coordinator.data.gsm
        return gsm.operator

class GSMSignalStrengthSensor(
    CoordinatorEntity[InimPrimeDataUpdateCoordinator],
    SensorEntity,
):
    _attr_name = "Signal Strength"
    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
            self,
            coordinator: InimPrimeDataUpdateCoordinator,
            entry: ConfigEntry,
    ):
        super().__init__(coordinator)

        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_gsm_signal_strength"

        self._attr_device_info = create_gsm_device_info(
            entry=entry,
            sw_version=self.coordinator.data.gsm.firmware_version,
        )

    @property
    def native_value(self) -> float | None:
        gsm = self.coordinator.data.gsm
        return gsm.signal_strength

class GSMCreditSensor(
    CoordinatorEntity[InimPrimeDataUpdateCoordinator],
    SensorEntity,
):
    _attr_name = "Credit"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:cash-multiple"

    def __init__(
            self,
            coordinator: InimPrimeDataUpdateCoordinator,
            entry: ConfigEntry,
    ):
        super().__init__(coordinator)

        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_gsm_credit"

        self._attr_device_info = create_gsm_device_info(
            entry=entry,
            sw_version=self.coordinator.data.gsm.firmware_version,
        )

    @property
    def native_value(self) -> str | None:
        gsm = self.coordinator.data.gsm
        return gsm.credit