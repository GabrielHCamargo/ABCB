from fastapi import APIRouter

from api.v1.endpoints import customer
from api.v1.endpoints import benefit
from api.v1.endpoints import discount
from api.v1.endpoints import document


api_router: APIRouter = APIRouter()
api_router.include_router(customer.router, prefix="/customers", tags=["customers"])
api_router.include_router(benefit.router, prefix="/benefits", tags=["benefits"])
api_router.include_router(discount.router, prefix="/discounts", tags=["discounts"])
api_router.include_router(document.router, prefix="/documents", tags=["documents"])