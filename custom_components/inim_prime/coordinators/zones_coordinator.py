import logging
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from inim_prime_api import InimPrimeClient
from inim_prime_api.models.partition import PartitionStatus
from inim_prime_api.models.zone import ZoneStatus
from inim_prime_api.models.system_faults import SystemFaultsStatus
from inim_prime_api.models.gsm import GSMSStatus
from inim_prime_api.models.output import OutputStatus

_LOGGER = logging.getLogger(__name__)

class InimPrimeZonesUpdateCoordinator(DataUpdateCoordinator[Dict[int, ZoneStatus]]):
    """Coordinator to fetch zones from the panel."""

    def __init__(
            self,
            hass: HomeAssistant,
            update_interval: timedelta,
            entry: ConfigEntry,
            client: InimPrimeClient,
    ):
        super().__init__(
            hass = hass,
            config_entry = entry,
            logger = _LOGGER,
            name = "INIM Prime Zones",
            update_interval = update_interval,
        )
        self.client = client
        self.data: Dict[int, ZoneStatus] = {}  # just an empty dict
        self.entry = entry

    async def _async_update_data(self) -> Dict[int, ZoneStatus]:
        """Fetch data from API."""
        try:
            zones = await self.client.get_zones_status()

            self.data = zones

            return self.data
        except Exception as err:
            raise UpdateFailed(err) from err
