from aiokafka.admin import AIOKafkaAdminClient

from event_consumer.utils.kafka_consumer import KafkaConsumerCluster

import asyncio

from event_consumer.config import consumer_config
from event_consumer.logger import log
from event_consumer.settings import settings


async def main():
    try:
        kafka_cluster = KafkaConsumerCluster(kafka_url=settings.kafka_url,
                                             consumers_configs=consumer_config)
        await kafka_cluster.run_cluster()
        await log.ainfo("run consumer cluster")
    finally:
        await kafka_cluster.stop_cluster()
        await log.ainfo("stop consumer cluster")



if __name__ == "__main__":
    asyncio.run(main())



