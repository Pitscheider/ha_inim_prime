from custom_components.inim_prime import InimPrimeDataUpdateCoordinator, DOMAIN, PANEL_LOG_EVENTS_COORDINATOR
from custom_components.inim_prime.entities.panel import PanelLogEventsEvent


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    panel_log_events_coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][PANEL_LOG_EVENTS_COORDINATOR]

    entities = []

    entities.append(PanelLogEventsEvent(panel_log_events_coordinator, entry))

    async_add_entities(entities, update_before_add=True)