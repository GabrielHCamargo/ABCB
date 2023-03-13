from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_URL: str = "/file_manager/v1"

    DB_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/abcb"    
    
    API_GATEWAY_V1_URL: str = "http://127.0.0.1:8000/api/v1"
    SEARCH_V1_URL: str  = "http://127.0.0.1:8010/search/v1"
    FILE_MANAGER_V1_URL: str  = "http://127.0.0.1:8020/file_manager/v1"
    CUSTOMER_MANAGER_V1_URL: str  = "http://127.0.0.1:8030/customer_manager/v1"
    CUSTOMER_V1_URL: str = "http://127.0.0.1:8040/customer/v1"
    REPORT_MANAGER_V1_URL: str  = "http://127.0.0.1:8050/report_manager/v1"
    USER_MANAGER_V1_URL: str  = "http://127.0.0.1:8060/user_manager/v1"
    EVENT_V1_URL: str  = "http://127.0.0.1:8070/event/v1"

    SECRET_DOCUMENT_ENCRYPTION_KEY: str = "18446cee1bcb682fad4e546a0e5677ae04106128586e0a2188ef31c5a9f3d96b"

    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION_NAME: str = ""
    AWS_CDN_URL: str = ""
    AWS_BUCKET_NAME: str = ""
    
    UPLOAD_TMP_DIR: str = "./.tmp"
    DELETE_UPLOADED_FILES_AFTER: int = 3600


    class Config:
        case_sensitive = True


settings: Settings = Settings()
