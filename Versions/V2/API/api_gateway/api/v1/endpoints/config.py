from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import BackgroundTasks

from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from services.config import create_configs_database


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


router = APIRouter()


# POST Configs
@router.post("/", status_code=status.HTTP_200_OK, response_model=Dict)
async def post_configs(background_task: BackgroundTasks, db: AsyncSession = Depends(get_session)):
    background_task.add_task(create_configs_database, db)
    
    return {"msg": "processed data"}