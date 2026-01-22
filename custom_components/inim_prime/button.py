from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from custom_components.inim_prime.entities.panel import IncludeAllZonesButton, ClearAllPartitionsAlarmMemoryButton
from custom_components.inim_prime.entities.partition import ClearPartitionAlarmMemoryButton


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    partitions = coordinator.data.partitions
    entities = []

    for partition in partitions.values():
        entities.append(ClearPartitionAlarmMemoryButton(coordinator, entry, partition))

    entities.append(IncludeAllZonesButton(coordinator, entry))
    entities.append(ClearAllPartitionsAlarmMemoryButton(coordinator, entry))

    async_add_entities(entities, update_before_add = True)
