from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_URL: str = "/customer/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/abcb"
    API_GATEWAY_V1_URL: str = "http://0.0.0.0:8000/api/v1"
    SEARCH_V1_URL: str  = "http://0.0.0.0:8010/search/v1"
    FILE_MANAGER_V1_URL: str  = "http://0.0.0.0:8020/file_manager/v1"
    CUSTOMER_MANAGER_V1_URL: str  = "http://0.0.0.0:8030/customer_manager/v1"
    CUSTOMER_V1_URL: str = "http://0.0.0.0:8040/customer/v1"
    REPORT_MANAGER_V1_URL: str  = "http://0.0.0.0:8050/report_manager/v1"
    USER_MANAGER_V1_URL: str  = "http://0.0.0.0:8060/user_manager/v1"
    EVENT_V1_URL: str  = "http://0.0.0.0:8070/event/v1"


    class Config:
        case_sensitive = True


settings: Settings = Settings()
