from fastapi import APIRouter

from api.v1.endpoints import create_customer
from api.v1.endpoints import update_benefit
from api.v1.endpoints import create_discount
from api.v1.endpoints import create_document
from api.v1.endpoints import crud_ticket


api_router: APIRouter = APIRouter()
# Group
api_router.include_router(create_customer.router, prefix="/customers", tags=["customers"])
api_router.include_router(update_benefit.router, prefix="/benefits", tags=["benefits"])
api_router.include_router(create_discount.router, prefix="/discounts", tags=["discounts"])
api_router.include_router(create_document.router, prefix="/documents", tags=["documents"])
# Unique
api_router.include_router(crud_ticket.router, prefix="/tickets", tags=["tickets"])