from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from inim_prime.models.system_faults import EXPOSED_SYSTEM_FAULTS
from .entities.panel import SystemFaultBinarySensor
from .entities.partition import PartitionAlarmMemoryBinarySensor
from .entities.zone import ZoneStateBinarySensor, ZoneAlarmMemoryBinarySensor


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Set up INIM Prime binary sensors from a config entry."""
    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = []

    zones = coordinator.data.zones
    partitions = coordinator.data.partitions

    for zone in zones.values():
        entities.append(ZoneStateBinarySensor(coordinator, entry, zone))
        entities.append(ZoneAlarmMemoryBinarySensor(coordinator, entry, zone))

    for partition in partitions.values():
        entities.append(PartitionAlarmMemoryBinarySensor(coordinator, entry, partition))

    for exposedSystemFault in EXPOSED_SYSTEM_FAULTS:
        entities.append(
            SystemFaultBinarySensor(coordinator, entry, exposedSystemFault)
        )

    async_add_entities(entities, update_before_add = True)
