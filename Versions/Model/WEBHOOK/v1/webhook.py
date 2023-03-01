from fastapi import APIRouter

from webhook.v1.endpoints import customer
from webhook.v1.endpoints import config


webhook_router = APIRouter()
webhook_router.include_router(config.router, prefix="/configs", tags=["configs"])
webhook_router.include_router(customer.router, prefix="/customers", tags=["customers"])