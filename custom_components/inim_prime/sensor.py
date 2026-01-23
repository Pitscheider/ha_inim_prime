from .coordinators.coordinator import InimPrimeDataUpdateCoordinator
from .const import DOMAIN
from .entities.gsm import GSMSupplyVoltageSensor, GSMOperatorSensor, GSMSignalStrengthSensor, GSMCreditSensor
from .entities.panel import PanelSupplyVoltageSensor, ExcludedZonesCountSensor
from .entities.partition import PartitionStateSensor
from .entities.zone import ZoneStateSensor


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    zones = coordinator.data.zones
    partitions = coordinator.data.partitions
    entities = []

    for zone in zones.values():
        entities.append(ZoneStateSensor(coordinator, entry, zone))

    for partition in partitions.values():
        entities.append(PartitionStateSensor(coordinator, entry, partition))

    entities.append(PanelSupplyVoltageSensor(coordinator, entry))
    entities.append(GSMSupplyVoltageSensor(coordinator, entry))
    entities.append(GSMOperatorSensor(coordinator, entry))
    entities.append(GSMSignalStrengthSensor(coordinator, entry))
    entities.append(GSMCreditSensor(coordinator, entry))
    entities.append(ExcludedZonesCountSensor(coordinator, entry))

    async_add_entities(entities, update_before_add = True)
