import uuid

import fastapi
import requests
from fastapi import responses
from fastapi import status

from app import service
from app.core import config
from app.redis_client import redis_client
from app.schemas.redis import SearchResults


router = fastapi.APIRouter()


@router.post('/')
async def search(background_tasks: fastapi.BackgroundTasks) -> responses.JSONResponse:
    search_id: str = str(uuid.uuid4())
    background_tasks.add_task(
        func=requests.post,
        url=f"http://{config.api.host}:{config.api.port}/api/v1/search/run-task/{search_id}",
    )
    return responses.JSONResponse(
        content={"search_id": search_id},
        status_code=status.HTTP_200_OK,
    )


@router.get('/results/{search_id}/{currency}', status_code=200, response_model=SearchResults)
async def results(search_id: str, currency: str):
    record: SearchResults = await redis_client.read_record(search_id=search_id)
    exchange_rates = await redis_client.get_exchange_rates()
    exchange_rates_dict = service.get_exchange_rates_dict(exchange_rates)

    if currency not in exchange_rates_dict.keys():
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The selected currency does not exist or is supported",
        )
    if record.items:
        target_data: SearchResults = service.add_price_field_and_sort_data_by_price(
            currency=currency,
            record=record,
            exchange_rates_dict=exchange_rates_dict,
        )
        return target_data

    return record


@router.post('/run-task/{search_id}', status_code=200, include_in_schema=False)
async def task(search_id: str):
    await redis_client.new_record(search_id=search_id)
    await service.run_tasks(search_id, redis_client)
    await redis_client.mark_record_completed(search_id=search_id)
