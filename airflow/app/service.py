import aiohttp
import json

import pydantic
import requests
import xmltodict

from app.core import config
from app.schemas.exchange_rates import NationalBankResponse, Item
from app.schemas.redis import SearchResults
from app.schemas.response import FlightInfo, Price
from app.redis_client import RedisClient
import asyncio

import aiocron


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
            kzt_price: float = item.pricing.total
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


@aiocron.crontab('* 12 * * *')
async def scheduled_tasks():
    redis_client = RedisClient(
        url=config.redis.url,
        db_number=0,
    )
    await update_exchange_rates(redis_client=redis_client)


async def update_exchange_rates(redis_client: RedisClient):
    xml_data = requests.get(url='https://www.nationalbank.kz/rss/get_rates.cfm?fdate=26.10.2021')
    parsed_xml: dict = xmltodict.parse(xml_data.content)
    national_bank_response: NationalBankResponse = NationalBankResponse(**parsed_xml)
    national_bank_response.rates.item.append(Item(
        fullname="КАЗАХСТАНСКИЙ ТЕНГЕ",
        title='KZT',
        description=1,
        quant=1,
        index="GOOD",
        change=0,
    ))
    await redis_client.set_exchange_rates(national_bank_response)
