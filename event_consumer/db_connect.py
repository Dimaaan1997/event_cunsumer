from event_consumer.settings import settings
from event_consumer.utils.clickhouse import ClSessionMaker, Shard

cl_session_maker = ClSessionMaker(
    Shard(name=settings.cl_shard_name, url=settings.cl_url),
)
