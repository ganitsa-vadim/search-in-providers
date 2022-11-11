import uuid
import fastapi
import requests

from app.core import config
from app.redis_client import RedisClient
from app import service
from app.schemas.redis import SearchResults

router = fastapi.APIRouter()


@router.post('/', status_code=200)
async def search(background_tasks: fastapi.BackgroundTasks) -> str:
    search_id: str = str(uuid.uuid4())
    background_tasks.add_task(requests.post, f"http://127.0.0.1:9000/api/v1/search/run-task/{search_id}")
    return search_id


@router.get('/results/{search_id}/{currency}', status_code=200)
async def results(search_id: str, currency: str):
    redis_client = RedisClient(
        url=config.redis.url,
        db_number=config.redis.db_search_results,
    )
    record: SearchResults = await redis_client.read_record(search_id=search_id)

    return "Zaebis"


@router.post('/run-task/{search_id}', status_code=200)
async def task(search_id: str):
    redis_client = RedisClient(
        url=config.redis.url,
        db_number=config.redis.db_search_results,
    )
    await redis_client.new_record(search_id=search_id)
    await service.run_tasks(search_id, redis_client)
