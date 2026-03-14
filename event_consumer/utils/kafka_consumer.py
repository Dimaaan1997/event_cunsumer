import asyncio
from asyncio import Task
from collections.abc import Awaitable
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer
from aiokafka.admin import AIOKafkaAdminClient
from orjson import orjson
from pydantic import BaseModel, ValidationError

from event_consumer.logger import log

TYPE_ERROR = "Type not serializable"

BATCH_SIZE = 400
POLL_TIMEOUT_MS = 1000


@dataclass
class KafkaConsumerConfig:
    topic: str
    worker: Awaitable
    worker_schema: BaseModel | None = None
    consumer_group: str | None = None


class KafkaConsumerCluster:

    @staticmethod
    def _process_message(msg) -> dict:
        return orjson.loads(msg.value.decode())

    def __init__(self, *consumers_configs: KafkaConsumerConfig, kafka_url: str):

        self.bootstrap_server = kafka_url
        self.consumers: list[AIOKafkaConsumer] = []
        self.consumers_configs = consumers_configs
        self.consumer_tasks: list[Task] = []

    def _create_consumer(self, config: KafkaConsumerConfig):
        consumer = AIOKafkaConsumer(
            config.topic,
            bootstrap_servers=self.bootstrap_server,
            group_id=config.consumer_group,
            auto_offset_reset="earliest",
            enable_auto_commit=False,  # (Кафка коммтитит прочитанные сообщения)
            # enable_auto_commit = True
        )
        self.consumers.append(consumer)
        return consumer

    async def run_cluster(self):
        for config in self.consumers_configs:
            consumer = self._create_consumer(config)
            # self.consumer_tasks.append(asyncio.create_task(self._run_consumer(consumer=consumer, config=config)))
            self.consumer_tasks.append(
                asyncio.create_task(
                    self._run_consumer_batch(consumer=consumer, config=config)
                )
            )
        await asyncio.gather(*self.consumer_tasks)

    async def stop_cluster(self):
        for consumer in self.consumers:
            await consumer.stop()

    async def wait_for_offsets_topic(self):
        admin = AIOKafkaAdminClient(bootstrap_servers=self.bootstrap_server)
        await admin.start()
        try:
            while True:
                topics = await admin.list_topics()
                if "__consumer_offsets" in topics:
                    break
                await log.ainfo(event="__consumer_offsets not exist")
                await asyncio.sleep(1)
        finally:
            await admin.stop()

    async def _run_consumer(
        self, consumer: AIOKafkaConsumer, config: KafkaConsumerConfig
    ):
        await consumer.start()
        await log.ainfo(
            event="consumer started", topic=config.topic, group=config.consumer_group
        )
        async for msg in consumer:
            message = self._process_message(msg)
            if config.worker_schema:
                try:
                    message = config.worker_schema(**message)
                    await config.worker(message)
                except ValidationError as err:
                    await log.aerror("message is invalid", err=err)

    async def _run_consumer_batch(
        self, consumer: AIOKafkaConsumer, config: KafkaConsumerConfig
    ):
        await consumer.start()
        await log.ainfo(
            event="consumer started", topic=config.topic, group=config.consumer_group
        )
        while True:
            batch = []
            records = await consumer.getmany(
                timeout_ms=POLL_TIMEOUT_MS,
                max_records=BATCH_SIZE,
            )

            for tp, messages in records.items():
                for msg in messages:
                    data = self._process_message(msg)
                    message = config.worker_schema(**data)
                    batch.append(message)
            if batch:
                await config.worker(batch)
                await consumer.commit()
                await log.ainfo(
                    event="Обработка сообщений", topic=config.topic, number=len(batch)
                )
