from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN

def create_gsm_device_info(
    domain: str = DOMAIN,
    sw_version: str = None
) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(domain, "gsm")},
        name="GSM",
        model="Prime",
        via_device=(domain, "panel"),
        sw_version=sw_version
    )

class GSMSupplyVoltageSensor(
    CoordinatorEntity[InimPrimeDataUpdateCoordinator],
    SensorEntity,
):

    _attr_name = "Supply Voltage"
    _attr_unique_id = f"{DOMAIN}_gsm_supply_voltage"
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = "V"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: InimPrimeDataUpdateCoordinator):
        super().__init__(coordinator)
        self._attr_device_info = create_gsm_device_info(
            sw_version= self.coordinator.data.gsm.firmware_version
        )

    @property
    def native_value(self) -> float | None:
        gsm = self.coordinator.data.gsm
        return gsm.supply_voltage
