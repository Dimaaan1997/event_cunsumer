from contextlib import asynccontextmanager
from aiochclient import ChClient, Record
from aiohttp import ClientSession
from clickhouse_driver import Client
from dataclasses import dataclass
import asyncio

@dataclass
class Shard:
    name: str
    url: str
    password: str | None = None


class SqlQuery(str):
    pass

class Session:

    def __init__(self, client: ChClient):
        self._client = client

    async def insert_objects(self, insert_query: SqlQuery, values: list[tuple]):
        await self._client.execute(insert_query, *values)

    async def select_objects(self, select_query: SqlQuery, as_dict: bool = False) -> list[Record | dict]:
        return await self._client.fetch(select_query, json=as_dict)


class ClConnection:

    def __init__(self, shard: Shard):
        self.client_session = ClientSession()
        self.shard = shard

    async def __aenter__(self) -> Session:
        client = ChClient(self.client_session, url=f'http://{self.shard.url}', password=self.shard.password)
        return Session(client)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client_session.close()


class ClSessionMaker:

    def __init__(self, *shards):
        self.shards = shards
        self.shards_mapping: dict[str, Shard] = {item.name: item for item in shards}

    @asynccontextmanager
    async def __call__(self, shard_name: str | None = None) -> Session:
        shard_config = self.shards[0] if not shard_name else self.shards_mapping[shard_name]
        async with ClConnection(shard_config) as session:
            yield session


















