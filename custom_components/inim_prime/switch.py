from . import InimPrimeDataUpdateCoordinator, DOMAIN
from .entities.zone import ZoneExclusionSwitch


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    zones = coordinator.data.zones

    entities = []

    for zone in zones.values():
        entities.append(ZoneExclusionSwitch(coordinator, entry, zone))

    async_add_entities(entities, update_before_add = True)
