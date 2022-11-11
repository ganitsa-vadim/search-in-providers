from fastapi import FastAPI

from ..core import config
from . import v1
from ..redis_client import RedisClient

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
        db_number=config.redis.db_exchange_rates,
    )


@app.on_event("shutdown")
async def shutdown():
    pass
