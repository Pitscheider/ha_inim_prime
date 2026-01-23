from inim_prime import InimPrimeClient
from inim_prime.models import PartitionStatus
from inim_prime.models.partition import ClearPartitionAlarmMemoryRequest


def get_partitions_with_alarm_memory(
        partitions: dict[int, PartitionStatus],
) -> dict[int, PartitionStatus]:
    return {
        partition_id: partition
        for partition_id, partition in partitions.items()
        if partition.alarm_memory
    }


async def clear_all_partitions_alarm_memory(
        partitions: dict[int, PartitionStatus],
        client: InimPrimeClient,
        timeout: int = None,
        retries: int = None,
        retry_delay: float = None,
) -> dict[int, PartitionStatus]:
    partitions_with_alarm_memory = get_partitions_with_alarm_memory(partitions)

    for partition in partitions_with_alarm_memory.values():
        request = ClearPartitionAlarmMemoryRequest(
            partition_id = partition.id,
        )
        await client.clear_partition_alarm_memory(
            request = request,
            timeout = timeout,
            retries = retries,
            retry_delay = retry_delay,
        )

    return partitions_with_alarm_memory
