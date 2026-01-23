from __future__ import annotations

import asyncio
import ssl
from datetime import datetime
from typing import Any

import aiohttp

from .const import *
from .exceptions import *
from .models.gsm import GSMSStatus
from .models.log_event import LogEvent
from .models.output import OutputSetRequest, OutputStatus, OutputType
from .models.partition import (
    SetPartitionModeRequest,
    PartitionMode,
    ClearPartitionAlarmMemoryRequest,
    PartitionStatus,
    PartitionState,
)
from .models.scenario import ScenarioStatus, ActivateScenarioRequest
from .models.system_faults import SystemFaultsStatus, SystemFault
from .models.zone import ZoneExclusionSetRequest, ZoneStatus, ZoneState


def _handle_status(status: int) -> None:
    if status == STATUS_SUCCESS:
        return
    message, exc_class = STATUS_EXCEPTIONS.get(
        status,
        (f"Unknown API error: {status}", InimPrimeError)
    )
    raise exc_class(message)


def _parse_float(value: str | None) -> float | None:
    """Parse a float, handling European decimal comma."""
    if not value:
        return None
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return None


def _parse_faults(value: str | int) -> frozenset[SystemFault]:
    bitmap = int(value or 0)

    return frozenset(
        fault
        for fault in SystemFault
        if (bitmap >> fault.value) & 1
    )


def _create_ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.set_ciphers("DEFAULT:@SECLEVEL=1")
    return context


class InimPrimeClient:
    """
    Async client for INIM Prime HTTP API.
    """

    def __init__(
            self,
            host: str,
            api_key: str,
            timeout: int = 20,
            use_https: bool = True,
            ping_on_connect = True,
    ) -> None:
        scheme = "https" if use_https else "http"
        self._base_url = f"{scheme}://{host.rstrip('/')}"
        self._api_key = api_key
        self._timeout = aiohttp.ClientTimeout(total = timeout)
        self._use_https = use_https
        self._ping_on_connect = ping_on_connect
        self._session: aiohttp.ClientSession | None = None

    # Enable usage of 'async with'
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self) -> None:
        if self._session is not None:
            return

        connector = None

        if self._use_https:
            ssl_context = await asyncio.to_thread(_create_ssl_context)
            connector = aiohttp.TCPConnector(ssl = ssl_context)

        self._session = aiohttp.ClientSession(
            timeout = self._timeout,
            connector = connector,
        )

        if self._ping_on_connect:
            await self.ping()

    async def close(self) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    async def _request(
            self,
            cmd: str,
            timeout: int | None = None,
            retries: int | None = None,
            retry_delay: float | None = None,
            **params: Any,
    ) -> Any:
        if not self._session:
            raise RuntimeError("Client not connected")

        query = {"apikey": self._api_key, "cmd": cmd}
        query.update(params)
        url = f"{self._base_url}{API_PATH}"

        request_timeout = aiohttp.ClientTimeout(total = timeout) if timeout else self._timeout
        retries = retries or 0
        retry_delay = retry_delay or 0.5

        attempt = 0
        while True:
            try:
                async with self._session.get(url, params = query, timeout = request_timeout) as response:
                    if response.status != 200:
                        raise InimPrimeExecutionError(f"HTTP error {response.status}")
                    data = await response.json()

                status = data.get("Status")
                if status != STATUS_SUCCESS:
                    _handle_status(status)

                return data.get("Data")
            except(aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt > retries:
                    raise
                attempt += 1
                print(f"Request failed ({e}), retrying {attempt}/{retries} in {retry_delay}s...")
                await asyncio.sleep(retry_delay)

    async def get_api_version(
            self,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> str:
        raw_data = await self._request(
            cmd = CMD_VERSION,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
        )
        version = raw_data.get("version")
        return version

    async def ping(
            self,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> bool:
        await self._request(
            cmd = CMD_PING,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
        )
        return True

    async def get_zones_status(
            self,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> dict[int, ZoneStatus]:
        raw_data = await self._request(
            cmd = CMD_GET_ZONES_STATUS,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
        )

        zones_data = raw_data.get("zone", [])

        zones = {
            int(zone_data["id"]): ZoneStatus(
                id = int(zone_data["id"]),
                name = zone_data["lb"],
                terminal = int(zone_data["tl"]),
                state = ZoneState(int(zone_data["st"])),
                alarm_memory = bool(int(zone_data["mm"])),
                excluded = not bool(int(zone_data["by"])),  # by=1 means included
            )
            for zone_data in zones_data
        }

        return zones

    async def get_outputs_status(
            self,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> dict[int, OutputStatus]:
        raw_data = await self._request(
            cmd = CMD_GET_OUTPUTS_STATUS,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
        )

        outputs_data = raw_data.get("cmd", [])

        outputs = {
            int(output_data["id"]): OutputStatus(
                id = int(output_data["id"]),
                name = output_data["lb"],
                terminal = int(output_data["tl"]),
                state = int(output_data["st"]),
                type = OutputType(int(output_data["t"])),
                voltage = _parse_float(output_data.get("v")) if "v" in output_data else None,
                power = _parse_float(output_data.get("p")) if "p" in output_data else None,
                cos_phi = _parse_float(output_data.get("c")) if "c" in output_data else None,
            )
            for output_data in outputs_data
        }

        return outputs

    async def get_partitions_status(
            self,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> dict[int, PartitionStatus]:
        raw_data = await self._request(
            cmd = CMD_GET_PARTITIONS_STATUS,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
        )

        partitions_data = raw_data.get("part", [])

        partitions = {
            int(partition_data["id"]): PartitionStatus(
                id = int(partition_data["id"]),
                name = partition_data["lb"],
                state = PartitionState(int(partition_data["st"])),
                mode = PartitionMode(int(partition_data["am"])),
                alarm_memory = bool(int(partition_data["mm"])),
            )
            for partition_data in partitions_data
        }

        return partitions

    async def get_scenarios_status(
            self,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> dict[int, ScenarioStatus]:
        raw_data = await self._request(
            cmd = CMD_GET_SCENARIOS_STATUS,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
        )

        scenarios_data = raw_data.get("sce", [])

        scenarios = {
            int(scenario_data["id"]): ScenarioStatus(
                id = int(scenario_data["id"]),
                name = scenario_data["lb"],
                state = bool(int(scenario_data["st"])),
            )
            for scenario_data in scenarios_data
        }

        return scenarios

    async def get_log_events(
            self,
            limit: int,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> list[LogEvent]:
        if not 1 <= limit <= 4000:
            raise ValueError("limit must be between 1 and 4000")

        timeout = timeout or 120 if limit > 500 else None

        raw_data = await self._request(
            cmd = CMD_GET_LOG_ELEMENTS,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
            p1 = limit,
        )

        log_events_data = raw_data.get("log", [])

        log_events = [
            LogEvent(
                id = int(log_event_data["id"]),
                timestamp = datetime.strptime(
                    log_event_data["dt"], "%d/%m/%Y %H:%M:%S"
                ),
                type = log_event_data["ty"],
                agent = log_event_data["lo"] or None,
                location = log_event_data["ag"] or None,
                value = log_event_data["v"] or None,
            )
            for log_event_data in log_events_data
        ]

        return log_events

    async def get_gsm_status(
            self,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> GSMSStatus:
        raw_data = await self._request(
            cmd = CMD_GET_GSM_STATUS,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
        )

        gsm_status = GSMSStatus(
            supply_voltage = _parse_float(raw_data.get("vcc")),
            firmware_version = raw_data.get("fwv") or None,
            operator = raw_data.get("gop") or None,
            signal_strength = int(raw_data["gpw"]) if raw_data.get("gpw") else None,
            credit = raw_data.get("cre") if raw_data.get("cre") != "--" else None,
        )

        return gsm_status

    async def get_system_faults_status(
            self,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> SystemFaultsStatus:
        raw_data = await self._request(
            cmd = CMD_GET_FAULTS_STATUS,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
        )

        system_faults_status = SystemFaultsStatus(
            supply_voltage = _parse_float(raw_data.get("vcc")),
            faults = _parse_faults(raw_data.get("fau")),
        )

        return system_faults_status

    async def set_zone_exclusion(
            self,
            request: ZoneExclusionSetRequest,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> None:

        zone_id = request.zone_id

        p2 = int(request.exclude)

        await self._request(
            cmd = CMD_SET_ZONES_MODE,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
            p1 = zone_id,
            p2 = p2,
        )

        return

    async def set_output(
            self,
            request: OutputSetRequest,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> None:

        if not 0 <= request.value <= 100:
            raise ValueError("Output value must be between 0 and 100")

        await self._request(
            cmd = CMD_SET_OUTPUTS_MODE,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
            p1 = request.output_id,
            p2 = request.value,
        )

        return

    async def set_partition_mode(
            self,
            request: SetPartitionModeRequest,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> None:

        await self._request(
            cmd = CMD_SET_PARTITIONS_MODE,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
            p1 = request.partition_id,
            p2 = request.mode.value,
        )

        return

    async def clear_partition_alarm_memory(
            self,
            request: ClearPartitionAlarmMemoryRequest,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> None:
        await self._request(
            cmd = CMD_SET_PARTITIONS_MODE,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
            p1 = request.partition_id,
            p2 = 5,
        )

        return

    async def activate_scenario(
            self,
            request: ActivateScenarioRequest,
            timeout: int = None,
            retries: int = None,
            retry_delay: float = None,
    ) -> None:
        await self._request(
            cmd = CMD_SET_SCENARIOS_MODE,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
            p1 = request.scenario_id,
        )
