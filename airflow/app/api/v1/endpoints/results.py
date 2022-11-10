import fastapi

router = fastapi.APIRouter()


@router.post(
    '/',
    status_code=200,
)
async def results():
    pass