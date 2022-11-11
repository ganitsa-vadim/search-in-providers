import json
import uuid

import fastapi
import requests

from app.core import config
from app.redis_client import RedisClient
from app import service
from app.schemas.redis import SearchResults
from app.schemas.response import Price
from fastapi import status

router = fastapi.APIRouter()


def get_exchange_rates_dict(exchange_rates):
    exchange_rates_dict = {}
    for item in exchange_rates.rates.item:
        exchange_rates_dict[item.title] = item
    return exchange_rates_dict


def add_price_field_and_sort_data_by_price(
        currency: str,
        record: SearchResults,
        exchange_rates_dict,
) -> SearchResults:
    for item in record.items:
        target_currency = exchange_rates_dict[currency]

        if item.pricing.currency == "KZT":
            kzt_price = item.pricing.total
            currency_price = kzt_price / target_currency.description * target_currency.quant
        else:
            current_currency = exchange_rates_dict[item.pricing.currency]
            kzt_price = (item.pricing.total * current_currency.description) / current_currency.quant
            currency_price = kzt_price / target_currency.description * target_currency.quant

        item.price = Price(
            amount="{:.2f}".format(currency_price),
            currency=currency,
        )
    record.items.sort(key=lambda x: x.price.amount)
    return record


@router.post('/', status_code=200)
async def search(background_tasks: fastapi.BackgroundTasks) -> str:
    search_id: str = str(uuid.uuid4())
    background_tasks.add_task(requests.post, f"http://127.0.0.1:9000/api/v1/search/run-task/{search_id}")
    return search_id


@router.get('/results/{search_id}/{currency}', status_code=200, response_model=SearchResults)
async def results(search_id: str, currency: str):
    redis_client = RedisClient(
        url=config.redis.url,
        db_number=0,
    )

    record: SearchResults = await redis_client.read_record(search_id=search_id)

    exchange_rates = await redis_client.get_exchange_rates()
    exchange_rates_dict = get_exchange_rates_dict(exchange_rates)
    if currency not in exchange_rates_dict.keys():
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The selected currency does not exist or is supported",
        )

    target_data: SearchResults = add_price_field_and_sort_data_by_price(
        currency=currency,
        record=record,
        exchange_rates_dict=exchange_rates_dict,
    )
    return target_data


@router.post('/run-task/{search_id}', status_code=200)
async def task(search_id: str):
    redis_client = RedisClient(
        url=config.redis.url,
        db_number=0,
    )
    await redis_client.new_record(search_id=search_id)
    await service.run_tasks(search_id, redis_client)
