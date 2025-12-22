from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from custom_components.inim_prime.const import INIM_PRIME_DEVICE_MANUFACTURER, INIM_PRIME_MODEL_ZONE
from inim_prime.models import ZoneState, ZoneStatus
from homeassistant.helpers.entity import DeviceInfo

def create_zone_device_info(
    zone_id: int,
    zone_name: str,
    domain: str = DOMAIN,
) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(domain, f"zone_{zone_id}")},
        name=f"Zone {zone_name}",
        model="Prime Zone",
    )


class ZoneStateBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: InimPrimeDataUpdateCoordinator, zone: ZoneStatus):
        super().__init__(coordinator)

        self.zone_id = zone.id
        self._attr_name = None
        self._attr_unique_id = f"{DOMAIN}_zone_{zone.id}_triggered"

        self._attr_device_info = create_zone_device_info(
            zone_id=self.zone_id,
            zone_name=zone.name,
        )

    @property
    def is_on(self) -> bool | None:
        zones = self.coordinator.data.get("zones", [])
        zone = next((z for z in zones if z.id == self.zone_id), None)
        if zone:
            if zone.state == ZoneState.ALARM:
                return True
            elif zone.state == ZoneState.READY:
                return False
        return None

class ZoneStateSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: InimPrimeDataUpdateCoordinator, zone: ZoneStatus):
        super().__init__(coordinator)

        self.zone_id = zone.id
        self._attr_name = "State"
        self._attr_unique_id = f"{DOMAIN}_zone_{zone.id}_state"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = [state.name for state in ZoneState]
        self._attr_icon = "mdi:magnify"

        self._attr_device_info = create_zone_device_info(
            zone_id=self.zone_id,
            zone_name=zone.name,
        )

    @property
    def native_value(self) -> str:
        zones: list[ZoneStatus] = self.coordinator.data.get("zones", [])
        zone = next((z for z in zones if z.id == self.zone_id), None)
        return zone.state.name

class ZoneAlarmMemoryBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor per l'alarm memory della zona."""

    def __init__(self, coordinator: InimPrimeDataUpdateCoordinator, zone: ZoneStatus):
        super().__init__(coordinator)

        self.zone_id = zone.id
        self._attr_name = "Alarm Memory"
        self._attr_unique_id = f"{DOMAIN}_zone_{zone.id}_alarm_memory"
        self._attr_icon = "mdi:alarm-light"

        self._attr_device_info = create_zone_device_info(
            zone_id=self.zone_id,
            zone_name=zone.name,
        )

    @property
    def is_on(self) -> bool | None:
        zones = self.coordinator.data.get("zones", [])
        zone = next((z for z in zones if z.id == self.zone_id), None)
        if zone:
            return zone.alarm_memory
        return None


class ZoneExcludedBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: InimPrimeDataUpdateCoordinator, zone: ZoneStatus):
        super().__init__(coordinator)

        self.zone_id = zone.id
        self._attr_name = "Excluded"
        self._attr_unique_id = f"{DOMAIN}_zone_{zone.id}_excluded"
        self._attr_icon = "mdi:cancel"

        self._attr_device_info = create_zone_device_info(
            zone_id=self.zone_id,
            zone_name=zone.name,
        )

    @property
    def is_on(self) -> bool | None:
        zones = self.coordinator.data.get("zones", [])
        zone = next((z for z in zones if z.id == self.zone_id), None)
        if zone:
            return zone.excluded
        return None
