from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from custom_components.inim_prime.entities.area import AreaModeSelect, ClearAreaAlarmMemoryButton


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    areas = coordinator.data.areas
    entities = []

    for area in areas.values():
        entities.append(ClearAreaAlarmMemoryButton(coordinator, area))

    async_add_entities(entities, update_before_add=True)