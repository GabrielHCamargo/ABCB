from fastapi import FastAPI

from api.v1.api import api_router
from core.configs import settings


app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_URL)