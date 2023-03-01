from pydantic import BaseSettings

import os

class Settings(BaseSettings):
    API_V1_URL: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/abcb"
    SEARCH_URL: str  = "http://0.0.0.0:8010"
    FILE_MANAGER_URL: str  = "http://0.0.0.0:8020"
    CUSTOMER_MANAGER_URL: str  = "http://0.0.0.0:8030"
    REPORT_MANAGER_URL: str  = "http://0.0.0.0:8040"
    REPORT_GENERATOR_URL: str  = "http://0.0.0.0:8041"
    USER_MANAGER_URL: str  = "http://0.0.0.0:8050"
    EVENT_URL: str  = "http://0.0.0.0:8060"
    NOTIFICATIONS_URL: str  = "http://0.0.0.0:8070"

    STATUS_CODES_CSV: str = os.path.join(os.getcwd(), "utils/Status_Codes.csv")
    CUSTOMERS_EVENTS_CODES_CSV: str = os.path.join(os.getcwd(), "utils/Customers_Events_Codes.csv")


    class Config:
        case_sensitive = True


settings: Settings = Settings()
