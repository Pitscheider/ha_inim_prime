from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .coordinators import (
    InimPrimeGSMUpdateCoordinator,
    InimPrimePartitionsUpdateCoordinator,
    InimPrimeZonesUpdateCoordinator,
    InimPrimePanelLogEventsCoordinator,
    InimPrimeSystemFaultsUpdateCoordinator,
)

from inim_prime_api import InimPrimeClient
from .const import (
    CONF_SERIAL_NUMBER,
    DOMAIN,
    PANEL_LOG_EVENTS_COORDINATOR,
    ZONES_COORDINATOR,
    PARTITIONS_COORDINATOR,
    GSM_COORDINATOR,
    SYSTEM_FAULTS_COORDINATOR,
    CONF_MAIN_SCAN_INTERVAL,
    CONF_MAIN_SCAN_INTERVAL_DEFAULT,
    CONF_PANEL_LOG_EVENTS_SCAN_INTERVAL,
    CONF_PANEL_LOG_EVENTS_SCAN_INTERVAL_DEFAULT,
)

from .entities.panel import create_panel_device_info

PLATFORMS = [
    "binary_sensor",
    "sensor",
    "switch",
    "select",
    "button",
    "event",
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up INIM Prime integration."""
    hass.data.setdefault(DOMAIN, {})

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    create_panel_device_info(entry)

    host = entry.data["host"]
    api_key = entry.data["api_key"]
    use_https = entry.data.get("use_https", True)

    client = InimPrimeClient(host = host, api_key = api_key, use_https = use_https)
    await client.connect()

    ###
    ### Coordinators
    ###
    main_scan_interval = entry.options.get(CONF_MAIN_SCAN_INTERVAL, CONF_MAIN_SCAN_INTERVAL_DEFAULT)
    panel_log_events_scan_interval = entry.options.get(CONF_PANEL_LOG_EVENTS_SCAN_INTERVAL, CONF_PANEL_LOG_EVENTS_SCAN_INTERVAL_DEFAULT)

    coordinators = {
        ZONES_COORDINATOR: InimPrimeZonesUpdateCoordinator(
            hass = hass,
            update_interval = timedelta(seconds = main_scan_interval),
            entry = entry,
            client = client,
        ),
        PARTITIONS_COORDINATOR: InimPrimePartitionsUpdateCoordinator(
            hass = hass,
            update_interval = timedelta(seconds = main_scan_interval),
            entry = entry,
            client = client,
        ),
        SYSTEM_FAULTS_COORDINATOR: InimPrimeSystemFaultsUpdateCoordinator(
            hass = hass,
            update_interval = timedelta(seconds = main_scan_interval),
            entry = entry,
            client = client,
        ),
        GSM_COORDINATOR: InimPrimeGSMUpdateCoordinator(
            hass = hass,
            update_interval = timedelta(seconds = main_scan_interval),
            entry = entry,
            client = client,
        ),
        PANEL_LOG_EVENTS_COORDINATOR: InimPrimePanelLogEventsCoordinator(
            hass = hass,
            update_interval = timedelta(seconds = panel_log_events_scan_interval),
            entry = entry,
            client = client,
        ),
    }

    await coordinators[ZONES_COORDINATOR].async_config_entry_first_refresh()
    await coordinators[PARTITIONS_COORDINATOR].async_config_entry_first_refresh()
    await coordinators[SYSTEM_FAULTS_COORDINATOR].async_config_entry_first_refresh()
    await coordinators[GSM_COORDINATOR].async_config_entry_first_refresh()

    await coordinators[PANEL_LOG_EVENTS_COORDINATOR].async_startup()
    await coordinators[PANEL_LOG_EVENTS_COORDINATOR].async_config_entry_first_refresh()


    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinators": coordinators,
    }

    await hass.config_entries.async_forward_entry_setups(
        entry = entry,
        platforms = PLATFORMS,
    )

    return True


async def async_remove_config_entry_device(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        device_entry: DeviceEntry,
) -> bool:
    """Allow removing sub-devices but not the panel."""
    for domain, dev_id in device_entry.identifiers:
        # Prevent deleting the panel itself
        if dev_id == config_entry.data[CONF_SERIAL_NUMBER]:
            return False

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload INIM Prime config entry."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload INIM Prime integration."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry = entry,
        platforms = PLATFORMS,
    )

    if unload_ok:
        data = hass.data[DOMAIN].pop(entry.entry_id)

        # Stop coordinators (optional but recommended)
        coordinators = data.get("coordinators", {})

        for coordinator in coordinators.values():
            if coordinator and hasattr(coordinator, "async_shutdown"):
                coordinator.async_shutdown()

        # Close API client
        await data["client"].close()

    return unload_ok
