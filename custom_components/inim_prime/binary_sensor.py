from typing import Dict, Any

from inim_prime.models import ZoneStatus

from .coordinator import InimPrimeDataUpdateCoordinator
from .entities.area import AreaStateSensor
from .entities.zone import ZoneStateBinarySensor, ZoneAlarmMemoryBinarySensor


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Set up INIM Prime binary sensors from a config entry."""
    coordinator: InimPrimeDataUpdateCoordinator = hass.data["inim_prime"][entry.entry_id]["coordinator"]

    entities = []

    zones = coordinator.data.zones
    areas = coordinator.data.areas

    for zone in zones.values():
        entities.append(ZoneStateBinarySensor(coordinator, zone))
        entities.append(ZoneAlarmMemoryBinarySensor(coordinator, zone))

    for area in areas.values():
        entities.append(AreaStateSensor(coordinator, area))

    async_add_entities(entities, update_before_add=True)