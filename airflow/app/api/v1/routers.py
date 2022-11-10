import fastapi

from .endpoints import results

api_router = fastapi.APIRouter()
api_router.include_router(results.router, prefix="/search", tags=["parsing"])
