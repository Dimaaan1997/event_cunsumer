from datetime import datetime, UTC
from pydantic import BaseModel, Field, field_validator

from event_consumer.const import EventType, LikeOperationType, PlaylistOperationType, ListenOperationType


class BaseEvent(BaseModel):
    user_id: int | None  = Field(default=None, description="id пользователя")
    track_id: int = Field(description="ID трека")
    event_time: datetime = Field(description="Время события")
    event_type: str = Field(description="тип события")
    operation_type: str = Field(description='тип операции в событии')

    @field_validator('event_time')
    @classmethod
    def event_time_validator(cls, value: datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S.%f')


class PlaylistEvent(BaseEvent):
    playlist_id: int = Field(description="ID плейлиста")

