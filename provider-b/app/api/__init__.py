from fastapi import FastAPI

from ..core import config
from . import v1


app = FastAPI(
    title=config.api.title,
    docs_url=config.api.swagger_url,
    openapi_url=config.api.openapi_url,
)

app.include_router(v1.api_router, prefix='/api/v1')


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass
