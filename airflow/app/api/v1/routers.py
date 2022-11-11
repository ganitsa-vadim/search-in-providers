import fastapi

from .endpoints import search


api_router = fastapi.APIRouter()
api_router.include_router(search.router, prefix="/search", tags=["search"])
