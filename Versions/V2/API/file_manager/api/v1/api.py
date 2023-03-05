from fastapi import APIRouter

from api.v1.endpoints import file


api_router: APIRouter = APIRouter()
api_router.include_router(file.router, prefix="/process", tags=["process"])