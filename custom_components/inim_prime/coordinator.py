from dataclasses import dataclass, field
from typing import Dict, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
from custom_components.inim_prime import DOMAIN
from custom_components.inim_prime.const import CONF_SERIAL_NUMBER, \
    STORAGE_KEY_LAST_PANEL_EVENT_LOGS
from custom_components.inim_prime.helpers.panel_log_events import deserialize_panel_log_events, \
    serialize_panel_log_events, async_fetch_panel_log_events

from inim_prime import InimPrimeClient
from inim_prime.models import OutputStatus, SystemFaultsStatus, GSMSStatus, LogEvent
from inim_prime.models.partition import PartitionStatus
from inim_prime.models.zone import ZoneStatus
import logging

_LOGGER = logging.getLogger(__name__)


@dataclass
class CoordinatorData:
    system_faults: SystemFaultsStatus = SystemFaultsStatus(supply_voltage=None, faults=frozenset())
    gsm: GSMSStatus = GSMSStatus(supply_voltage=None, firmware_version=None, operator=None, signal_strength=None,
                                 credit=None)
    zones: Dict[int, ZoneStatus] = field(default_factory=dict)
    partitions: Dict[int, PartitionStatus] = field(default_factory=dict)
    outputs: Dict[int, OutputStatus] = field(default_factory=dict)


class InimPrimeDataUpdateCoordinator(DataUpdateCoordinator[CoordinatorData]):
    """Coordinator to fetch data from the panel."""
    STORAGE_VERSION = 1

    panel_log_events_entity = None

    def __init__(self, hass, client: InimPrimeClient, entry: ConfigEntry):
        super().__init__(
            hass,
            _LOGGER,
            name="INIM Prime",
            update_interval=timedelta(seconds=10),
        )
        self.client = client
        self.data: CoordinatorData = CoordinatorData()  # initialize with empty data
        self.entry = entry

        self.last_panel_log_events_store = Store(
            hass,
            self.STORAGE_VERSION,
            f"{DOMAIN}_{entry.data[CONF_SERIAL_NUMBER]}_{STORAGE_KEY_LAST_PANEL_EVENT_LOGS}",
        )

        self.last_panel_log_events: list[LogEvent] = []

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

            current_panel_log_events, current_panel_log_events_filtered = await async_fetch_panel_log_events(
                self.last_panel_log_events or [],
                self.client
            )

            if current_panel_log_events_filtered and self.panel_log_events_entity:
                await self.panel_log_events_entity.handle_events(current_panel_log_events_filtered)

            if current_panel_log_events is not None:
                self.last_panel_log_events = current_panel_log_events
                await self.async_save_current_panel_log_events(self.last_panel_log_events)

            # Optionally fetch partitions, outputs, etc.
            return self.data
        except Exception as err:
            raise UpdateFailed(err) from err

    async def async_load_last_panel_log_events(self):
        """Load logs from HA storage."""
        stored_data = await self.last_panel_log_events_store.async_load()
        if stored_data and "logs" in stored_data:
            last_panel_log_events = deserialize_panel_log_events(stored_data["logs"])
        else:
            last_panel_log_events = []
        return last_panel_log_events

    async def async_save_current_panel_log_events(
            self,
            current_panel_log_events: List[LogEvent]
    ):
        await self.last_panel_log_events_store.async_save(
            {"logs": serialize_panel_log_events(current_panel_log_events)}
        )

    async def async_startup(self) -> None:
        """Load persisted data before first refresh."""
        self.last_panel_log_events = await self.async_load_last_panel_log_events()