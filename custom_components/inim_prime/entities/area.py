from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from inim_prime.models import AreaStatus, AreaState
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from homeassistant.helpers.entity import DeviceInfo

from inim_prime.models.area import SetAreaModeRequest, AreaMode


def create_area_device_info(
    area_id: int,
    area_name: str,
    domain: str = DOMAIN,
) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(domain, f"area_{area_id}")},
        name=f"Area {area_name}",
        model="Prime Area",
    )

class AreaStateSensor(CoordinatorEntity[InimPrimeDataUpdateCoordinator], SensorEntity):
    def __init__(self, coordinator: InimPrimeDataUpdateCoordinator, area: AreaStatus):
        super().__init__(coordinator)

        self.area_id = area.id
        self._attr_name = "State"
        self._attr_unique_id = f"{DOMAIN}_area_{area.id}_state"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = [state.name for state in AreaState]
        self._attr_icon = "mdi:magnify"

        self._attr_device_info = create_area_device_info(
            area_id = self.area_id,
            area_name = area.name,
        )


    @property
    def native_value(self) -> str | None:
        area = self.coordinator.data.areas.get(self.area_id)
        if area:
            return area.state.name
        return None

# class AreaModeSensor(CoordinatorEntity[InimPrimeDataUpdateCoordinator], SensorEntity):
#     def __init__(self, coordinator: InimPrimeDataUpdateCoordinator, area: AreaStatus):
#         super().__init__(coordinator)
#
#         self.area_id = area.id
#         self._attr_name = "Mode"
#         self._attr_unique_id = f"{DOMAIN}_area_{area.id}_mode"
#         self._attr_device_class = SensorDeviceClass.ENUM
#         self._attr_options = [state.name for state in AreaMode]
#         self._attr_icon = "mdi:shield-lock"
#
#         self._attr_device_info = create_area_device_info(
#             area_id=self.area_id,
#             area_name=area.name,
#         )
#
#     @property
#     def native_value(self) -> str | None:
#         area = self.coordinator.data.areas.get(self.area_id)
#         if area:
#             return area.mode.name
#         return None

class AreaModeSelect(
    CoordinatorEntity[InimPrimeDataUpdateCoordinator],
    SelectEntity,
):
    """Select entity to control area arming mode."""

    def __init__(self, coordinator: InimPrimeDataUpdateCoordinator, area):
        super().__init__(coordinator)

        self.area_id = area.id

        self._attr_name = "Mode"
        self._attr_unique_id = f"{DOMAIN}_area_{area.id}_mode"
        self._attr_icon = "mdi:shield-lock"

        # Options shown in UI
        self._attr_options = [mode.name for mode in AreaMode]

        self._attr_device_info = create_area_device_info(
            area_id=self.area_id,
            area_name=area.name,
        )

    @property
    def current_option(self) -> str | None:
        """Return the current area mode."""
        area = self.coordinator.data.areas.get(self.area_id)
        if area:
            return area.mode.name
        return None

    async def async_select_option(self, option: str) -> None:
        """Set a new area mode."""
        mode = AreaMode[option]

        request = SetAreaModeRequest(
            area_id=self.area_id,
            mode=mode,
        )

        await self.coordinator.client.set_area_mode(request)
        await self.coordinator.async_request_refresh()

class AreaAlarmMemoryBinarySensor(CoordinatorEntity[InimPrimeDataUpdateCoordinator], BinarySensorEntity):

    def __init__(self, coordinator: InimPrimeDataUpdateCoordinator, area: AreaStatus):
        super().__init__(coordinator)

        self.area_id = area.id
        self._attr_name = "Alarm Memory"
        self._attr_unique_id = f"{DOMAIN}_area_{area.id}_alarm_memory"
        self._attr_icon = "mdi:alarm-light"

        self._attr_device_info = create_area_device_info(
            area_id = self.area_id,
            area_name = area.name,
        )

    @property
    def is_on(self) -> bool | None:
        area = self.coordinator.data.areas.get(self.area_id)
        if area:
            return area.alarm_memory
        return None