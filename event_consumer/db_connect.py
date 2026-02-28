from event_consumer.utils.clickhouse import ClSessionMaker, Shard

cl_session_maker = ClSessionMaker(
    Shard(name="test_analytics", url="localhost:8127"),
                                  # Shard(name="shard", url="localhost:8125")
)
