from fastapi import FastAPI

from app import service
from app.api import v1
from app.core import config
from app.redis_client import redis_client


app = FastAPI(
    title=config.api.title,
    docs_url=config.api.swagger_url,
    openapi_url=config.api.openapi_url,
)

app.include_router(v1.api_router, prefix='/api/v1')


@app.on_event("startup")
async def startup():
    await service.update_exchange_rates(redis_client=redis_client)


@app.on_event('startup')
async def start_scheduler():
    service.scheduled_tasks.start()


@app.on_event("shutdown")
async def shutdown():
    pass
