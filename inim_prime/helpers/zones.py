from inim_prime import InimPrimeClient
from inim_prime.models import ZoneStatus, ZoneExclusionSetRequest


def get_excluded_zones(
        zones: dict[int, ZoneStatus],
) -> dict[int, ZoneStatus]:
    return {
        zone_id: zone
        for zone_id, zone in zones.items()
        if zone.excluded
    }


async def include_all_zones(
        zones: dict[int, ZoneStatus],
        client: InimPrimeClient,
        timeout: int = None,
        retries: int = None,
        retry_delay: float = None,
) -> dict[int, ZoneStatus]:
    excluded_zones = get_excluded_zones(zones)

    for zone in excluded_zones.values():
        request = ZoneExclusionSetRequest(
            zone_id = zone.id,
            exclude = False,
        )
        await client.set_zone_exclusion(
            request = request,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
        )

    return excluded_zones
