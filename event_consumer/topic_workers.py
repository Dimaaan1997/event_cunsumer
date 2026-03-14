from event_consumer.cl_connect import get_cl_connect
from event_consumer.queries.user_events import (
    insert_like_object,
    insert_listening_object,
    insert_playlist_object,
)
from event_consumer.schemas.events import BaseEvent, PlaylistEvent


async def like_event_worker(messages: list[BaseEvent]):
    session = get_cl_connect()
    await session.insert_objects(
        insert_like_object,
        values=[tuple(message.model_dump().values()) for message in messages],
    )


async def play_list_event_worker(messages: list[PlaylistEvent]):
    session = get_cl_connect()
    for message in messages:
        await session.insert_objects(
            insert_playlist_object, values=[tuple(message.model_dump().values())]
        )


async def listen_event_worker(messages: list[BaseEvent]):
    session = get_cl_connect()
    await session.insert_objects(
        insert_listening_object,
        values=[tuple(message.model_dump().values()) for message in messages],
    )
