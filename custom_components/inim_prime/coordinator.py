from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import asyncio
from datetime import timedelta
from inim_prime import InimPrimeClient
from inim_prime.models.zone import ZoneStatus
import logging

_LOGGER = logging.getLogger(__name__)



class InimPrimeDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from the panel."""

    def __init__(self, hass, client: InimPrimeClient):
        super().__init__(
            hass,
            _LOGGER,
            name="INIM Prime",
            update_interval=timedelta(seconds=10),
        )
        self.client = client
        self.data = {
            "zones": [],
            "areas": [],
            "outputs": [],
        }

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            zones: list[ZoneStatus] = await self.client.get_zones_status()
            self.data["zones"] = zones
            # Optionally fetch areas, outputs, etc.
            return self.data
        except Exception as err:
            raise UpdateFailed(err) from err
