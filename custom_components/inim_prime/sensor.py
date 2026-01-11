from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from custom_components.inim_prime.entities.partition import PartitionStateSensor
from custom_components.inim_prime.entities.gsm import GSMSupplyVoltageSensor, GSMOperatorSensor, \
    GSMSignalStrengthSensor, GSMCreditSensor
from custom_components.inim_prime.entities.panel import PanelSupplyVoltageSensor
from custom_components.inim_prime.entities.zone import ZoneStateSensor


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    zones = coordinator.data.zones
    partitions = coordinator.data.partitions
    entities = []

    for zone in zones.values():
        entities.append(ZoneStateSensor(coordinator, zone))

    for partition in partitions.values():
        entities.append(PartitionStateSensor(coordinator, entry, partition))

    entities.append(PanelSupplyVoltageSensor(coordinator,entry))
    entities.append(GSMSupplyVoltageSensor(coordinator))
    entities.append(GSMOperatorSensor(coordinator))
    entities.append(GSMSignalStrengthSensor(coordinator))
    entities.append(GSMCreditSensor(coordinator))

    async_add_entities(entities, update_before_add=True)