from fastapi import FastAPI

from api.v1.api import api_router
from core.configs import settings


app = FastAPI(
    upload_tmp_dir=settings.UPLOAD_TMP_DIR,
    delete_uploaded_files_after=settings.DELETE_UPLOADED_FILES_AFTER,
)
app.include_router(api_router, prefix=settings.API_V1_URL)