import uuid
import aiohttp
import fastapi
import asyncio

router = fastapi.APIRouter()


def write_to_redis():
    pass


async def send_response_and_write_to_redis(
        session: aiohttp.ClientSession,
        url: str,
        search_id: str,
) -> str:
    async with session.post(url) as resp:
        content: str = await resp.text()

        return content


@router.post(
    '/',
    status_code=200,
)
async def search():
    search_id: str = str(uuid.uuid4())
    write_to_redis()
    async with aiohttp.ClientSession() as session:
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
                ),
            )

            tasks.append(task)
        await asyncio.gather(*tasks)
