from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import BackgroundTasks

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from services.document import create_documents


router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=Dict)
async def post_documents(documents: Dict, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_session)):
    
    background_tasks.add_task(create_documents, documents, db)

    return {"msg": "processed data"}