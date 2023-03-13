from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import BackgroundTasks
from fastapi import UploadFile
from fastapi import Depends
from fastapi import HTTPException

from services.manager import common_manager
from services.manager import document_manager

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session


router: APIRouter = APIRouter()


@router.post("/bases", status_code=status.HTTP_200_OK)
async def post_base(file: UploadFile, background_tasks: BackgroundTasks, user_id: int = None, db: AsyncSession = Depends(get_session)):
    
    try:
        background_tasks.add_task(common_manager, file, "base", user_id, db)
        return {"msg": "received data"}
    except:
        raise HTTPException(detail="internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/returns", status_code=status.HTTP_200_OK)
async def post_return(file: UploadFile, background_tasks: BackgroundTasks, user_id: int = None, db: AsyncSession = Depends(get_session)):
    
    try:
        background_tasks.add_task(common_manager, file, "return", user_id, db)
        return {"msg": "received data"}
    except:
        raise HTTPException(detail="internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/transfers", status_code=status.HTTP_200_OK)
async def post_transfer(file: UploadFile, background_tasks: BackgroundTasks, user_id: int = None, db: AsyncSession = Depends(get_session)):
    
    try:
        background_tasks.add_task(common_manager, file, "transfer", user_id, db)
        return {"msg": "received data"}
    except:
        raise HTTPException(detail="internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/documents", status_code=status.HTTP_200_OK)
async def post_document(files: List[UploadFile], background_tasks: BackgroundTasks, user_id: int = None, db: AsyncSession = Depends(get_session)):
    
    try:
        background_tasks.add_task(document_manager, files, "document", user_id, db)
        return {"msg": "received data"}
    except:
        raise HTTPException(detail="internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)