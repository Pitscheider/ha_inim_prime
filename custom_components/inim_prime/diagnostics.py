"""Provide diagnostics for INIM Prime integration."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from . import InimPrimeDataUpdateCoordinator
from .const import DOMAIN, CONF_SERIAL_NUMBER


async def async_get_config_entry_diagnostics(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for the config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

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
            for zone_id, zone in coordinator.data.zones.items()
        },
        "partitions": {
            partition_id: {
                "id": partition.id,
                "name": partition.name,
                "state": partition.state.name,
                "mode": partition.mode.name,
                "alarm_memory": partition.alarm_memory,
            }
            for partition_id, partition in coordinator.data.partitions.items()
        },
        "system_faults": {
            "supply_voltage": coordinator.data.system_faults.supply_voltage,
            "faults": [fault.name for fault in coordinator.data.system_faults.faults],
        },
        "gsm": {
            "supply_voltage": coordinator.data.gsm.supply_voltage,
            "firmware_version": coordinator.data.gsm.firmware_version,
            "operator": coordinator.data.gsm.operator,
            "signal_strength": coordinator.data.gsm.signal_strength,
            "credit": coordinator.data.gsm.credit,
        },
    }



async def async_get_device_diagnostics(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        device: DeviceEntry,
) -> dict[str, Any]:
    """Return diagnostics for a device."""

    coordinator: InimPrimeDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

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
                zone = coordinator.data.zones.get(zone_id)
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
                partition = coordinator.data.partitions.get(partition_id)
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
                gsm = coordinator.data.gsm
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
                    "supply_voltage": coordinator.data.system_faults.supply_voltage,
                    "active_faults": [
                        fault.name for fault in coordinator.data.system_faults.faults
                    ],
                    "log_events": coordinator.last_panel_log_events,
                }

    return device_info