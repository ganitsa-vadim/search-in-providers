import asyncio

import fastapi

from app.service import read_provider_response
from app.schemas import response

router = fastapi.APIRouter()


@router.post(
    '/',
    status_code=200,
    response_model=list[response.FlightInfo],
)
async def search():
    response_a: list[dict] = await read_provider_response("response_a.json")
    await asyncio.sleep(60)
    return response_a
