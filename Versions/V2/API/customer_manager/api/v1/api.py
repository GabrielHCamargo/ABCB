from fastapi import APIRouter

from api.v1.endpoints import create_customer
from api.v1.endpoints import update_benefit
from api.v1.endpoints import create_discount
from api.v1.endpoints import create_document


api_router: APIRouter = APIRouter()
api_router.include_router(create_customer.router, prefix="/customers", tags=["customers"])
api_router.include_router(update_benefit.router, prefix="/benefits", tags=["benefits"])
api_router.include_router(create_discount.router, prefix="/discounts", tags=["discounts"])
api_router.include_router(create_document.router, prefix="/documents", tags=["documents"])