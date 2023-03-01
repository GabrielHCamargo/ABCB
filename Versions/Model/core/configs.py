from pydantic import BaseSettings


class Settings(BaseSettings):
    WEBHOOK_V1_URL: str = "/webhook/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/abcb"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"

    class Config:
        case_sensitive = True


settings: Settings = Settings()