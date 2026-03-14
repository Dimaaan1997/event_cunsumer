from datetime import UTC, datetime

from pydantic import BaseModel, Field, field_serializer


class BaseEvent(BaseModel):
    user_id: int | None = Field(default=None)
    track_id: int
    event_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    event_type: str
    operation_type: str

    @field_serializer("event_time")
    def serialize_event_time(self, value: datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S.%f")


class PlaylistEvent(BaseEvent):
    playlist_id: int
