from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from custom_components.inim_prime.sensors.zone_sensors import ZoneStateSensor
from inim_prime.models import ZoneStatus


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    zones: list[ZoneStatus] = coordinator.data.get("zones", [])

    entities = []

    for zone in zones:
        entities.append(ZoneStateSensor(coordinator, zone))


    async_add_entities(entities, update_before_add=True)