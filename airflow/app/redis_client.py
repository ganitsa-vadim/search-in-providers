import json

import aioredis
from app.schemas import response
from app.schemas import redis as redis_schemas


class RedisClient:
    def __init__(self, url: str, db_number: int):
        self.client = aioredis.from_url(
            url=url,
            db=db_number,
        )

    async def new_record(self, search_id: str) -> None:
        record = redis_schemas.SearchResults(
            search_id=search_id,
            status=str(redis_schemas.SearchStatusTypes.PENDING),
        )
        await self.client.set(
            name=search_id,
            value=record.json(),
        )

    async def update_record(
            self,
            search_id: str,
            items: response.FlightInfo) -> None:
        record: redis_schemas.SearchResults = await self.read_record(search_id=search_id)
        updated_record = self._process_items(record, items)
        await self.client.set(
            name=search_id,
            value=updated_record.json(),
        )

    async def read_record(self, search_id: str) -> redis_schemas.SearchResults:
        record = await self.client.get(search_id)
        unpacked_record = json.loads(record)
        return redis_schemas.SearchResults(**unpacked_record)

    def _process_items(
            self,
            record: redis_schemas.SearchResults,
            items: response.FlightInfo,
    ) -> redis_schemas.SearchResults:
        if not record.items:
            record.items = items
        else:
            record.items += items
        return record