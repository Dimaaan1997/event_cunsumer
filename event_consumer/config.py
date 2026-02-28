from event_consumer.schemas.events import PlaylistEvent, BaseEvent
from event_consumer.utils.kafka_consumer import KafkaConsumerConfig
from event_consumer.topic_workers import like_event_worker, play_list_event_worker, listen_event_worker


like_topic_config = KafkaConsumerConfig(topic='like_event',
                                                 worker=like_event_worker,
                                                 consumer_group='like_event_group_4',
                                        worker_schema=BaseEvent)

playlist_topic_config = KafkaConsumerConfig(topic='playlist_event',
                                                 worker=play_list_event_worker,
                                                 consumer_group='playlist_event_group_4',
                                            worker_schema=PlaylistEvent)

listen_topic_config = KafkaConsumerConfig(topic="listen_event",
                                          worker=listen_event_worker,
                                          consumer_group="listen_event_group_4",
                                          worker_schema=BaseEvent)


consumer_config = [like_topic_config,
                   playlist_topic_config,
                   listen_topic_config
                   ]