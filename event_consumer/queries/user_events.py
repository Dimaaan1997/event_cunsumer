from event_consumer.utils.clickhouse import SqlQuery

insert_like_object = SqlQuery(
    """
INSERT INTO shard.user_events
(user_id, track_id, event_time, event_type, operation_type)
VALUES
"""
)

insert_playlist_object = SqlQuery(
    """
INSERT INTO shard.user_events
(user_id, track_id, event_time, event_type, operation_type, playlist_id)
VALUES
"""
)


insert_listening_object = SqlQuery(
    """
INSERT INTO
shard.user_events
(user_id, track_id, event_time, event_type, operation_type)
VALUES
"""
)
