from .coordinators import InimPrimeZonesUpdateCoordinator, InimPrimePartitionsUpdateCoordinator
from .const import DOMAIN, ZONES_COORDINATOR, PARTITIONS_COORDINATOR
from .entities.panel import IncludeAllZonesButton, ClearAllPartitionsAlarmMemoryButton
from .entities.partition import ClearPartitionAlarmMemoryButton


async def async_setup_entry(hass, entry, async_add_entities):
    coordinators = hass.data[DOMAIN][entry.entry_id]["coordinators"]

    partitions_coordinator: InimPrimePartitionsUpdateCoordinator = coordinators[PARTITIONS_COORDINATOR]
    zones_coordinator: InimPrimeZonesUpdateCoordinator = coordinators[ZONES_COORDINATOR]

    entities = []

    for partition in partitions_coordinator.data.values():
        entities.append(ClearPartitionAlarmMemoryButton(partitions_coordinator, entry, partition))

    entities.append(IncludeAllZonesButton(zones_coordinator, entry))
    entities.append(ClearAllPartitionsAlarmMemoryButton(partitions_coordinator, entry))

    async_add_entities(entities, update_before_add = True)