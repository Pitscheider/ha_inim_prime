import logging
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from inim_prime import InimPrimeClient
from inim_prime.models import OutputStatus, SystemFaultsStatus, GSMSStatus
from inim_prime.models.partition import PartitionStatus
from inim_prime.models.zone import ZoneStatus

_LOGGER = logging.getLogger(__name__)


@dataclass
class CoordinatorData:
    system_faults: SystemFaultsStatus = SystemFaultsStatus(
        supply_voltage = None,
        faults = frozenset(),
    )
    gsm: GSMSStatus = GSMSStatus(
        supply_voltage = None,
        firmware_version = None,
        operator = None,
        signal_strength = None,
        credit = None,
    )
    zones: Dict[int, ZoneStatus] = field(default_factory = dict)
    partitions: Dict[int, PartitionStatus] = field(default_factory = dict)
    outputs: Dict[int, OutputStatus] = field(default_factory = dict)


class InimPrimeDataUpdateCoordinator(DataUpdateCoordinator[CoordinatorData]):
    """Coordinator to fetch data from the panel."""
    STORAGE_VERSION = 1

    def __init__(
            self,
            hass: HomeAssistant,
            update_interval: timedelta,
            entry: ConfigEntry,
            client: InimPrimeClient,
    ):
        super().__init__(
            hass = hass,
            logger = _LOGGER,
            name = "INIM Prime",
            update_interval = update_interval,
        )
        self.client = client
        self.data: CoordinatorData = CoordinatorData()  # initialize with empty data
        self.entry = entry

    async def _async_update_data(self) -> CoordinatorData:
        """Fetch data from API."""
        try:
            zones = await self.client.get_zones_status()
            partitions = await self.client.get_partitions_status()
            outputs = await self.client.get_outputs_status()
            system_faults = await self.client.get_system_faults_status()
            gsm = await self.client.get_gsm_status()

            self.data.zones = zones
            self.data.partitions = partitions
            self.data.outputs = outputs
            self.data.system_faults = system_faults
            self.data.gsm = gsm

            return self.data
        except Exception as err:
            raise UpdateFailed(err) from err
