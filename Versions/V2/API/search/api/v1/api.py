from fastapi import APIRouter

from api.v1.endpoints import customer
from api.v1.endpoints import ticket


api_router: APIRouter = APIRouter()
api_router.include_router(customer.router, prefix="/customers", tags=["customers"])
api_router.include_router(ticket.router, prefix="/tickets", tags=["tickets"])