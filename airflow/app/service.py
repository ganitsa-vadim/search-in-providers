import aiohttp
import json

import pydantic

from app.schemas.response import FlightInfo
from app.redis_client import RedisClient
import asyncio


async def send_response_and_write_to_redis(
        session: aiohttp.ClientSession,
        url: str,
        search_id: str,
        redis_client: RedisClient,
):
    async with session.post(url) as resp:
        content: str = await resp.text()

    items: list[FlightInfo] = pydantic.parse_obj_as(
        type_=list[FlightInfo],
        obj=json.loads(content),
    )
    await redis_client.update_record(search_id=search_id, items=items)


def create_tasks(
        session: aiohttp.ClientSession,
        search_id: str,
        redis_client: RedisClient,
):
    tasks = []
    urls = [
        'http://127.0.0.1:8000/api/v1/search/',
        'http://127.0.0.1:8001/api/v1/search/',
    ]
    for url in urls:
        task = asyncio.create_task(
            coro=send_response_and_write_to_redis(
                session=session,
                url=url,
                search_id=search_id,
                redis_client=redis_client,
            ),
        )

        tasks.append(task)
    return tasks


async def run_tasks(search_id, redis_client):
    async with aiohttp.ClientSession() as session:
        tasks = create_tasks(
            session=session,
            search_id=search_id,
            redis_client=redis_client,
        )
        await asyncio.gather(*tasks)
