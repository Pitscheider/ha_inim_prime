from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from custom_components.inim_prime.entities.partition import PartitionModeSelect


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    partitions = coordinator.data.partitions
    entities = []

    for partition in partitions.values():
        entities.append(PartitionModeSelect(coordinator, partition))

    async_add_entities(entities, update_before_add=True)