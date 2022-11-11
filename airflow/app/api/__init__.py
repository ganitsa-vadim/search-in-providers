from fastapi import FastAPI

from ..core import config
from . import v1
from ..redis_client import RedisClient
import xmltodict
import requests
from ..schemas.exchange_rates import NationalBankResponse

app = FastAPI(
    title=config.api.title,
    docs_url=config.api.swagger_url,
    openapi_url=config.api.openapi_url,
)

app.include_router(v1.api_router, prefix='/api/v1')


@app.on_event("startup")
async def startup():
    redis_client = RedisClient(
        url=config.redis.url,
        db_number=7,
    )
    xml_data = requests.get(url='https://www.nationalbank.kz/rss/get_rates.cfm?fdate=26.10.2021')
    parsed_xml: dict = xmltodict.parse(xml_data.content)
    national_bank_response: NationalBankResponse = NationalBankResponse(**parsed_xml)
    await redis_client.set_exchange_rates(national_bank_response)


@app.on_event("shutdown")
async def shutdown():
    pass
