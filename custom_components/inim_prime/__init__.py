from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .const import DOMAIN, PANEL_LOG_EVENTS_COORDINATOR
from .coordinator import InimPrimeDataUpdateCoordinator
from inim_prime import InimPrimeClient
from .coordinators.panel_log_events_coordinator import InimPrimePanelLogEventsCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up INIM Prime integration."""
    hass.data.setdefault(DOMAIN, {})

    host = entry.data["host"]
    api_key = entry.data["api_key"]
    use_https = entry.data.get("use_https", True)

    client = InimPrimeClient(host=host, api_key=api_key, use_https=use_https)
    await client.connect()

    main_coordinator = InimPrimeDataUpdateCoordinator(hass, client, entry)
    panel_log_events_coordinator = InimPrimePanelLogEventsCoordinator(hass, client, entry)

    await panel_log_events_coordinator.async_startup()
    await panel_log_events_coordinator.async_config_entry_first_refresh()
    await main_coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": main_coordinator,
        PANEL_LOG_EVENTS_COORDINATOR: panel_log_events_coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(
        entry = entry,
        platforms = [
            "binary_sensor",
            "sensor",
            "switch",
            "select",
            "button",
            "event",
        ]
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
        if dev_id == config_entry.entry_id:
            return False

    return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload INIM Prime config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload INIM Prime integration."""
    data = hass.data[DOMAIN].pop(entry.entry_id)
    await data["client"].close()
    return True
