from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .const import (
    DOMAIN,
    CONF_SERIAL_NUMBER,
    PANEL_LOG_EVENTS_COORDINATOR,
    ZONES_COORDINATOR,
    PARTITIONS_COORDINATOR,
    SYSTEM_FAULTS_COORDINATOR,
    GSM_COORDINATOR,
)

from .coordinators import (
    InimPrimeZonesUpdateCoordinator,
    InimPrimePartitionsUpdateCoordinator,
    InimPrimeSystemFaultsUpdateCoordinator,
    InimPrimeGSMUpdateCoordinator,
    InimPrimePanelLogEventsCoordinator,
)

async def async_get_config_entry_diagnostics(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for the config entry."""
    coordinators = hass.data[DOMAIN][config_entry.entry_id]["coordinators"]

    zones_coordinator: InimPrimeZonesUpdateCoordinator = coordinators[ZONES_COORDINATOR]
    partitions_coordinator: InimPrimePartitionsUpdateCoordinator = coordinators[PARTITIONS_COORDINATOR]
    system_faults_coordinator: InimPrimeSystemFaultsUpdateCoordinator = coordinators[SYSTEM_FAULTS_COORDINATOR]
    gsm_coordinator: InimPrimeGSMUpdateCoordinator = coordinators[GSM_COORDINATOR]
    panel_log_events_coordinator: InimPrimePanelLogEventsCoordinator = coordinators[PANEL_LOG_EVENTS_COORDINATOR]

    return {
        "panel": {
            "serial_number": config_entry.data[CONF_SERIAL_NUMBER],
            "host": config_entry.data.get("host"),
            "use_https": config_entry.data.get("use_https"),
        },
        "zones": {
            zone_id: {
                "id": zone.id,
                "name": zone.name,
                "state": zone.state.name,
                "excluded": zone.excluded,
                "alarm_memory": zone.alarm_memory,
            }
            for zone_id, zone in zones_coordinator.data.items()
        },
        "partitions": {
            partition_id: {
                "id": partition.id,
                "name": partition.name,
                "state": partition.state.name,
                "mode": partition.mode.name,
                "alarm_memory": partition.alarm_memory,
            }
            for partition_id, partition in partitions_coordinator.data.items()
        },
        "system_faults": {
            "supply_voltage": system_faults_coordinator.data.supply_voltage,
            "faults": [fault.name for fault in system_faults_coordinator.data.faults],
        },
        "gsm": {
            "supply_voltage": gsm_coordinator.data.supply_voltage,
            "firmware_version": gsm_coordinator.data.firmware_version,
            "operator": gsm_coordinator.data.operator,
            "signal_strength": gsm_coordinator.data.signal_strength,
            "credit": gsm_coordinator.data.credit,
        },
    }


async def async_get_device_diagnostics(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        device: DeviceEntry,
) -> dict[str, Any]:
    """Return diagnostics for a device."""

    coordinators = hass.data[DOMAIN][config_entry.entry_id]["coordinators"]

    zones_coordinator: InimPrimeZonesUpdateCoordinator = coordinators[ZONES_COORDINATOR]
    partitions_coordinator: InimPrimePartitionsUpdateCoordinator = coordinators[PARTITIONS_COORDINATOR]
    system_faults_coordinator: InimPrimeSystemFaultsUpdateCoordinator = coordinators[SYSTEM_FAULTS_COORDINATOR]
    gsm_coordinator: InimPrimeGSMUpdateCoordinator = coordinators[GSM_COORDINATOR]
    panel_log_events_coordinator: InimPrimePanelLogEventsCoordinator = coordinators[PANEL_LOG_EVENTS_COORDINATOR]

    # Extract the device type and ID from the device identifiers
    device_info = {}
    for domain, dev_id in device.identifiers:
        if domain == DOMAIN:
            # Parse the device ID to determine type
            # Examples:
            # - "ABC123_zone_1" -> zone device
            # - "ABC123_partition_1" -> partition device
            # - "ABC123_gsm" -> GSM device
            # - "ABC123" -> panel device

            if "_zone_" in dev_id:
                # Zone device
                zone_id = int(dev_id.split("_zone_")[1])
                zone = zones_coordinator.data.get(zone_id)
                if zone:
                    device_info = {
                        "device_type": "zone",
                        "zone_id": zone.id,
                        "zone_name": zone.name,
                        "state": zone.state.name,
                        "excluded": zone.excluded,
                        "alarm_memory": zone.alarm_memory,
                        # Add any other zone-specific info you want
                    }

            elif "_partition_" in dev_id:
                # Partition device
                partition_id = int(dev_id.split("_partition_")[1])
                partition = partitions_coordinator.data.get(partition_id)
                if partition:
                    device_info = {
                        "device_type": "partition",
                        "partition_id": partition.id,
                        "partition_name": partition.name,
                        "state": partition.state.name,
                        "mode": partition.mode.name,
                        "alarm_memory": partition.alarm_memory,
                    }

            elif "_gsm" in dev_id:
                # GSM device
                gsm = gsm_coordinator.data
                device_info = {
                    "device_type": "gsm",
                    "supply_voltage": gsm.supply_voltage,
                    "firmware_version": gsm.firmware_version,
                    "operator": gsm.operator,
                    "signal_strength": gsm.signal_strength,
                    "credit": gsm.credit,
                }

            else:
                # Panel device
                device_info = {
                    "device_type": "panel",
                    "serial_number": config_entry.data[CONF_SERIAL_NUMBER],
                    "host": config_entry.data.get("host"),
                    "use_https": config_entry.data.get("use_https"),
                    "supply_voltage": system_faults_coordinator.data.supply_voltage,
                    "active_faults": [
                        fault.name for fault in system_faults_coordinator.data.faults
                    ],
                    "log_events": panel_log_events_coordinator.last_panel_log_events,
                }

    return device_info
