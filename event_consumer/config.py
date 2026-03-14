from event_consumer.schemas.events import BaseEvent, PlaylistEvent
from event_consumer.topic_workers import (
    like_event_worker,
    listen_event_worker,
    play_list_event_worker,
)
from event_consumer.utils.kafka_consumer import KafkaConsumerConfig

like_topic_config = KafkaConsumerConfig(
    topic="like_event",
    worker=like_event_worker,
    consumer_group="like_event_group",
    worker_schema=BaseEvent,
)

playlist_topic_config = KafkaConsumerConfig(
    topic="playlist_event",
    worker=play_list_event_worker,
    consumer_group="playlist_event_group",
    worker_schema=PlaylistEvent,
)

listen_topic_config = KafkaConsumerConfig(
    topic="listen_event",
    worker=listen_event_worker,
    consumer_group="listen_event_group",
    worker_schema=BaseEvent,
)
