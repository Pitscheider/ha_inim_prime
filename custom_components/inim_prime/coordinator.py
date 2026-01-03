from dataclasses import dataclass, field
from typing import Dict, TypedDict

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import asyncio
from datetime import timedelta
from inim_prime import InimPrimeClient
from inim_prime.models import AreaStatus, OutputStatus
from inim_prime.models.zone import ZoneStatus
import logging

_LOGGER = logging.getLogger(__name__)

@dataclass
class PanelData:
    zones: Dict[int, ZoneStatus] = field(default_factory=dict)
    areas: Dict[int, AreaStatus] = field(default_factory=dict)
    outputs: Dict[int, OutputStatus] = field(default_factory=dict)


class InimPrimeDataUpdateCoordinator(DataUpdateCoordinator[PanelData]):
    """Coordinator to fetch data from the panel."""

    def __init__(self, hass, client: InimPrimeClient):
        super().__init__(
            hass,
            _LOGGER,
            name="INIM Prime",
            update_interval=timedelta(seconds=10),
        )
        self.client = client
        self.data: PanelData = PanelData()  # initialize with empty data

    async def _async_update_data(self) -> PanelData:
        """Fetch data from API."""
        try:
            zones = await self.client.get_zones_status()
            areas = await self.client.get_areas_status()
            outputs = await self.client.get_outputs_status()

            self.data.zones = zones
            self.data.areas = areas
            self.data.outputs = outputs

            # Optionally fetch areas, outputs, etc.
            return self.data
        except Exception as err:
            raise UpdateFailed(err) from err
