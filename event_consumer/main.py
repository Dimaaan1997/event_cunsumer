import asyncio

from event_consumer.cl_connect import set_cl_connect
from event_consumer.config import (
    like_topic_config,
    listen_topic_config,
    playlist_topic_config,
)
from event_consumer.db_connect import cl_session_maker
from event_consumer.logger import log
from event_consumer.settings import settings
from event_consumer.utils.kafka_consumer import KafkaConsumerCluster


async def main():
    try:
        async with cl_session_maker() as session:
            set_cl_connect(session)
            kafka_cluster = KafkaConsumerCluster(
                like_topic_config,
                playlist_topic_config,
                listen_topic_config,
                kafka_url=settings.kafka_url,
            )
            await kafka_cluster.run_cluster()
            await log.ainfo("run consumer cluster")
    finally:
        set_cl_connect(None)
        await kafka_cluster.stop_cluster()
        await log.ainfo("stop consumer cluster")


if __name__ == "__main__":
    asyncio.run(main())
