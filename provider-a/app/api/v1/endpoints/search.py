import fastapi

router = fastapi.APIRouter()


@router.post(
    '/',
    status_code=200,
    # response_model=,
)
async def search():
    pass
