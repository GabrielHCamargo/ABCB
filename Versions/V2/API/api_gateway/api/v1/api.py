from fastapi import APIRouter

from api.v1.endpoints import config
from api.v1.endpoints import upload


api_router = APIRouter()
api_router.include_router(config.router, prefix="/configs", tags=["configs"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])