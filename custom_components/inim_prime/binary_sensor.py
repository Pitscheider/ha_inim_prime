from typing import Dict, Any

from inim_prime.models import ZoneStatus

from .coordinator import InimPrimeDataUpdateCoordinator
from .entities.zones import ZoneStateBinarySensor, ZoneExcludedBinarySensor, ZoneAlarmMemoryBinarySensor


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Set up INIM Prime binary sensors from a config entry."""
    coordinator: InimPrimeDataUpdateCoordinator = hass.data["inim_prime"][entry.entry_id]["coordinator"]

    entities = []

    zones = coordinator.data.zones

    for zone in zones.values():
        entities.append(ZoneStateBinarySensor(coordinator, zone))
        entities.append(ZoneAlarmMemoryBinarySensor(coordinator, zone))
        entities.append(ZoneExcludedBinarySensor(coordinator, zone))

    async_add_entities(entities, update_before_add=True)