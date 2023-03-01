from fastapi import FastAPI

from core.configs import settings

from api.v1.api import api_router


app: FastAPI = FastAPI(title="API Gateway - ABCB")
app.include_router(api_router, prefix=settings.API_V1_URL)

