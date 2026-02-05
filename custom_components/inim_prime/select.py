from .coordinators import InimPrimePartitionsUpdateCoordinator
from .const import DOMAIN, PARTITIONS_COORDINATOR
from .entities.partition import PartitionModeSelect


async def async_setup_entry(hass, entry, async_add_entities):
    coordinators = hass.data[DOMAIN][entry.entry_id]["coordinators"]

    partitions_coordinator: InimPrimePartitionsUpdateCoordinator = coordinators[PARTITIONS_COORDINATOR]

    entities = []

    for partition in partitions_coordinator.data.values():
        entities.append(PartitionModeSelect(partitions_coordinator, entry, partition))

    async_add_entities(entities, update_before_add = True)
