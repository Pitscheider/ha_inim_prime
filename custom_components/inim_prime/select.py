from .coordinators.coordinator import InimPrimeDataUpdateCoordinator
from .const import DOMAIN
from .entities.partition import PartitionModeSelect


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    partitions = coordinator.data.partitions
    entities = []

    for partition in partitions.values():
        entities.append(PartitionModeSelect(coordinator, entry, partition))

    async_add_entities(entities, update_before_add = True)
