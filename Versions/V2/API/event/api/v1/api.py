from fastapi import APIRouter

from api.v1.endpoints import event
from api.v1.endpoints import notification


api_router: APIRouter = APIRouter()
api_router.include_router(event.router, prefix="/events", tags=["events"])
api_router.include_router(notification.router, prefix="/notifications", tags=["notifications"])