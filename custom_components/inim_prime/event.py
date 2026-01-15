from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN
from custom_components.inim_prime.entities.panel import PanelLogEventsEvent


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    coordinator.last_panel_log_events = await coordinator.async_load_last_panel_log_events()

    entities = []

    entities.append(PanelLogEventsEvent(coordinator, entry))

    async_add_entities(entities, update_before_add=True)