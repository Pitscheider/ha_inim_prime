import asyncio
import sys

from ..inim_prime_api.models.zone import ZoneExclusionSetRequest
from ..inim_prime_api import InimPrimeClient
from ..inim_prime_api.helpers.zones import get_excluded_zones, include_all_zones

from ..inim_prime_api.models.output import OutputSetRequest
from ..inim_prime_api.models.partition import PartitionMode, SetPartitionModeRequest
from ..inim_prime_api.models.scenario import ActivateScenarioRequest

if sys.platform == "win32":
    # Use SelectorEventLoop for Windows compatibility
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Install first: pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env into environment


def print_help():
    print("\nAvailable commands:")

    print("?. help")
    print("1. ping")
    print("2. get_api_version")
    print("3. get_zones")
    print("4. get_outputs")
    print("5. get_partitions")
    print("6. get_scenarios")
    print("7. get_log_events")
    print("8. get_gsm_status")
    print("9. get_system_faults")
    print("10. set_zone_exclusion")
    print("11. set_output")
    print("12. set_partition_mode")
    print("13. activate_scenario")
    print("101. get_excluded_zones")
    print("102. include_all_zones")
    print("0. quit")


async def main():
    host = os.getenv("INIM_HOST")
    api_key = os.getenv("INIM_API_KEY")

    async with InimPrimeClient(host, api_key) as client:
        print("Connected to Inim Prime panel!")
        print_help()
        while True:
            choice = input("Select an option: ").strip()

            try:
                if choice == "0":
                    print("Exiting...")
                    await client.close()
                    break
                elif choice == "?":
                    print_help()
                elif choice == "1":
                    result = await client.ping()
                    print("Ping result:", result)
                elif choice == "2":
                    version = await client.get_api_version()
                    print("API version:", version)
                elif choice == "3":
                    zones = await client.get_zones_status()
                    for zone in zones.values():
                        print(zone)
                elif choice == "4":
                    outputs = await client.get_outputs_status()
                    for output in outputs.values():
                        print(output)
                elif choice == "5":
                    partitions = await client.get_partitions_status()
                    for partition in partitions.values():
                        print(partition)
                elif choice == "6":
                    scenarios = await client.get_scenarios_status()
                    for scenario in scenarios.values():
                        print(scenario)
                elif choice == "7":
                    user_input = input("Limit (1-4000, default 100): ").strip()

                    if user_input:
                        limit = int(user_input)
                        log_events = await client.get_log_events(limit = limit)
                    else:
                        # user pressed Enter → do not pass limit, let default apply
                        log_events = await client.get_log_events()
                    for log_event in log_events:
                        print(log_event)
                elif choice == "8":
                    gsm_status = await client.get_gsm_status()
                    print(gsm_status)
                elif choice == "9":
                    system_faults = await client.get_system_faults_status()
                    print(system_faults)
                elif choice == "10":
                    zone_id = int(input("Zone ID: "))
                    exclude = bool(int(input("Exclude (default true, 0 = false): ") or 1))

                    request = ZoneExclusionSetRequest(
                        zone_id = zone_id,
                        exclude = exclude,
                    )

                    await client.set_zone_exclusion(request)
                elif choice == "11":
                    try:
                        output_id = int(input("Enter output ID: ").strip())
                        value = int(input("Enter value (0=off, 1=on, 1-100=dimming): ").strip())

                        request = OutputSetRequest(
                            output_id = output_id,
                            value = value,
                        )

                        await client.set_output(request)
                    except ValueError as e:
                        print("Invalid input:", e)
                elif choice == "12":
                    try:
                        partition_id = int(input("Enter partition ID: ").strip())

                        print("Select mode:")
                        for mode in PartitionMode:
                            print(f"{mode.value} = {mode.name}")

                        mode_input = int(input("Enter mode: ").strip())
                        mode = PartitionMode(mode_input)

                        await client.set_partition_mode(
                            SetPartitionModeRequest(partition_id = partition_id, mode = mode)
                        )
                    except ValueError as e:
                        print("Invalid input:", e)
                elif choice == "13":
                    scenario_id = int(input("Enter scenario ID to activate: "))
                    await client.activate_scenario(ActivateScenarioRequest(scenario_id))
                elif choice == "101":
                    zones = await client.get_zones_status()
                    excluded = get_excluded_zones(zones)

                    if excluded:
                        for zone in excluded.values():
                            print(zone)
                    else:
                        print("No zones to exclude")
                elif choice == "102":
                    zones = await client.get_zones_status()
                    included = await include_all_zones(zones, client)

                    if included:
                        print("Zones included:")
                        for zone in included.values():
                            print(zone.short_str())
                    else:
                        print("All the zones are already included")
                else:
                    print("Invalid choice, try again.")
            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())
