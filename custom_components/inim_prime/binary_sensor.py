from typing import Dict, Any

from inim_prime.models import ZoneStatus
from .sensors.zone_sensors import ZoneStateSensor, ZoneAlarmMemoryBinarySensor, ZoneExcludedBinarySensor, \
    ZoneStateBinarySensor
from .coordinator import InimPrimeDataUpdateCoordinator



async def async_setup_entry(hass, entry, async_add_entities):
    """Set up INIM Prime binary sensors from a config entry."""
    coordinator: InimPrimeDataUpdateCoordinator = hass.data["inim_prime"][entry.entry_id]["coordinator"]

    entities = []

    zones: list[ZoneStatus] = coordinator.data.get("zones", [])

    for zone in zones:
        entities.append(ZoneStateBinarySensor(coordinator, zone))
        entities.append(ZoneAlarmMemoryBinarySensor(coordinator, zone))
        entities.append(ZoneExcludedBinarySensor(coordinator, zone))

    async_add_entities(entities, update_before_add=True)