from enum import StrEnum


class PlaylistOperationType(StrEnum):
    ADD = "add"
    REMOVE = "remove"


class LikeOperationType(StrEnum):
    LIKE = "like"
    DISLIKE = "dislike"


class ListenOperationType(StrEnum):
    START = "start"
    STOP = "stop"


class EventType(StrEnum):
    LIKE = "like"
    PLAYLIST = "playlist"
    LISTENING = "listening"
