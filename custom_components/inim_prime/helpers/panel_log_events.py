from typing import List

from custom_components.inim_prime import InimPrimeDataUpdateCoordinator
from inim_prime.models import LogEvent
from datetime import datetime


# ───────────────
# Serialization helpers
# ───────────────
def serialize_panel_log_event(event: LogEvent) -> dict:
    return {
        "id": event.id,
        "timestamp": event.timestamp.isoformat(),
        "type": event.type,
        "agent": event.agent,
        "location": event.location,
        "value": event.value,
    }


def deserialize_panel_log_event(data: dict) -> LogEvent:
    return LogEvent(
        id=data["id"],
        timestamp=datetime.fromisoformat(data["timestamp"]),
        type=data["type"],
        agent=data.get("agent"),
        location=data.get("location"),
        value=data.get("value"),
    )


def serialize_panel_log_events(logs: List[LogEvent]) -> list[dict]:
    return [serialize_panel_log_event(l) for l in logs]


def deserialize_panel_log_events(data: list[dict]) -> List[LogEvent]:
    return [deserialize_panel_log_event(d) for d in data]