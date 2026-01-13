from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .const import DOMAIN
from .coordinator import InimPrimeDataUpdateCoordinator
from inim_prime import InimPrimeClient


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up INIM Prime integration."""
    hass.data.setdefault(DOMAIN, {})

    host = entry.data["host"]
    api_key = entry.data["api_key"]
    use_https = entry.data.get("use_https", True)

    # Crea client
    client = InimPrimeClient(host=host, api_key=api_key, use_https=use_https)
    await client.connect()

    # Crea coordinator
    coordinator = InimPrimeDataUpdateCoordinator(hass, client, entry)
    await coordinator.async_config_entry_first_refresh()

    # Salva nel dict di HA
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }

    # Forward setup alle piattaforme
    # Nuovo metodo corretto per HA 2025+
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

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload INIM Prime integration."""
    data = hass.data[DOMAIN].pop(entry.entry_id)
    await data["client"].close()
    return True
