from .const import DOMAIN, PANEL_LOG_EVENTS_COORDINATOR
from .coordinators.panel_log_events_coordinator import InimPrimePanelLogEventsCoordinator
from .entities.panel import PanelLogEventsEvent


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    panel_log_events_coordinator: InimPrimePanelLogEventsCoordinator = hass.data[DOMAIN][entry.entry_id][PANEL_LOG_EVENTS_COORDINATOR]

    entities = []

    panel_log_events_event = PanelLogEventsEvent(panel_log_events_coordinator, entry)
    panel_log_events_coordinator.panel_log_events_entity = panel_log_events_event

    entities.append(panel_log_events_event)

    async_add_entities(entities, update_before_add = True)
