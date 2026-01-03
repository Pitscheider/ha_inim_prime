from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from custom_components.inim_prime.entities.area import AreaStateSensor, AreaModeSensor
from custom_components.inim_prime.entities.zone import ZoneStateSensor


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    zones = coordinator.data.zones
    areas = coordinator.data.areas
    entities = []

    for zone in zones.values():
        entities.append(ZoneStateSensor(coordinator, zone))

    for area in areas.values():
        entities.append(AreaStateSensor(coordinator, area))
        entities.append(AreaModeSensor(coordinator, area))

    async_add_entities(entities, update_before_add=True)