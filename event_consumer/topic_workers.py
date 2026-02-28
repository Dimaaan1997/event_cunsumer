from event_consumer.db_connect import cl_session_maker
from event_consumer.queries.user_events import insert_like_object, insert_playlist_object, insert_listening_object
from event_consumer.schemas.events import BaseEvent, PlaylistEvent


async def like_event_worker(messages: list[BaseEvent]):
    async with cl_session_maker() as session:
        for message in messages:
            await session.insert_objects(insert_like_object, values=[tuple(message.model_dump().values())])


async def play_list_event_worker(messages: list[PlaylistEvent]):
    async with cl_session_maker() as session:
        for message in messages:
            await session.insert_objects(insert_playlist_object, values=[tuple(message.model_dump().values())])


async def listen_event_worker(messages: list[BaseEvent]):
    async with cl_session_maker() as session:
        for message in messages:
            await session.insert_objects(insert_listening_object, values=[tuple(message.model_dump().values())])



# async def like_event_worker(message: list[BaseEvent]):
#     async with cl_session_maker() as session:
#         await session.insert_objects(insert_like_object, values=[tuple(message.model_dump().values())])
#
#
# async def play_list_event_worker(message: list[PlaylistEvent]):
#     async with cl_session_maker() as session:
#         await session.insert_objects(insert_playlist_object, values=[tuple(message.model_dump().values())])
#
#
# async def listen_event_worker(message: list[BaseEvent]):
#     async with cl_session_maker() as session:
#         await session.insert_objects(insert_listening_object, values=[tuple(message.model_dump().values())])