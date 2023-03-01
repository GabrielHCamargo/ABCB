from fastapi import FastAPI

from core.configs import settings
from webhook.v1.webhook import webhook_router


app: FastAPI = FastAPI(title="Webhook ABCB")
app.include_router(webhook_router, prefix=settings.WEBHOOK_V1_URL)